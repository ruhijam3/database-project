import os
from uuid import uuid4
from flask import Flask, jsonify, request, session
from flask_cors import CORS 
import psycopg2.extras

import psycopg2
from dotenv import load_dotenv

# database connection info stored in .env
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Database connection (from your db_script.py)
def get_db_connection():
    return psycopg2.connect(
        host='127.0.0.1',
        database='culturalheritage',
        user='postgres',
        password='password',
        port=5432
    )

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Flask API is running'})

@app.route('/location', methods=['GET'])
def get_sites():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('SELECT * FROM egypt_heritage.location')
        sites = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(sites), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# added for phase 2
    # POST /location  -> insert one location
@app.route('/location', methods=['POST'])
def create_location():
    data = request.get_json(force=True) or {}
    # adjust field names if your column names differ
    required = ['name', 'city', 'latitude', 'longitude']
    missing = [k for k in required if data.get(k) in (None, "")]
    if missing:
        return jsonify({'error': f"missing fields: {', '.join(missing)}"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        new_id = str(uuid4())
        cur.execute("""
            INSERT INTO egypt_heritage.location
              (name, street, city, zip_code, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (
            data['name'],
            data.get('street'),
            data['city'],
            data.get('zip_code'),
            data['latitude'],
            data['longitude'],
        ))
        conn.commit()
        cur.close(); conn.close()
        return jsonify({'name': data['name']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE /location/<name>  -> delete by name
@app.route('/location/<name>', methods=['DELETE'])
def delete_location(name):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM egypt_heritage.site WHERE dname = %s;", (name,))
        cur.execute("DELETE FROM egypt_heritage.location WHERE name = %s;", (name,))
        deleted = cur.rowcount
        conn.commit()
        cur.close(); conn.close()

        if deleted == 0:
            return jsonify({'error': 'not found'}), 404
        return jsonify({'deleted': name}), 200

    except psycopg2.Error as e:
        # foreign-key conflict (row referenced elsewhere)
        if getattr(e, "pgcode", None) == "23503":
            return jsonify({'error': 'Cannot delete: row is referenced by other records.'}), 409
        return jsonify({'error': str(e)}), 500

#@app.route('/items', methods=['GET'])
#def get_items():
    # ... code here

if __name__ == '__main__':
    print("=" * 50)
    print("Starting Flask server...")
    print("API running at: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000)