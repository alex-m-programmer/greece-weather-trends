# 🌦️ Greece Weather Trends: End-to-End ETL & Dashboard

A production-ready data pipeline that extracts weather data for major Greek cities, transforms it using Python, stores it in a Cloud PostgreSQL database, and visualizes trends through an interactive Streamlit dashboard.

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

## 📋 Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.
- A Visual Crossing API Key.
- A PostgreSQL Database (e.g., Render, Neon, or AWS).

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
git clone [https://github.com/your-username/greece-weather-trends.git](https://github.com/alex-m-programmer/greece-weather-trends.git)
cd greece-weather-trends

2. Configure Environment Variables
Create a file named .env in the root directory and add your credentials:
DATABASE_URL=postgresql://user:password@host:port/dbname
WEATHER_API_KEY=your_visual_crossing_api_key

3. Initialize the Database Constraint
To enable the "skip duplicates" logic, run this SQL command in your database console (e.g., pgAdmin or your Cloud DB dashboard). This ensures a city cannot have two entries for the same date:

ALTER TABLE weather_data 
ADD CONSTRAINT city_date_unique UNIQUE (city, datetime);
🐳 Running with Docker
This project uses Docker Compose to run the data gatherer and the dashboard.

Build and start the services:

docker compose up --build
weather_etl: This container will extract the latest data, save it to your cloud DB (or skip if data exists), and then exit.

weather_dashboard: This container will stay running.

View the Dashboard: Open your browser to http://localhost:8501.

📊 Project Structure
├── Dockerfile             # Defines the Python environment
├── docker-compose.yml     # Orchestrates the ETL and Dashboard services
├── requirements.txt       # Python dependencies
├── main.py                # ETL entry point
├── app.py                 # Streamlit dashboard code
├── db.py                  # Database connection & duplicate handling logic
├── api.py                 # API extraction logic with retries
├── transform.py           # Data cleaning and formatting
├── config.py              # Environment variable management
└── logger.py              # Custom logging utility
