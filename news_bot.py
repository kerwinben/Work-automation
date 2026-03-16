import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, timedelta, timezone

def generate_dashboard():
    # Time handling
    now_utc = datetime.now(timezone.utc)
    now_edt = now_utc - timedelta(hours=4)
    display_now = now_edt.strftime("%B %d, %Y | %I:%M %p")
    
    verticals = [
        "AESA", "passive radar", "radar technology trends",
        "Passive radar defense applications", "Counter-UAS (c-UAS) systems",
        "SIGINT and Electronic Warfare market", "Israeli Defense Tech"
    ]
    
    # Using a list and .join() is much safer than f-strings for large HTML
    output = []
    output.append("<html><head><title>Defense Intel Hub</title>")
    output.append("<style>body { font-family: sans-serif; margin: 40px; background: #f4f4f9; }")
    output.append(".container { max-width: 800px; margin: auto; background: white; padding: 25px; border-radius: 8px; }")
    output.append("h1 { color: #1a237e; border-bottom: 2px solid #1a237e; }")
    output.append("h3 { color: #0d47a1; margin-top: 20px; text-transform: uppercase; }")
    output.append("li { margin-bottom: 10px; padding: 8px; border-left: 4px solid #1a237e; background: #fcfcfc; list-style: none; }")
    output.append("a { text-decoration: none; color: #333; font-weight: bold; }</style></head>")
    output.append(f"<body><div class='container'><h1>Intelligence Brief</h1>")
    output.append(f"<p>Last Updated: {display_now} EDT</p>")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    for topic in verticals:
        output.append(f"<h3>{topic}</h3><ul>")
        try:
            query = urllib.parse.quote(f'"{topic}" when:1d')
            rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            response = requests.get(rss_url, headers=headers, timeout=20)
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all('item')
            
            if not items:
                output.append("<li>No updates in the last 24 hours.</li>")
            else:
                for item in items[:5]:
                    t = item.title.text if item.title else "No Title"
                    l = item.link.text if item.link else "#"
                    output.append(f"<li><a href='{l}' target='_blank'>{t}</a></li>")
        except Exception as e:
            output.append(f"<li>Error: {str(e)}</li>")
        output.append("</ul>")

    output.append("</div></body></html>")
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write("".join(output))

if __name__ == "__main__":
    generate_dashboard()
