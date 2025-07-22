from flask import Flask, request, redirect, jsonify
import psycopg2
from psycopg2 import sql
import bcrypt

app = Flask(__name__)

# Configuración de PostgreSQL
db_config = {
    'dbname': 'devops_tools',
    'user': 'postgres',
    'password': 'password',
    'host': 'db',
    'port': '5432'
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

@app.route('/api/message', methods=['GET'])
def get_message():
    return jsonify({"message": "Hello DevOps"})

@app.route('/api/contact', methods=['POST'])
def post_contact():
    name = request.form.get('name')
    activity = request.form.get('activity')
    email = request.form.get('email')
    phone = request.form.get('phone')
    description = request.form.get('description')
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql.SQL("INSERT INTO contacts (name, activity, email, phone, description) VALUES (%s, %s, %s, %s, %s)"),
                    (name, activity, email, phone, description)
                )
        return redirect('/tools.html')
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")
        return jsonify({"error": "Error al procesar el formulario"}), 500
    finally:
        conn.close()

@app.route('/api/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not all([name, email, password]):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    try:
        with conn:
            with conn.cursor() as cur:
                # Verificar si el correo ya existe
                cur.execute(
                    sql.SQL("SELECT email FROM users WHERE email = %s"),
                    (email,)
                )
                if cur.fetchone():
                    return jsonify({"error": "El correo ya está registrado"}), 400
                
                # Hashear contraseña
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                
                # Insertar usuario
                cur.execute(
                    sql.SQL("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"),
                    (name, email, hashed_password.decode('utf-8'))
                )
        return jsonify({"message": "Registro exitoso"}), 200
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return jsonify({"error": "Error al procesar el registro"}), 500
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not all([email, password]):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql.SQL("SELECT password FROM users WHERE email = %s"),
                    (email,)
                )
                result = cur.fetchone()
                if not result:
                    return jsonify({"error": "Correo no registrado"}), 400
                
                stored_password = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    return jsonify({"message": "Inicio de sesión exitoso"}), 200
                else:
                    return jsonify({"error": "Contraseña incorrecta"}), 400
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return jsonify({"error": "Error al procesar el inicio de sesión"}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
