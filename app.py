from bson import ObjectId
from bson.errors import InvalidId
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://pineapple:aWU8ztWJpMUakEscOLItkXYzhKnXdvqRknbIzqUymFNew"
                     "0ZACmfhbR3XhJxdxtl65rKv3EjgAIerACDbOq7oAA"
                     "=@pineapple.mongo.cosmos.azure.com:10255/?ss"
                     "l=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=1200"
                     "00&appName=@pineapple@")
db = client["PineappleDB"]
collection = db["bookstore"]

# Create
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    required_fields = ['isbn', 'title', 'year', 'price', 'page', 'category', 'coverPhoto', 'publisher', 'author']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'All required fields must be present in the request body'}), 400

    try:
        result = collection.insert_one(data)
        return jsonify({'message': 'Book created successfully', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating book: {str(e)}'}), 500

# GetAll
@app.route('/books', methods=['GET'])
def get_all_books():
    books = []
    for book in collection.find():
        books.append(format_book(book))
    return jsonify({'books': books})

# GetById
@app.route('/books/<string:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    try:
        obj_id = ObjectId(book_id)
    except InvalidId:
        return jsonify({'message': 'Invalid book ID format'}), 400

    book = collection.find_one({'_id': obj_id})

    if book:
        return jsonify(format_book(book)), 200
    else:
        return jsonify({'message': 'Book not found'}), 404

# Delete
@app.route('/books/<string:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        obj_id = ObjectId(book_id)
    except InvalidId:
        return jsonify({'message': 'Invalid book ID format'}), 400

    result = collection.delete_one({'_id': obj_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Book deleted successfully'}), 200
    else:
        return jsonify({'message': 'Book not found'}), 404

# UpdateOne
@app.route('/books/<string:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        obj_id = ObjectId(book_id)
    except InvalidId:
        return jsonify({'message': 'Invalid book ID format'}), 400

    data = request.get_json()

    required_fields = ['isbn', 'title', 'year', 'price', 'page', 'category', 'coverPhoto', 'publisher', 'author']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'All required fields must be present in the request body'}), 400

    try:
        result = collection.replace_one({'_id': obj_id}, data)
        if result.modified_count > 0:
            return jsonify({'message': 'Book updated successfully'}), 200
        else:
            return jsonify({'message': 'Book not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error updating book: {str(e)}'}), 500

# UpdatePrice
@app.route('/books/<string:book_id>/update_price', methods=['PATCH'])
def update_book_price(book_id):
    try:
        obj_id = ObjectId(book_id)
    except InvalidId:
        return jsonify({'message': 'Invalid book ID format'}), 400

    price_param = request.args.get('price')

    if not price_param:
        return jsonify({'message': 'Price parameter is required for the update'}), 400

    try:
        price = float(price_param)
    except ValueError:
        return jsonify({'message': 'Invalid price format'}), 400

    result = collection.update_one({'_id': obj_id}, {'$set': {'price': price}})

    if result.modified_count > 0:
        return jsonify({'message': 'Book price updated successfully'}), 200
    else:
        return jsonify({'message': 'Book not found'}), 404

# Helper function to format book data
def format_book(book):
    formatted_book = {
        'id': str(book['_id']),
        'isbn': book['isbn'],
        'title': book['title'],
        'year': book['year'],
        'price': book['price'],
        'page': book['page'],
        'category': book['category'],
        'coverPhoto': book['coverPhoto'],
        'publisher': book['publisher'],
        'author': book['author']
    }
    return formatted_book

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
