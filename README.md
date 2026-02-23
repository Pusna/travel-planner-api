# Travel Planner API 🌍

A backend service for planning trips to Chicago, integrated with the Art Institute of Chicago API for location validation.

---

## 🛠 Tech Stack
* **Python** / **FastAPI**
* **PostgreSQL** / **SQLAlchemy 2.0 (Async)**
* **Docker** & **Docker Compose**
* **Pydantic v2**

---

## 📁 Project Structure
```text
├── app/
│   ├── routers/          # API endpoints (projects, places)
│   ├── api_chicago.py    # Chicago Art API integration
│   ├── crud.py           # Business logic & DB operations
│   ├── database.py       # Database connection setup
│   ├── main.py           # Application entry point
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic validation schemas
│   └── settings.py       # Environment configuration
├── .env.example          # Environment variables template
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Services orchestration
└── requirements.txt      # Project dependencies
```

---

## 🚀 How to Run
### 1. Prepare Environment
Copy the example environment file to create your active `.env`:
```bash
cp .env.example .env
```

### 2. Launch Application
Build and start the containers:

```bash
docker-compose up --build
```

## 📖 API Testing
Swagger UI: http://localhost:8000/docs — Use this to test all endpoints.

Postman: Import the travel_planner.postman_collection.json file from the root folder for automated test flows.

## ⚙️ Key Requirements Met
Validation: All places are verified via the Art Institute of Chicago API.

Constraints: Enforced limit of max 10 places per project.

Auto-Status: Projects are automatically marked as completed when all places are visited.

Data Integrity: Unique constraint prevents duplicate places in the same project.

Protection: Projects with visited places cannot be deleted.