# 💊 Medicine Price Comparison System

## 📌 Overview
The Medicine Price Comparison System is a web-based application developed using Django that helps users compare medicine prices across multiple online pharmacy platforms. It enables users to find the most affordable option and save money by providing real-time price comparisons.

## 🚀 Features
- 🔍 Search for medicines by name  
- 🌐 Fetch real-time prices from multiple pharmacy websites  
- 💰 Identify the lowest price among platforms  
- 📊 Calculate and display savings percentage  
- 🖥️ Simple and user-friendly interface  

## 🛠️ Tech Stack
- Backend: Python (Django)  
- Database: SQLite
- Frontend: HTML, CSS, JavaScript  
- Web Scraping: SeleniumBase  

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd Medicine-Price-Comparison
````

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

### 6. Open in browser

```
http://127.0.0.1:8000/
```

## 📊 How It Works

1. User enters a medicine name
2. System scrapes data from multiple pharmacy websites
3. Prices are compared and processed
4. The lowest price and savings percentage are displayed

## 🎯 Purpose

The main goal of this project is to help users make cost-effective decisions by comparing medicine prices across different platforms in real time.

## 📌 Future Improvements

* Add more pharmacy platforms
* Improve scraping speed and accuracy
* Add user authentication
* Save search history

## 👨‍💻 Author

**Darshan Kaladiya**
