import sqlite3
import os
import string
import random
from flask import Flask, render_template, redirect, request, url_for, g, jsonify, abort, send_from_directory

# --- App-Konfiguration ---
app = Flask(__name__)
app.config['DEBUG'] = True # Kann für Produktion auf False gesetzt werden

# --- Datenbank-Setup & Helfer ---
# Dieser Pfad wird vom Docker-Volume gemountet
DATA_DIR = "/app/data"
DB_FILE = os.path.join(DATA_DIR, "dumbshort.db")

# Wir müssen sicherstellen, dass das Datenverzeichnis existiert, bevor wir es benutzen
os.makedirs(DATA_DIR, exist_ok=True)

def init_db():
    """Initialisiert die Datenbank und die Tabellen, falls sie nicht existieren."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Tabelle für die Links
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            original_url TEXT NOT NULL UNIQUE,
            short_code TEXT NOT NULL UNIQUE,
            clicks INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabelle für die Gesamt-Statistik
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            total_created INTEGER NOT NULL DEFAULT 0
        )
    ''')
    
    # Sicherstellen, dass die eine Statistik-Zeile existiert
    cursor.execute('INSERT OR IGNORE INTO stats (id, total_created) VALUES (1, 0)')
    
    conn.commit()
    conn.close()
    print("Datenbank-Initialisierung geprüft.")

# ======================================================================
# WICHTIGER FIX: Wir rufen init_db() direkt hier auf.
# Das wird ausgeführt, sobald Gunicorn die Datei importiert, und stellt sicher,
# dass die Datenbank bereit ist, bevor die erste Anfrage kommt.
# ======================================================================
init_db()

def get_db():
    """Öffnet eine neue Datenbankverbindung pro Request."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_FILE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Schließt die Datenbankverbindung am Ende des Requests."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def generate_short_code(length=7):
    """Generiert einen zufälligen Kurz-Code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# --- Haupt-, PWA- und Umleitungs-Routen ---

@app.route('/')
def index():
    """Zeigt die Hauptseite (Single Page Application)."""
    return render_template('index.html')

@app.route('/sw.js')
def service_worker():
    """Liefert den Service Worker für die PWA."""
    return send_from_directory('.', 'sw.js')

@app.route('/favicon.ico')
def favicon():
    # We could return an icon, but to simply suppress the 404 error,
    # we send a "204 No Content" response. It's dumb, but effective.
    return '', 204

@app.route('/<string:short_code>')
def redirect_to_url(short_code):
    """Sucht den Code, erhöht den Klickzähler und leitet um."""
    db = get_db()
    link = db.execute('SELECT id, original_url FROM links WHERE short_code = ?', (short_code,)).fetchone()

    if link:
        db.execute('UPDATE links SET clicks = clicks + 1 WHERE id = ?', (link['id'],))
        db.commit()
        return redirect(link['original_url'])
    else:
        abort(404)

# --- API-Routen für das Frontend ---

@app.route('/api/shorten', methods=['POST'])
def shorten_api():
    """Nimmt eine URL als JSON entgegen und gibt das Ergebnis als JSON zurück."""
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'URL fehlt.'}), 400

    db = get_db()
    existing_link = db.execute('SELECT id, short_code FROM links WHERE original_url = ?', (original_url,)).fetchone()
    
    if existing_link:
        short_code = existing_link['short_code']
        link_id = existing_link['id']
    else:
        while True:
            short_code = generate_short_code()
            if not db.execute('SELECT id FROM links WHERE short_code = ?', (short_code,)).fetchone():
                break
        
        cursor = db.execute('INSERT INTO links (original_url, short_code) VALUES (?, ?)', (original_url, short_code))
        link_id = cursor.lastrowid
        
        db.execute('UPDATE stats SET total_created = total_created + 1 WHERE id = 1')
        db.commit()

    short_url = request.host_url + short_code
    
    return jsonify({
        'id': link_id,
        'original_url': original_url,
        'short_url': short_url,
        'short_code': short_code
    })

@app.route('/api/links', methods=['GET'])
def get_links():
    """Gibt eine Liste aller Links zurück."""
    db = get_db()
    links_cursor = db.execute('SELECT id, name, original_url, short_code, clicks, created_at FROM links ORDER BY created_at DESC')
    links = [dict(row) for row in links_cursor.fetchall()]
    return jsonify(links)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Liefert die globalen Statistiken."""
    db = get_db()
    
    stats_row = db.execute('SELECT total_created FROM stats WHERE id = 1').fetchone()
    active_links = db.execute('SELECT COUNT(id) FROM links').fetchone()[0] or 0
    total_clicks = db.execute('SELECT SUM(clicks) FROM links').fetchone()[0] or 0
    
    return jsonify({
        'total_created': stats_row['total_created'] if stats_row else 0,
        'active_links': active_links,
        'total_clicks': total_clicks
    })

@app.route('/api/links/<int:link_id>', methods=['DELETE'])
def delete_link(link_id):
    """Löscht einen Link anhand seiner ID."""
    db = get_db()
    db.execute('DELETE FROM links WHERE id = ?', (link_id,))
    db.commit()
    return jsonify({'success': True, 'message': 'Link wurde dumm gelöscht.'})

@app.route('/api/links/<int:link_id>/name', methods=['PUT'])
def update_link_name(link_id):
    """Aktualisiert den Namen eines bestehenden Links."""
    data = request.get_json()
    new_name = data.get('name', '').strip()

    db = get_db()
    db.execute('UPDATE links SET name = ? WHERE id = ?', (new_name, link_id))
    db.commit()
    
    return jsonify({'success': True, 'message': 'Name wurde dumm aktualisiert.'})

# --- Error Handler ---

@app.errorhandler(404)
def not_found_error(error):
    """Liefert die benutzerdefinierte 404-Seite für normale Routen."""
    if request.path != '/' and not request.path.startswith(('/api', '/static')):
        return render_template('404.html'), 404
    return jsonify({'error': 'Not Found'}), 404

# --- Startblock für lokales Debugging ---
if __name__ == '__main__':
    # Bei lokalem Start wird init_db() ebenfalls ganz oben ausgeführt.
    app.run(host='0.0.0.0', port=5000)