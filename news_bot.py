import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, timedelta, timezone # Added timezone
import email.utils

def generate_dashboard():
    # Set time for UTC and then convert to EDT (UTC-4)
    now_utc = datetime.now(timezone.utc)
    now_edt = now_utc - timedelta(hours=4)
    display_now = now_edt.strftime("%B %d, %Y | %I:%M %p")
    
    verticals = [
        "AESA", "passive radar", "radar technology trends",
        "Passive radar defense applications", "Counter-UAS (c-UAS) systems",
        "SIGINT and Electronic Warfare market", "Israeli Defense Tech"
    ]
    
    # HTML Header
    html_start = f"""
    <html>
    <head>
        <title>Defense Intel Dashboard</title>
        <style>
            body {{ font-family: sans-serif; margin: 40px; background: #f4f4f9; }}
            .container {{ max-width: 800px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a237e; border-bottom: 2px solid #1a237e; padding-bottom: 10px; }}
            h3 {{ color: #0d47a1; margin-top: 20px; text-transform: uppercase; }}
            li {{ margin-bottom: 10px; padding: 8px; border-left: 4px solid #1a237e; background: #fcfcfc; list-style: none; }}
            a {{ text-decoration: none; color: #333; font-weight: bold; }}
            .timestamp {{ color: #666; font-size: 0.9em; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Intelligence Brief</h1>
            <p class="timestamp">Last Updated: {display_now} EDT</p>
    """

    html_body = ""
    headers = {{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}}

    for topic in verticals:
        html_body += f"<h3>{topic}</h3><ul>"
        try:
            query = urllib.parse.quote(f'"{topic}" when:1d')
            rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            
            response = requests.get(rss_url, headers=headers, timeout=20)
            
            # Using 'html.parser' for maximum compatibility in GitHub Actions
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all('item')
            
            if not items:
                html_body += "<li>No updates in the last 24 hours.</li>"
            else:
                for item in items[:5]:
                    title = item.title.text if item.title else "No Title"
                    link = item.link.text if item.link else "#"
                    html_body += f"<li><a href='{{link}}' target='_blank'>{{title}}</a></li>"
        
        except Exception as e:
            html_body += f"<li>Error fetching this section: {{str(e)}}</li>"
        
        html_body += "</ul>"

    html_end = "</div></body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_start + html_body + html_end)

if __name__ == "__main__":
    generate_dashboard()
