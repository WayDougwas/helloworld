import sqlite3
import hashlib
from pathlib import Path

# Use Path.home() corretamente
home = Path.home()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def criar_db(database):
    # Caminho para o banco de dados
    db_path = home / 'test' / database
    db_path.parent.mkdir(parents=True, exist_ok=True)  # Criar diretório se não existir
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Criação da tabela se não existir
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Banco de dados e tabela OK.")

def registrar_usuario(username, password, database):
    db_path = home / 'test' / database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    hashed_password = hash_password(password)
    
    try:
        c.execute('''
            INSERT INTO usuarios (username, password)
            VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()
        print("Usuário registrado com sucesso.")
    except sqlite3.IntegrityError:
        print("Nome de usuário já existe.")
    finally:
        conn.close()

def autenticar_usuario(username, password, database):
    db_path = home / 'test' / database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    hashed_password = hash_password(password)
    
    c.execute('''
        SELECT * FROM usuarios
        WHERE username = ? AND password = ?
    ''', (username, hashed_password))
    
    user = c.fetchone()
    conn.close()
    
    if user:
        print("Login bem-sucedido!")
        return True
    else:
        print("Nome de usuário ou senha incorretos.")
        return False
