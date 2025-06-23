import sqlite3
import os
import string
import random
from flask import Flask, render_template, redirect, request, url_for, g, jsonify, abort, send_from_directory

# --- App-Konfiguration ---
app = Flask(__name__)
# Den Debug-Modus können wir für die "Produktion" später auf False setzen
app.config['DEBUG'] = True

# --- Datenbank-Setup & Helfer ---
DB_FILE = "dumbshort.db"

def get_db():
    """Öffnet eine neue Datenbankverbindung, wenn noch keine für diesen Request existiert."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_FILE)
        # Sorgt dafür, dass wir Dictionaries statt Tupel von der DB zurückbekommen
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Schließt die Datenbankverbindung am Ende des Requests."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

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
            id INTEGER PRIMARY KEY CHECK (id = 1), -- Erzwingt, dass es nur eine Zeile gibt
            total_created INTEGER NOT NULL DEFAULT 0
        )
    ''')
    
    # Sicherstellen, dass die eine Statistik-Zeile existiert
    cursor.execute('INSERT OR IGNORE INTO stats (id, total_created) VALUES (1, 0)')
    
    conn.commit()
    conn.close()
    print("Datenbank initialisiert und einsatzbereit.")


def generate_short_code(length=7):
    """Generiert einen zufälligen, dummen Kurz-Code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# --- Haupt-, PWA- und Umleitungs-Routen ---

@app.route('/')
def index():
    """Zeigt die Hauptseite (Single Page Application)."""
    return render_template('index.html')

@app.route('/<string:short_code>')
def redirect_to_url(short_code):
    """Sucht den Code, erhöht den Klickzähler und leitet zur Original-URL um."""
    db = get_db()
    link = db.execute('SELECT id, original_url FROM links WHERE short_code = ?', (short_code,)).fetchone()

    if link:
        db.execute('UPDATE links SET clicks = clicks + 1 WHERE id = ?', (link['id'],))
        db.commit()
        return redirect(link['original_url'])
    else:
        # Wirft einen 404-Fehler, den unser Handler fängt
        abort(404)

@app.route('/sw.js')
def service_worker():
    """Liefert die Service-Worker-Datei für die PWA."""
    return send_from_directory('.', 'sw.js')


# --- API-Routen für das Frontend ---

@app.route('/api/shorten', methods=['POST'])
def shorten_api():
    """Nimmt eine URL als JSON entgegen und gibt das Ergebnis als JSON zurück."""
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'URL fehlt.'}), 400

    db = get_db()
    
    # Prüfen, ob die URL schon existiert und die ID holen
    existing_link = db.execute('SELECT id, short_code FROM links WHERE original_url = ?', (original_url,)).fetchone()
    
    if existing_link:
        short_code = existing_link['short_code']
        link_id = existing_link['id']
    else:
        # Wenn nicht, neuen Code generieren, speichern und ID holen
        while True:
            short_code = generate_short_code()
            if not db.execute('SELECT id FROM links WHERE short_code = ?', (short_code,)).fetchone():
                break
        
        cursor = db.execute('INSERT INTO links (original_url, short_code) VALUES (?, ?)', (original_url, short_code))
        link_id = cursor.lastrowid # ID des soeben erstellten Eintrags
        
        db.execute('UPDATE stats SET total_created = total_created + 1 WHERE id = 1')
        db.commit()

    short_url = request.host_url + short_code
    
    # Wir geben jetzt ein sauberes JSON-Objekt mit der ID zurück
    return jsonify({
        'id': link_id,
        'original_url': original_url,
        'short_url': short_url,
        'short_code': short_code
    })

@app.route('/api/links', methods=['GET'])
def get_links():
    """Gibt eine Liste aller Links zurück, sortiert nach Erstellungsdatum."""
    db = get_db()
    links_cursor = db.execute('SELECT id, name, original_url, short_code, clicks, created_at FROM links ORDER BY created_at DESC')
    links = [dict(row) for row in links_cursor.fetchall()]
    return jsonify(links)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Berechnet und liefert die globalen Statistiken aus den Tabellen."""
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
    # Wenn die Anfrage an eine "normale" URL ging, zeige unsere coole 404-Seite
    # Dies verhindert, dass bei einem API-Tippfehler eine HTML-Seite zurückkommt
    if request.path != '/' and not request.path.startswith('/api') and not request.path.startswith('/static') and not request.path == '/sw.js':
        return render_template('404.html'), 404
    # Für andere 404-Fehler (z.B. falsche API-URL) geben wir einen JSON-Fehler zurück
    return jsonify({'error': 'Not Found'}), 404


# --- App starten ---
if __name__ == '__main__':
    # init_db() wird beim ersten Request automatisch durch die Logik in get_db und die Tabellenerstellung getriggert.
    # Wir können es aber explizit hier aufrufen, um sicherzugehen, dass die DB beim Start bereit ist.
    init_db()
    app.run(host='0.0.0.0', port=5000)