import sqlite3
import os
import string
import random
from flask import Flask, render_template, redirect, request, url_for, g, jsonify, abort, send_from_directory

app = Flask(__name__)

DATA_DIR = "/app/data"
DB_FILE = os.path.join(DATA_DIR, "dumbshort.db")
os.makedirs(DATA_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, original_url TEXT NOT NULL UNIQUE,
            short_code TEXT NOT NULL UNIQUE, clicks INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY CHECK (id = 1), total_created INTEGER NOT NULL DEFAULT 0)
    ''')
    cursor.execute('INSERT OR IGNORE INTO stats (id, total_created) VALUES (1, 0)')
    conn.commit()
    conn.close()
    print("Datenbank-Initialisierung geprüft.")

init_db()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_FILE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None: db.close()

def generate_short_code(length=7):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# --- Routen ---

@app.route('/')
def index(): return render_template('index.html')

@app.route('/sw.js')
def service_worker(): return send_from_directory('.', 'sw.js')

@app.route('/favicon.ico')
def favicon(): return send_from_directory('static/icons', 'icon-192x192.png')

@app.route('/<string:short_code>')
def redirect_to_url(short_code):
    db = get_db()
    link = db.execute('SELECT id, original_url FROM links WHERE short_code = ?', (short_code,)).fetchone()
    if link:
        db.execute('UPDATE links SET clicks = clicks + 1 WHERE id = ?', (link['id'],))
        db.commit()
        # Keine Reparatur mehr nötig, die URL in der DB ist jetzt immer korrekt.
        return redirect(link['original_url'])
    else:
        abort(404)

# --- API Routen ---

@app.route('/api/shorten', methods=['POST'])
def shorten_api():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL fehlt.'}), 400
    
    original_url_input = data['url'].strip()

    # DER FINALE VALIDIERUNGS-FIX
    # Dumme, aber effektive Prüfung: Hat es einen Punkt und ist nicht nur ein Punkt?
    if '.' not in original_url_input or len(original_url_input) < 4:
        return jsonify({'error': 'Ungültige URL.'}), 400

    # Reparatur der URL (wird erst hier durchgeführt)
    if not original_url_input.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url_input
    else:
        original_url = original_url_input

    db = get_db()
    existing_link = db.execute('SELECT id, short_code FROM links WHERE original_url = ?', (original_url,)).fetchone()
    if existing_link:
        link_id, short_code = existing_link['id'], existing_link['short_code']
    else:
        while True:
            short_code = generate_short_code()
            if not db.execute('SELECT id FROM links WHERE short_code = ?', (short_code,)).fetchone(): break
        cursor = db.execute('INSERT INTO links (original_url, short_code) VALUES (?, ?)', (original_url, short_code))
        link_id = cursor.lastrowid
        db.execute('UPDATE stats SET total_created = total_created + 1 WHERE id = 1')
        db.commit()
    
    short_url = request.host_url + short_code
    return jsonify({'id': link_id, 'original_url': original_url, 'short_url': short_url, 'short_code': short_code})

@app.route('/api/links', methods=['GET'])
def get_links():
    db = get_db()
    links = db.execute('SELECT id, name, original_url, short_code, clicks FROM links ORDER BY created_at DESC').fetchall()
    return jsonify([dict(row) for row in links])

@app.route('/api/stats', methods=['GET'])
def get_stats():
    db = get_db()
    stats_row = db.execute('SELECT total_created FROM stats WHERE id = 1').fetchone()
    active_links = db.execute('SELECT COUNT(id) FROM links').fetchone()[0] or 0
    total_clicks = db.execute('SELECT SUM(clicks) FROM links').fetchone()[0] or 0
    return jsonify({'total_created': stats_row['total_created'] if stats_row else 0, 'active_links': active_links, 'total_clicks': total_clicks})

@app.route('/api/links/<int:link_id>', methods=['DELETE'])
def delete_link(link_id):
    db = get_db()
    db.execute('DELETE FROM links WHERE id = ?', (link_id,))
    db.commit()
    return jsonify({'success': True})

@app.route('/api/links/<int:link_id>/name', methods=['PUT'])
def update_link_name(link_id):
    data = request.get_json()
    new_name = data.get('name', '').strip()
    db = get_db()
    db.execute('UPDATE links SET name = ? WHERE id = ?', (new_name, link_id))
    db.commit()
    return jsonify({'success': True})

@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api/'): return jsonify({'error': 'Not Found'}), 404
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)