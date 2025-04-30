# BookVerse Microservices - Flask + Docker + AWS Ready

# Each microservice will be in its own folder with a Dockerfile.
# This is a simplified structure and starter code.

# ------------------------------------------
# user_service/app.py
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

users = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user_id = str(uuid.uuid4())
    users[user_id] = {
        "username": data['username'],
        "password": data['password']  # Not secure, use hashing in prod
    }
    return jsonify({"user_id": user_id}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    for uid, user in users.items():
        if user['username'] == data['username'] and user['password'] == data['password']:
            return jsonify({"message": "Login successful", "user_id": uid})
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

# ------------------------------------------
# book_service/app.py
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

books = {}

@app.route('/books', methods=['GET'])
def list_books():
    return jsonify(list(books.values()))

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    book_id = str(uuid.uuid4())
    books[book_id] = {"id": book_id, "title": data['title'], "author": data['author']}
    return jsonify(books[book_id]), 201

@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    return jsonify(books.get(book_id, {}))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

# ------------------------------------------
# order_service/app.py
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

orders = {}

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    order_id = str(uuid.uuid4())
    orders[order_id] = {"id": order_id, "user_id": data['user_id'], "book_id": data['book_id']}
    return jsonify(orders[order_id]), 201

@app.route('/orders/<user_id>', methods=['GET'])
def user_orders(user_id):
    result = [order for order in orders.values() if order['user_id'] == user_id]
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

# ------------------------------------------
# payment_service/app.py
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

payments = {}

@app.route('/payment', methods=['POST'])
def make_payment():
    data = request.json
    payment_id = str(uuid.uuid4())
    payments[payment_id] = {"id": payment_id, "order_id": data['order_id'], "amount": data['amount']}
    return jsonify(payments[payment_id]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)

# ------------------------------------------
# api_gateway/app.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/gateway/<service>/<path:endpoint>', methods=["GET", "POST"])
def gateway(service, endpoint):
    services = {
        "user": "http://user_service:5001",
        "book": "http://book_service:5002",
        "order": "http://order_service:5003",
        "payment": "http://payment_service:5004"
    }
    url = f"{services[service]}/{endpoint}"
    if request.method == "GET":
        resp = requests.get(url, params=request.args)
    else:
        resp = requests.post(url, json=request.json)
    return (resp.content, resp.status_code, resp.headers.items())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# ------------------------------------------
# docker-compose.yml
version: '3'
services:
  user_service:
    build: ./user_service
    ports:
      - "5001:5001"
  book_service:
    build: ./book_service
    ports:
      - "5002:5002"
  order_service:
    build: ./order_service
    ports:
      - "5003:5003"
  payment_service:
    build: ./payment_service
    ports:
      - "5004:5004"
  api_gateway:
    build: ./api_gateway
    ports:
      - "5000:5000"
    depends_on:
      - user_service
      - book_service
      - order_service
      - payment_service
