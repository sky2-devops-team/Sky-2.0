from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "clientes.db"

app = Flask(__name__)

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT,
            categoria TEXT
        )
    """)
    con.commit()
    con.close()

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/clients")
def list_clients():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM clientes ORDER BY id DESC")
    rows = [dict(r) for r in cur.fetchall()]
    con.close()
    return jsonify(rows)

@app.get("/clients/<int:cid>")
def get_client(cid):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM clientes WHERE id=?", (cid,))
    row = cur.fetchone()
    con.close()
    if not row:
        return jsonify(error="not found"), 404
    return jsonify(dict(row))

@app.post("/clients")
def create_client():
    data = request.get_json(force=True)
    nombre = data.get("nombre")
    email = data.get("email")
    telefono = data.get("telefono")
    categoria = data.get("categoria")
    if not nombre or not email:
        return jsonify(error="nombre y email son requeridos"), 400
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO clientes(nombre,email,telefono,categoria) VALUES(?,?,?,?)",
        (nombre, email, telefono, categoria),
    )
    con.commit()
    new_id = cur.lastrowid
    con.close()
    return jsonify(id=new_id, nombre=nombre, email=email, telefono=telefono, categoria=categoria), 201

@app.put("/clients/<int:cid>")
def update_client(cid):
    data = request.get_json(force=True)
    fields = []
    vals = []
    for k in ("nombre","email","telefono","categoria"):
        if k in data and data[k] is not None:
            fields.append(f"{k}=?")
            vals.append(data[k])
    if not fields:
        return jsonify(error="sin cambios"), 400
    vals.append(cid)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"UPDATE clientes SET {', '.join(fields)} WHERE id=?", vals)
    con.commit()
    con.close()
    return jsonify(updated=True)

@app.delete("/clients/<int:cid>")
def delete_client(cid):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("DELETE FROM clientes WHERE id=?", (cid,))
    con.commit()
    con.close()
    return jsonify(deleted=True)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)
else:
    init_db()
