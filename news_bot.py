import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, timedelta, timezone

def generate_dashboard():
    # Time handling
    now_utc = datetime.now(timezone.utc)
    now_edt = now_utc - timedelta(hours=4)
    display_now = now_edt.strftime("%B %d, %Y | %I:%M %p")
    
    # Your Verticals
    verticals = [
        "AESA",
        "passive radar",
        "radar technology trends",
        "passive coherent location",
        "Counter-UAS (c-UAS) systems",
        "SIGINT and Electronic Warfare market",
        "Israeli Defense Tech"
    ]
    
    # YOUR NEW TECH RADAR FOCUS
    competitors = ["Hensoldt", "Northrop Grumman", "Elbit Systems", "Selentium Defense"]

    output = []
    output.append("<html><head><title>Strategic Tech Radar</title>")
    output.append("<style>body { font-family: sans-serif; margin: 40px; background: #f0f2f5; }")
    output.append(".container { max-width: 900px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }")
    output.append("h1 { color: #1a237e; border-bottom: 4px solid #1a237e; padding-bottom: 10px; }")
    output.append(".radar-section { background: #fffde7; padding: 15px; border-radius: 8px; border: 1px solid #fbc02d; margin-bottom: 20px; }")
    output.append("h3 { color: #c62828; margin-top: 25px; text-transform: uppercase; font-size: 1.1em; }")
    output.append("li { margin-bottom: 12px; padding: 12px; border-left: 5px solid #1a237e; background: #fafafa; list-style: none; }")
    output.append("a { text-decoration: none; color: #0277bd; font-weight: bold; }</style></head>")
    output.append(f"<body><div class='container'><h1>Director's Tech Radar</h1>")
    output.append(f"<p><strong>Last Updated:</strong> {display_now} EDT</p>")

    # SECTION 1: COMPETITOR PATENT WATCH
    output.append("<div class='radar-section'><h2>🚨 Patent & R&D Watch (Last 24h)</h2>")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    for comp in competitors:
        # Search Google Patents for the assignee + core tech
        patent_query = urllib.parse.quote(f'assignee:"{comp}" radar')
        patent_url = f"https://patents.google.com/?q={patent_query}&sort=new"
        
        output.append(f"<strong>{comp}:</strong> ")
        try:
            res = requests.get(patent_url, headers=headers, timeout=15)
            # Check for recent filings (simplified for this dashboard)
            output.append(f"<a href='{patent_url}' target='_blank'>View Latest IP Filings</a><br>")
        except:
            output.append("Connection to Patent Database timed out.<br>")
    output.append("</div>")

    # SECTION 2: INDUSTRY VERTICALS
    for topic in verticals:
        output.append(f"<h3>{topic}</h3><ul>")
        try:
            query = urllib.parse.quote(f'"{topic}" when:1d')
            rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            response = requests.get(rss_url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all('item')[:4]
            
            if not items:
                output.append("<li>No new tactical updates today.</li>")
            else:
                for item in items:
                    output.append(f"<li><a href='{item.link.text}' target='_blank'>{item.title.text}</a></li>")
        except Exception as e:
            output.append(f"<li>Technical error fetching {topic}.</li>")
        output.append("</ul>")

    output.append("</div></body></html>")
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write("".join(output))

if __name__ == "__main__":
    generate_dashboard()
