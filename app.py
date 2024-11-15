from flask import Flask, jsonify, request
from http import HTTPStatus
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/api/books", methods=["GET"])
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"success": True, "data": books, "total": len(books)}), HTTPStatus.OK

@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    cursor.close()
    conn.close()
    if book is None:
        return jsonify({"success": False, "error": "Book not found"}), HTTPStatus.NOT_FOUND
    return jsonify({"success": True, "data": book}), HTTPStatus.OK

@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), HTTPStatus.BAD_REQUEST

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE books SET title = %s, author = %s, year = %s WHERE id = %s",
        (data.get("title"), data.get("author"), data.get("year"), book_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({"success": False, "error": "Book not found"}), HTTPStatus.NOT_FOUND

    return jsonify({"success": True, "message": "Book updated successfully"}), HTTPStatus.OK

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({"success": False, "error": "Book not found"}), HTTPStatus.NOT_FOUND

    return jsonify({"success": True, "message": f"Book with id {book_id} has been deleted."}), HTTPStatus.OK

if __name__ == "__main__":
    app.run(debug=True)
