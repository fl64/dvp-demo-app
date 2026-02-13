from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2
import os
import socket

load_dotenv(dotenv_path='/app/.env')

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'host')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'db')

@app.route('/health/ready', methods=['GET'])
def readiness():
    try:
        # todo
        # conn = psycopg2.connect(...)
        # conn.close()
        return jsonify({"status": "ready"}), 200
    except Exception as e:
        return jsonify({"status": "not ready", "error": str(e)}), 500

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )

@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM test_table")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([{"id": row[0], "name": row[1]} for row in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data', methods=['POST'])
def add_data():
    try:
        data = request.json
        name = data.get('name')
        if not name:
            return jsonify({"error": "Name is required"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO test_table (name) VALUES (%s) RETURNING id", (name,))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"id": new_id, "name": name}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM test_table WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": f"Record with ID {id} deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nodes', methods=['GET'])
def get_nodes():
    try:
        # Get current node information (backend)
        backend_hostname = socket.gethostname()
        backend_ip = None
        try:
            # Try to get IP via connection to external address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            backend_ip = s.getsockname()[0]
            s.close()
        except:
            try:
                backend_ip = socket.gethostbyname(backend_hostname)
            except:
                pass

        # Check database availability
        db_available = False
        try:
            conn = get_db_connection()
            conn.close()
            db_available = True
        except:
            pass

        # Backend is always VM (from k8s structure)
        backend_type = 'vm'

        # Frontend can be pod or VM - determine by environment variable or hostname
        frontend_hostname = request.headers.get('Host', 'unknown')
        frontend_type = os.getenv('FRONTEND_TYPE', '').lower()
        if not frontend_type:
            # Try to determine by hostname or other indicators
            # If hostname contains typical pod indicators (e.g., contains dashes and digits)
            if '-' in frontend_hostname and any(c.isdigit() for c in frontend_hostname):
                frontend_type = 'container'
            else:
                frontend_type = 'vm'

        return jsonify({
            'frontend': {
                'hostname': frontend_hostname,
                'type': frontend_type,
                'available': True
            },
            'backend': {
                'hostname': backend_hostname,
                'ip': backend_ip or backend_hostname,
                'type': backend_type,
                'available': True  # If endpoint responds, it's available
            },
            'database': {
                'hostname': DB_HOST,
                'type': 'vm',  # DB is always VM
                'available': db_available
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
