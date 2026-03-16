import requests
from bs4 import BeautifulSoup
import urllib.parse
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_news():
    verticals = [
        "AESA", 
        "passive radar",
        "radar technology trends",
        "Passive radar defense applications",
        "Counter-UAS (c-UAS) systems",
        "SIGINT and Electronic Warfare market",
        "Israeli Defense Tech"
    ]
    
    for topic in verticals:
        encoded_topic = urllib.parse.quote(topic)
        rss_url = f"https://news.google.com/rss/search?q={encoded_topic}&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(rss_url)
        soup = BeautifulSoup(response.content, features="xml")
        
        report += f"<h3>{topic.upper()}</h3><ul>"
        for item in soup.find_all('item')[:3]:
            report += f"<li><a href='{item.link.text}'>{item.title.text}</a></li>"
        report += "</ul>"
    return report

def send_email(content):
    sender_email = os.environ.get("SENDER_EMAIL")
    receiver_email = os.environ.get("RECEIVER_EMAIL")
    password = os.environ.get("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Morning Market Intelligence Brief"

    msg.attach(MIMEText(content, 'html'))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

if __name__ == "__main__":
    news_content = get_news()
    send_email(news_content)
    print("Email sent successfully.")