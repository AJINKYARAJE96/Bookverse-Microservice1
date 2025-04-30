 Code Structure & Explanation
 /user_service/app.py
Handles user registration and login.

POST /register: Creates a new user (stores username & password in-memory).

POST /login: Authenticates a user.

Uses a dictionary users to simulate a user database.

Each user is assigned a unique UUID.

 In production, store passwords securely (use bcrypt) and persist data in a real database.

/book_service/app.py
Manages books and book search.

GET /books: Returns a list of all books.

POST /books: Adds a new book (title and author required).

GET /books/<book_id>: Fetches a specific book by ID.

Stores book data in a dictionary books.

 Ideal to back with MongoDB or PostgreSQL in production.
 /order_service/app.py
Handles user orders (book purchases).

POST /order: Places an order with user_id and book_id.

GET /orders/<user_id>: Returns all orders placed by a specific user.

Uses a dictionary orders to store data.

🛒 You can enrich this to check book stock, order status, etc.

 /payment_service/app.py
Simulates processing payments.

POST /payment: Accepts order_id and amount, creates a payment entry.

Stores data in a dictionary payments.

 In real-world apps, integrate with Stripe or Razorpay APIs.

 /api_gateway/app.py
Acts as a single entry point to route requests to appropriate microservices.

URL format: /gateway/<service>/<endpoint>

Maps logical service names to their internal container addresses like:

user → http://user_service:5001

book → http://book_service:5002

Forwards the incoming request (GET or POST) to the actual service and returns its response.

 This pattern simulates how an API Gateway works in cloud platforms like AWS API Gateway.

 docker-compose.yml
Defines and runs all microservices together locally.

Each service is declared with its build path and port.

Enables you to run everything using a single command:

bash
Copy
Edit
docker-compose up --build
 Docker Compose networks services automatically, e.g., user_service becomes reachable from other containers.

🔧 Dockerfile (per service)
Each folder (e.g., user_service/) should have a Dockerfile like this:

Dockerfile
Copy
Edit
FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install flask requests
EXPOSE 5001  # Change port per service
CMD ["python", "app.py"]
Change the EXPOSE port and final CMD according to each microservice
