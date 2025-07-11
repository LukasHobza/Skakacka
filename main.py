from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# inicializace databáze
def init_db():
    conn = sqlite3.connect('skore.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS skore (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jmeno TEXT NOT NULL,
            skore INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/uloz_skore', methods=['POST'])
def uloz_skore():
    data = request.get_json()
    jmeno = data['jmeno']
    skore = data['skore']

    conn = sqlite3.connect('skore.db')
    c = conn.cursor()
    c.execute('INSERT INTO skore (jmeno, skore) VALUES (?, ?)', (jmeno, skore))
    conn.commit()
    conn.close()

    return jsonify({"stav": "OK"}), 200

@app.route('/tabulka', methods=['GET'])
def tabulka():
    conn = sqlite3.connect('skore.db')
    c = conn.cursor()
    c.execute('SELECT jmeno, skore FROM skore ORDER BY skore DESC LIMIT 10')
    vysledky = c.fetchall()
    conn.close()
    return jsonify(vysledky)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
