import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime

def generate_dashboard():
    now = datetime.now().strftime("%B %d, %Y | %I:%M %p") # e.g., March 16, 2026 | 02:20 PM
    
    verticals = [
        "AESA", 
        "passive radar",
        "radar technology trends",
        "Passive radar defense applications",
        "Counter-UAS (c-UAS) systems",
        "SIGINT and Electronic Warfare market",
        "Israeli Defense Tech"
    ]
    
    # Start of the HTML file with some basic styling
    html_content = f"""
    <html>
    <head>
        <title>Defense Intelligence Dashboard</title>
        <style>
            body { font-family: sans-serif; margin: 40px; background: #f4f4f9; }
            .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; border-bottom: 2px solid #0056b3; padding-bottom: 10px; }
            h3 { color: #0056b3; margin-top: 25px; }
            ul { list-style: none; padding: 0; }
            li { margin-bottom: 10px; padding: 10px; border-left: 4px solid #0056b3; background: #fafafa; }
            a { text-decoration: none; color: #333; font-weight: bold; }
            a:hover { color: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Intelligence Brief: Radars, c-UAS & SIGINT</h1>
            <div class="timestamp">Last Updated: {now} (Eastern Time)</div>
    """

    for topic in verticals:
        encoded_topic = urllib.parse.quote(topic)
        rss_url = f"https://news.google.com/rss/search?q={encoded_topic}&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(rss_url)
        soup = BeautifulSoup(response.content, features="xml")
        
        html_content += f"<h3>{topic.upper()}</h3><ul>"
        for item in soup.find_all('item')[:5]: # Top 5 articles
            html_content += f"<li><a href='{item.link.text}' target='_blank'>{item.title.text}</a></li>"
        html_content += "</ul>"

    html_content += "</div></body></html>"
    
    # Save to a file
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_dashboard()
