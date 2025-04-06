# Multi-Platform E-commerce Analytics Benchmarking Pipeline

A scalable data extraction and benchmarking system for e-commerce platforms, designed for real-time analytics and model evaluation.

## 🚀 Features
- Collects 5,000+ data points using Selenium automation.
- Full-stack web architecture (FastAPI backend).
- Benchmarks performance of multi-threaded data pipelines.

## 📊 Benchmark Goals
- Measure performance of scraping and API endpoints.
- Automate large-scale data collection for ML tasks.
- Ensure fault tolerance, reproducibility, and deployment stability.

## 🛠️ Tech Stack
- Python, FastAPI, Selenium
- PostgreSQL, Docker
- Threading, Logging, RESTful APIs

## 📁 Structure
- `/backend`: API and data pipelines
- `/scrapers`: Selenium automation scripts
- `/utils`: Error handling, logs, and data parsers

## 📌 Reproducibility
Install requirements via `pip install -r requirements.txt`.  
Start backend server using `uvicorn main:app --reload`.  
Run scrapers using `python scrapers/run_all.py`.

## 📈 Sample Output
- 4x faster data extraction compared to baseline
- Scalable backend architecture for high-volume tasks
