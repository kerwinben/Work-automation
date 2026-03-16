import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, timedelta

def generate_dashboard():
    # Set time for EDT (UTC-4)
    now_utc = datetime.now(timedelta(0))
    display_now = (now_utc - timedelta(hours=4)).strftime("%B %d, %Y | %I:%M %p")
    
    verticals = [
        "AESA", "passive radar", "radar technology trends",
        "Passive radar defense applications", "Counter-UAS (c-UAS) systems",
        "SIGINT and Electronic Warfare market", "Israeli Defense Tech"
    ]
    
    # We use double {{ }} for CSS so Python f-string ignores them
    html_start = f"""
    <html>
    <head>
        <title>Defense Intelligence Dashboard</title>
        <style>
            body {{ font-family: sans-serif; margin: 40px; background: #f4f4f9; }}
            .container {{ max-width: 800px; margin: auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a237e; border-bottom: 2px solid #1a237e; padding-bottom: 10px; }}
            .timestamp {{ color: #666; margin-bottom: 20px; font-size: 0.9em; }}
            h3 {{ color: #0d47a1; margin-top: 25px; text-transform: uppercase; font-size: 1em; }}
            li {{ margin-bottom: 12px; padding: 10px; border-left: 4px solid #1a237e; background: #fcfcfc; }}
            a {{ text-decoration: none; color: #333; font-weight: bold; }}
            a:hover {{ color: #1a237e; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Intelligence Brief</h1>
            <div class="timestamp">Last Updated: {display_now} EDT</div>
    """

    html_body = ""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    for topic in verticals:
        encoded_topic = urllib.parse.quote(f'"{topic}" when:1d')
        rss_url = f"https://news.google.com/rss/search?q={encoded_topic}&hl=en-US&gl=US&ceid=US:en"
        
        try:
            response = requests.get(rss_url, headers=headers, timeout=15)
            # Use 'xml' parser to handle RSS properly
            soup = BeautifulSoup(response.content, "xml")
            
            html_body += f"<h3>{topic}</h3><ul>"
            items = soup.find_all('item')[:5]
            
            if not items:
                html_body += "<li>No new updates in the last 24 hours.</li>"
            else:
                for item in items:
                    title = item.title.text
                    link = item.link.text
                    html_body += f"<li><a href='{link}' target='_blank'>{title}</a></li>"
            html_body += "</ul>"
        except Exception as e:
            print(f"Error fetching {topic}: {e}")
            continue

    html_end = "</div></body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_start + html_body + html_end)

if __name__ == "__main__":
    generate_dashboard()
