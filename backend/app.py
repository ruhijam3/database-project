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

#@app.route('/items', methods=['GET'])
#def get_items():
    # ... code here

if __name__ == '__main__':
    print("=" * 50)
    print("Starting Flask server...")
    print("API running at: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5000)