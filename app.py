# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2
from urllib.parse import urlparse
import os

app = Flask(__name__, template_folder="templates")  # templates folder me index.html rakho
CORS(app)

# Render External DB URL
DATABASE_URL = 'postgresql://api_control_panel_user:P3M6R2CJbIsdePfCep1YLXxgFc7dBPgp@dpg-d4ng4r6uk2gs739r2hs0-a.oregon-postgres.render.com/api_control_panel'
result = urlparse(DATABASE_URL)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=result.hostname,
    port=result.port,
    database=result.path[1:],
    user=result.username,
    password=result.password,
    sslmode="require"
)
cur = conn.cursor()

# Ensure table exists
cur.execute("""
CREATE TABLE IF NOT EXISTS api_urls (
    id SERIAL PRIMARY KEY,
    type CHARACTER VARYING(50) UNIQUE NOT NULL,
    url CHARACTER VARYING(255) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()

# ------------------ ROUTES ------------------

# Serve index.html
@app.route("/")
def home():
    return render_template("index.html")

# Fetch URLs
@app.route('/api', methods=['GET'])
def get_urls():
    cur.execute("SELECT type, url FROM api_urls;")
    rows = cur.fetchall()
    data = {row[0]: row[1] for row in rows}
    return jsonify(data)

# Save/Update URL
@app.route('/api', methods=['POST'])
def save_url():
    data = request.json
    field = data.get('field')
    value = data.get('value')
    if not field or not value:
        return jsonify({'error':'Field and value required'}),400

    cur.execute("""
    INSERT INTO api_urls (type,url)
    VALUES (%s,%s)
    ON CONFLICT (type) DO UPDATE SET url=EXCLUDED.url, updated_at=NOW();
    """,(field,value))
    conn.commit()
    return jsonify({'success':True})

# ------------------ RUN APP ------------------
if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))  # Render dynamically assigns port
    app.run(host="0.0.0.0", port=port, debug=True)
