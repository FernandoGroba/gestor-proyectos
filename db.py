import os
import shutil
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_NAME = str(Path(os.getenv("FLET_APP_STORAGE_DATA", str(BASE_DIR))) / "proyectos.db")


def init_db():
    if not os.path.exists(DB_NAME) and (BASE_DIR / "proyectos.db").exists():
        os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
        shutil.copyfile(BASE_DIR / "proyectos.db", DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    conn.execute("""
        CREATE TABLE IF NOT EXISTS proyecto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            descripcion TEXT,
            cliente TEXT,
            valor_hora REAL,
            horas REAL,
            aprobado INTEGER   -- 0 = No Aprobado, 1 = Aprobado, 2 = Pendiente
        )
    """)
    conn.execute("CREATE TABLE IF NOT EXISTS config (key TEXT PRIMARY KEY, value TEXT)")
    conn.commit()

    cantidad = conn.execute("SELECT COUNT(*) FROM config").fetchone()[0]
    if cantidad == 0:
        conn.execute("INSERT INTO config (key, value) VALUES (?, ?)", ("tarifa_a", "8000"))
        conn.execute("INSERT INTO config (key, value) VALUES (?, ?)", ("tarifa_b", "10650"))
        conn.commit()

    conn.close()


def insertar_proyecto(datos):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    nuevo_id = conn.execute(
        "INSERT INTO proyecto (nombre, descripcion, cliente, valor_hora, horas, aprobado) VALUES (?, ?, ?, ?, ?, ?)",
        (datos["nombre"], datos["descripcion"], datos["cliente"],
         datos["valor_hora"], datos["horas"], datos["aprobado"]),
    ).lastrowid
    conn.commit()
    conn.close()
    return nuevo_id


def list_proyectos(filtro=None):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    if filtro is None or filtro == "todas":
        filas = conn.execute("SELECT * FROM proyecto ORDER BY id DESC").fetchall()
    else:
        filas = conn.execute("SELECT * FROM proyecto WHERE aprobado = ? ORDER BY id DESC", (filtro,)).fetchall()

    conn.close()
    return [dict(fila) for fila in filas]


def get_proyecto(id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    fila = conn.execute("SELECT * FROM proyecto WHERE id = ?", (id,)).fetchone()
    conn.close()
    return dict(fila) if fila else None


def update_proyecto(id, datos):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute(
        "UPDATE proyecto SET nombre = ?, descripcion = ?, cliente = ?, valor_hora = ?, horas = ?, aprobado = ? WHERE id = ?",
        (datos["nombre"], datos["descripcion"], datos["cliente"],
         datos["valor_hora"], datos["horas"], datos["aprobado"], id),
    )
    conn.commit()
    conn.close()


def get_config():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    filas = conn.execute("SELECT * FROM config").fetchall()
    conn.close()
    return {fila["key"]: fila["value"] for fila in filas}


def set_config(tarifa_a, tarifa_b):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("UPDATE config SET value = ? WHERE key = 'tarifa_a'", (tarifa_a,))
    conn.execute("UPDATE config SET value = ? WHERE key = 'tarifa_b'", (tarifa_b,))
    conn.commit()
    conn.close()


def eliminar_proyecto(id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM proyecto WHERE id = ?", (id,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()