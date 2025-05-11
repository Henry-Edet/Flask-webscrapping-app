from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import time
import schedule
from dotenv import load_dotenv

#email setup
import smtplib
from email.message import EmailMessage

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY') # Needed for flashing messages

# Dummy group members for the About page
GROUP_MEMBERS = [
    {
        "name": "David Michael",
        "student_id": "123456",
        "image": "david.jpg",
        "hobbies": "Only God Knows, Doesn't need a phone"
    },
    {
        "name": "Ada Lovelace",
        "student_id": "789012",
        "image": "ada.jpg",
        "hobbies": "Mathematics, inventing"
    }
]

# Email settings
GROUP_EMAILS = ['avidmichael615@gmail.com', 'gracemichael02@gmail.com']
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Store last submitted URL for scheduling
last_submitted_url = None


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', members=GROUP_MEMBERS)


@app.route('/task', methods=['GET', 'POST'])
def task():
    global last_submitted_url
    if request.method == 'POST':
        url = request.form.get('url')

        if not url:
            flash("Please enter a valid URL.")
            return redirect(url_for('task'))

        try:
            last_submitted_url = url
            scrape_and_email(url)         # Immediate scrape & email
            schedule_daily_scraping()     # Schedule daily scraping
            flash("Data scraped, emailed, and scheduled to repeat daily at 8:00 AM!")
        except Exception as e:
            flash(f"An error occurred: {e}")

        return redirect(url_for('task'))

    return render_template('task.html')


def scrape_and_email(url):
    # Fetch and scrape the site
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract meaningful text from the page (simplified)
    content = '\n'.join([p.get_text() for p in soup.find_all('p') if p.get_text().strip()])

    # Save to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'scraped_data/data_{timestamp}.txt'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    # Send email
    send_email_with_attachment(filename, content)


def send_email_with_attachment(file_path, body):
    msg = EmailMessage()
    msg['Subject'] = 'Scraped Web Data'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(GROUP_EMAILS)
    msg.set_content("See attached file for the latest scraped content.")

    # Attach file
    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(file_path)
        msg.add_attachment(file_data, maintype='text', subtype='plain', filename=file_name)

    # Send
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


# -------------------- Scheduler Logic --------------------

def schedule_daily_scraping():
    schedule.clear()  # Clear previous jobs
    if last_submitted_url:
        schedule.every().day.at("08:00").do(scrape_and_email, last_submitted_url)
        print(f"[Scheduled] Scraping for {last_submitted_url} at 08:00 daily.")



def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


# -------------------- Start Scheduler Thread --------------------

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()


if __name__ == '__main__':
    app.run(debug=True)
