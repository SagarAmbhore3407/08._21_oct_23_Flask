
#9. Create a RESTful API using Flask to perform CRUD operations on resources like books or movies.

from flask import Flask, request,jsonify
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('books.db')
curr = conn.cursor()

curr.execute('''CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL
    )''')

conn.commit()

#Get all books
@app.route('/books', methods=['GET'])
def get_books():
    conn = sqlite3.connect('books.db')
    curr = conn.cursor()
    curr.execute('SELECT * FROM books')
    
    rows = curr.fetchall()
    conn.close()
    booksLst = []
    
    for row in rows:
        book = {
            'id':row[0],
            'title':row[1],
            'author':row[2],
        }
        booksLst.append(book)
        
    return jsonify(booksLst)   


#Get a specific book
@app.route('/books/<int:book_id>',methods = ['GET'])
def get_book(book_id):
    conn = sqlite3.connect('books.db')
    curr = conn.cursor()
    curr.execute('''SELECT * FROM books WHERE id = ?''',(book_id,))
    book = curr.fetchone()
    if book:
        book = {
            'Book_id':book[0],
            'Title':book[1],
            'Author':book[2]
        }
        return jsonify(book)
    return jsonify({'error':'Book is not available associated with given id..'}),404
        

 
#Add or Create a new book       
@app.route('/books', methods=['POST'])
def create_book():
    new_book = request.get_json()
    title = new_book.get('title')
    author = new_book.get('author')
    
    if title and author:
        conn = sqlite3.connect('books.db')
        curr = conn.cursor()
        curr.execute('''
                     INSERT INTO books ('title','author') VALUES(?,?)''',(title,author))
        conn.commit()
        curr.execute('''SELECT * FROM books''')
        rows = curr.fetchall()
        book_id = len(rows)
        created_book={
            'book_id': book_id,
            'title' : title,
            'author' : author
        }
        return created_book,201
    return jsonify({'error':'Invalid data'}),400
        

#Update books
@app.route('/books/<int:book_id>',methods=['PUT'])
def update_book(book_id):
    book = request.get_json()
    title = book.get('title')
    author = book.get('author')
    
    if title or author:
        conn = sqlite3.connect('books.db')
        curr = conn.cursor()
        curr.execute('''SELECT * FROM books WHERE id = ?''',(book_id,))
        book = curr.fetchone()
        
        if book:
            if title:
                curr.execute('''UPDATE books SET title = ? WHERE id = ?''',(title,book_id))
            if author:
                curr.execute('''UPDATE books SET author = ? WHERE id = ?''',(author,book_id))
            conn.commit()
            updated_book = {
                'id':book_id,
                'Title':title if title else book[1],
                'Author':author if author else book[2]
            }
            return jsonify(updated_book)        
            
        return jsonify({'error':'Book is not available associated with given id..'}),404      
    return jsonify({'error':'No data provoded for update..provide a data..'}),404  
        
        
#Delete a specific book
@app.route("/books/<int:book_id>",methods = ['DELETE'])
def delete_book(book_id):
    conn = sqlite3.connect('books.db')
    curr = conn.cursor()
    curr.execute('''SELECT * FROM books WHERE id=?''',(book_id,))
    book = curr.fetchone()
    if book:
        curr.execute('''DELETE FROM books WHERE id=?''',(book_id,))
        conn.commit()
        return jsonify({'message':f'book deleted with id {book_id}'})
        
    return jsonify({'error':'Book is not available associated with given id..'}),404     

#DELETE all books from database
@app.route('/books',methods = ['DELETE'])
def delete_all():
    conn = sqlite3.connect('books.db')
    curr = conn.cursor()
    curr.execute('''SELECT * FROM books''')
    record = curr.fetchone()
    if record:             
        curr.execute('''DELETE FROM books''')
        conn.commit()
        return jsonify({'message':'All Books has been deleted.'})
    return jsonify({'message':'The books table is Already Empty..'})
    
    
if __name__ == '__main__':
    app.run(debug=True)