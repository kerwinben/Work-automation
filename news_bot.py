import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, timedelta  # <--- Added this

def generate_dashboard():
    # Get current date and time
    # Subtract 4 hours from UTC to get Eastern Daylight Time (EDT)
    now_utc = datetime.utcnow()
    now_edt = now_utc - timedelta(hours=4)
    now = now_edt.strftime("%B %d, %Y | %I:%M %p")
    
    verticals = [
        "AESA", 
        "passive radar",
        "radar technology trends",
        "Passive radar defense applications",
        "Counter-UAS (c-UAS) systems",
        "SIGINT and Electronic Warfare market",
        "Israeli Defense Tech"
    ]
    
    html_content = f"""
    <html>
    <head>
        <title>Defense Intelligence Dashboard</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 40px; background: #f4f4f9; }}
            .container {{ max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a2a6c; border-bottom: 2px solid #0056b3; padding-bottom: 10px; margin-bottom: 5px; }}
            .timestamp {{ color: #666; font-size: 0.9em; margin-bottom: 20px; }}
            h3 {{ color: #0056b3; margin-top: 25px; text-transform: uppercase; font-size: 1.1em; }}
            ul {{ list-style: none; padding: 0; }}
            li {{ margin-bottom: 12px; padding: 12px; border-left: 4px solid #0056b3; background: #fafafa; border-radius: 0 4px 4px 0; }}
            a {{ text-decoration: none; color: #333; font-weight: bold; line-height: 1.4; display: block; }}
            a:hover {{ color: #0056b3; }}
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
        
        html_content += f"<h3>{topic}</h3><ul>"
        items = soup.find_all('item')
        if not items:
            html_content += "<li>No new updates for this category today.</li>"
        for item in items[:5]:
            html_content += f"<li><a href='{item.link.text}' target='_blank'>{item.title.text}</a></li>"
        html_content += "</ul>"

    html_content += "</div></body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_dashboard()
