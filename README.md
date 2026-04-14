# 🌦️ Greece Weather Trends: End-to-End ETL & Dashboard

A production-ready data pipeline that extracts weather data for major Greek cities, transforms it using Python, stores it in a Cloud PostgreSQL database, and visualizes trends through an interactive Streamlit dashboard.
**🔗 [View Live Dashboard](https://greece-weather-trends-qqb5pxmz2gqjcgtccedds8.streamlit.app/)**
---

## 🚀 Features
- **Automated ETL**: Python-based extraction from Visual Crossing API with built-in retry logic using `tenacity`.
- **Data Integrity**: Database-level `UNIQUE` constraints combined with Python exception handling to prevent duplicate records (Idempotency).
- **Containerized Architecture**: Multi-container setup using **Docker Compose** for seamless environment replication.
- **Interactive Dashboard**: Real-time visualization of temperature, humidity, and weather trends using **Streamlit**.
- **Resilient Logging**: Centralized logging to track pipeline performance and ingestion status.

---

## 🛠️ Tech Stack
- **Language:** Python 3.11
- **Orchestration:** Docker & Docker Compose
- **Database:** PostgreSQL (Cloud Managed)
- **Libraries:** Pandas, SQLAlchemy, Streamlit, Requests, Tenacity
- **API:** Visual Crossing Weather API

---

## 🤖 Automation Details
This project is fully autonomous. A GitHub Action workflow (`daily_etl.yml`) triggers every morning to:
1. Spin up a Python environment.
2. Connect to the Visual Crossing API.
3. Clean and validate data via `transform.py`.
4. Upsert data into the PostgreSQL database.

---

## 📋 Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.
- A Visual Crossing API Key.
- A PostgreSQL Database (e.g., Render, Neon, or AWS).

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/alex-m-programmer/greece-weather-trends.git](https://github.com/your-username/greece-weather-trends.git)
cd greece-weather-trends
```

### 2. Configure Environment Variables
Create a file named .env in the root directory. This file is ignored by Git to keep your credentials secure:
```bash
DATABASE_URL=postgresql://user:password@host:port/dbname
WEATHER_API_KEY=your_visual_crossing_api_key
```

### 3. Initialize the Database Constraint
To ensure the pipeline handles repeated runs gracefully, run this SQL command in your database console. This creates a rule that prevents the same city from having two entries for the same date:

```bash
ALTER TABLE weather_data 
ADD CONSTRAINT city_date_unique UNIQUE (city, datetime);
```

🐳 This project uses Docker Compose to manage the ETL script and the Dashboard as separate services.

Build and start all services:

```Bash
docker compose up --build
```
weather_etl: Wakes up, extracts data, saves it to the database (skipping duplicates), and then shuts down.

weather_dashboard: Remains active. View it at http://localhost:8501.

```bash
📊 Project Structure
├── Dockerfile             # Shared image definition for ETL and Dashboard
├── docker-compose.yml     # Service orchestration (ETL & Dashboard)
├── requirements.txt       # Python dependencies
├── main.py                # ETL entry point and orchestration
├── app.py                 # Streamlit dashboard UI
├── db.py                  # Database connection & integrity logic
├── api.py                 # API extraction logic with retry decorators
├── transform.py           # Data cleaning & Pandas transformation
├── config.py              # Environment variable management
└── logger.py              # Custom logging utility
```
