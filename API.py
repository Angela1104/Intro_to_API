from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "year": 1925,
    },
    {
        "id": 2,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "year": 1988,
    },
    {
        "id": 3,
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J. K. Rowling",
        "year": 1997,
    },
    {
        "id": 4,
        "title": "The Mortal Instruments: City of Bones",
        "author": "Cassandra Clare",
        "year": 2007,
    }
]

def find_book(book_id):
    return next((book for book in books if book["id"] == book_id), None)

@app.route("/api/books", methods=["GET"])
def get_books():
    return jsonify({"success": True, "data": books, "total": len(books)}), HTTPStatus.OK

@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = find_book(book_id)
    if book is None:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Book not found",
                }
            ),
            HTTPStatus.NOT_FOUND,
        )
    return (
        jsonify(
            {
                "success": True,
                "data": book,
            }
        ),
        HTTPStatus.OK,
    )

@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.get_json()
    if not data or not all(key in data for key in ["title", "author", "year"]):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Title, author, and year are required fields.",
                }
            ),
            HTTPStatus.BAD_REQUEST,
        )

    new_book = {
        "id": books[-1]["id"] + 1 if books else 1,
        "title": data["title"],
        "author": data["author"],
        "year": data["year"],
    }
    books.append(new_book)

    return (
        jsonify(
            {
                "success": True,
                "data": new_book,
            }
        ),
        HTTPStatus.CREATED,
    )

@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = find_book(book_id)
    if book is None:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Book not found",
                }
            ),
            HTTPStatus.NOT_FOUND,
        )

    data = request.get_json()
    if not data:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "No data provided",
                }
            ),
            HTTPStatus.BAD_REQUEST,
        )

    book.update({key: data[key] for key in ["title", "author", "year"] if key in data})

    return (
        jsonify(
            {
                "success": True,
                "data": book,
            }
        ),
        HTTPStatus.OK,
    )

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = find_book(book_id)
    if book is None:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Book not found",
                }
            ),
            HTTPStatus.NOT_FOUND,
        )

    books.remove(book)
    return (
        jsonify(
            {
                "success": True,
                "message": f"Book with id {book_id} has been deleted.",
            }
        ),
        HTTPStatus.OK,
    )

if __name__ == "__main__":
    app.run(debug=True)
