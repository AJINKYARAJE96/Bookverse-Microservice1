#  BookVerse - Flask Microservices on AWS

**BookVerse** is an online bookstore application built using Python Flask microservices architecture. Each microservice handles a specific business function and communicates over HTTP. The services are containerized using Docker and deployed using Docker Compose (locally) or ECS (AWS).

---

##  Microservices Overview

| Microservice   | Description                        | Port  |
|----------------|------------------------------------|-------|
| User Service   | Handles user registration & login  | 5001  |
| Book Service   | Manages books and search           | 5002  |
| Order Service  | Manages book orders                | 5003  |
| Payment Service| Simulates payment transactions     | 5004  |
| API Gateway    | Routes requests to respective APIs | 5000  |

---

## 🛠 Tech Stack

- **Backend:** Python (Flask)
- **Databases:** (In-memory for demo, replace with PostgreSQL/MongoDB for prod)
- **Communication:** REST APIs via Flask + `requests`
- **Containerization:** Docker
- **Orchestration (Local):** Docker Compose
- **Cloud:** AWS EC2 / ECS / Fargate
- **Auth:** Basic (JWT can be added)
- **Monitoring (optional):** AWS CloudWatch / Prometheus

---

##  Getting Started

###  Prerequisites

- Docker & Docker Compose installed
- Python 3.8+ (for development)
- AWS CLI configured (for deployment)

###  Running Locally

```bash
# Clone the project
git clone https://github.com/yourusername/bookverse.git
cd bookverse

# Build and run all services
docker-compose up --build
