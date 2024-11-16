import pytest
from app import app
import mysql.connector
from config import DB_CONFIG

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_database():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("DROP DATABASE IF EXISTS library")
    cursor.execute("CREATE DATABASE library") 
    cursor.execute("USE library")  

    cursor.execute(""" 
        CREATE TABLE books (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255),
            author VARCHAR(255),
            year INT
        )
    """)

    cursor.execute("INSERT INTO books (title, author, year) VALUES ('Philosopher''s Stone', 'J. K. Rowling', 1997)")
    cursor.execute("INSERT INTO books (title, author, year) VALUES ('Chamber of Secrets', 'J. K. Rowling', 1998)")
    cursor.execute("INSERT INTO books (title, author, year) VALUES ('Prisoner of Azkaban', 'J. K. Rowling', 1999)")
    cursor.execute("INSERT INTO books (title, author, year) VALUES ('Goblet of Fire', 'J. K. Rowling', 2000)")
    cursor.execute("INSERT INTO books (title, author, year) VALUES ('Order of the Phoenix', 'J. K. Rowling', 2003)")
    cursor.execute("INSERT INTO books (title, author, year) VALUES ('Half-Blood Prince', 'J. K. Rowling', 2005)")
    cursor.execute("INSERT INTO books (title, author, year) VALUES ('Deathly Hallows', 'J. K. Rowling', 2007)")
    conn.commit()
    cursor.close()
    conn.close()

def test_get_books(client):
    response = client.get("/api/books")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert len(data["data"]) == 7

def test_get_book(client):
    response = client.get("/api/books/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["title"] == "Philosopher's Stone"

def test_get_book_not_found(client):
    response = client.get("/api/books/999")
    assert response.status_code == 404

def test_update_book(client):
    response = client.put("/api/books/1", json={"title": "Updated Title", "author": "Updated Author", "year": 2000})
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    get_response = client.get("/api/books/1")
    get_data = get_response.get_json()
    assert get_data["data"]["title"] == "Updated Title"

def test_delete_book(client):
    response = client.delete("/api/books/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    get_response = client.get("/api/books/1")
    assert get_response.status_code == 404

def test_delete_book_not_found(client):
    response = client.delete("/api/books/999")
    assert response.status_code == 404
