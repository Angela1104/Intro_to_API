from flask import Flask, jsonify
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

@app.route("/api/books", methods=["GET"])
def get_books():
    return jsonify({"success": True, "data": books, "total": len(books)}), HTTPStatus.OK

if __name__ == "__main__":
    app.run(debug=True)
