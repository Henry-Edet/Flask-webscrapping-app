# Flask-webscrapping-app

# 📬 Flask Web Scraping & Email Scheduler App

A simple but powerful Flask web application that:
- Renders a **Home**, **About**, and **Task** page.
- Allows users to input a URL to **scrape content** from.
- Automatically **emails the scraped content** to group members.
- **Schedules** the scraping task to run **daily at 8:00 AM**.

---

## 📁 Project Structure
flask_app/ │ ├── app.py # Main Flask app with scraping and email logic ├── templates/ # HTML templates │ ├── base.html │ ├── home.html │ ├── about.html │ └── task.html ├── static/ │ ├── style.css # CSS file │ └── images/ # Group member photos ├── scraped_data/ # Folder where scraped content is stored ├── .env # Environment variables (NOT tracked by Git) └── README.md 


---

## 🚀 Features

### 🏠 Home Page
A welcoming landing page styled with CSS.

### 🧑‍🤝‍🧑 About Page
Displays "postcards" for each group member, including:
- Name
- Student ID
- Photo
- Hobbies

### 🧪 Task Page
- Enter a URL (e.g., `https://www.bbc.com`)
- Scrape content from it (paragraphs only)
- Save it to a `.txt` file
- Automatically email it to group members
- Schedule this task to run daily

---

## ⚙️ Setup Instructions

### 1. 🔧 Environment Setup


    # Create virtual environment
    /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -m venv venv
    
    # Activate it
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt

📅 Running the App
➕ Start the Web App


