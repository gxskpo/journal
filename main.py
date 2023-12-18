import hashlib
import typing as t
from typing import List, Any

import cryptography
from flask import Flask, request, jsonify, render_template
from utils import DataBase
import ecn

app = Flask(__name__)
database = DataBase('local.db', check_same_thread=False)

initial_query = """
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash TEXT NOT NULL,
    note TEXT NOT NULL
);
"""


@app.route("/", methods=["GET"])
async def root():
    return render_template("index.html")


@app.route("/notes/", methods=["GET"])
async def notes():
    return render_template("notes.html")


@app.route("/notes/new/", methods=["GET"])
async def new_notes():
    return render_template("new_note.html")


@app.route("/notes/<note_hash>/", methods=["GET"])
async def note_view(note_hash):
    return render_template("note_view.html", note_hash=note_hash)


async def add_note(password, note):
    note_hash = hashlib.sha256(note.encode()).hexdigest()
    note_encrypted = ecn.encrypt(note, password)
    query = """
    INSERT INTO notes (hash, note) 
    VALUES (?, ?)
    """
    database.execute(query, (note_hash, note_encrypted))
    return note_hash


async def get_notes() -> int | list[Any]:
    data = database.read("SELECT * FROM notes")
    if data:
        d = [{"id": row[0], "hash": row[1], "note": row[2].decode()} for row in data]
        print(d)
        return d
    return []


async def remove_note() -> int | list[Any]:
    data = database.execute("DELETE FROM notes WHERE hash = '{note_hash}'")
    if data:
        return data
    return []


@app.route("/api/notes/", methods=["POST", "GET", "DELETE"])
async def api_notes():
    match request.method:
        case "POST":
            data = request.json
            note = data.get("note")
            password = data.get("password")
            if not note or not password:
                return jsonify({"error": "Missing required data"}), 400
            note_hash = await add_note(password, note)
            return jsonify({"note_hash": note_hash}), 201

        case "GET":
            notes = await get_notes()
            return jsonify(notes), 200
        case "DELETE":
            data = request.json
            note_hash = data.get("note_hash")
            password = data.get("password")
            if not note_hash or not password:
                return jsonify({"error": "Missing required data"}), 400
            note_hash = await remove_note()
            return jsonify({"note_hash": note_hash}), 201
        case _:
            return jsonify({"error": "Method not allowed"}), 405


@app.route("/api/notes/<note_hash>", methods=["POST"])
async def api_note_view(note_hash):
    match request.method:
        case "POST":
            try:
                data = database.read(f"SELECT * FROM notes WHERE hash = '{note_hash}'")
                if data and request.json:
                    note = data[0][2].decode()
                    return jsonify({"note": ecn.decrypt(note, request.json.get("password"))}), 200
            except UnicodeDecodeError:
                return jsonify({"error": "Invalid password", "note": "Error while decoding content"}), 400
        case _:
            return jsonify({"error": "Method not allowed"}), 405


if __name__ == "__main__":
    database.execute(initial_query)
    app.run(debug=True)
