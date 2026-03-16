import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, timedelta
import email.utils
import random

def generate_dashboard():
    # 1. TIME SETUP
    now_utc = datetime.now(timedelta(0))
    time_threshold = now_utc - timedelta(hours=24)
    display_now = (now_utc - timedelta(hours=4)).strftime("%B %d, %Y | %I:%M %p")

    # 2. SECTOR & COMPETITOR DATA
    verticals = [
        "AESA radar", "passive radar", "radar technology trends",
        "Counter-UAS c-UAS systems", "SIGINT Electronic Warfare market",
        "Israeli Defense Tech", "ELTA Systems IAI"
    ]
    competitors = ["Hensoldt", "Northrop Grumman", "L3Harris", "Lockheed Martin Radar"]
    
    # 3. STOCK TICKERS (Visual placeholders for now)
    stocks = {"LMT": "Lockheed", "NOC": "Northrop", "LHX": "L3Harris", "ESLT": "Elbit"}

    # 4. INTELLIGENCE GLOSSARY
    glossary = {
        "PEO IEW&S": "Program Executive Office Intelligence, Electronic Warfare and Sensors.",
        "AESA": "Active Electronically Scanned Array - high-bandwidth, multi-target radar.",
        "COMINT": "Communications Intelligence - intercepting foreign communications.",
        "MASINT": "Measurement and Signature Intelligence - distinct technical data (heat, sound).",
        "c-UAS": "Counter-Unmanned Aircraft Systems - detection and neutralization of drones."
    }
    acronym, definition = random.choice(list(glossary.items()))

    # 5. HTML START
    html_content = f"""
    <html>
    <head>
        <title>Director's Intel Hub</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; margin: 0; background: #eceff1; color: #333; }}
            .sidebar {{ width: 250px; position: fixed; height: 100%; background: #1a237e; color: white; padding: 20px; }}
            .main {{ margin-left: 290px; padding: 40px; max-width: 900px; }}
            .card {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a237e; border-bottom: 3px solid #1a237e; padding-bottom: 10px; }}
            h3 {{ color: #d32f2f; border-left: 5px solid #d32f2f; padding-left: 10px; margin-top: 30px; }}
            .stock-box {{ background: #263238; color: #81c784; padding: 10px; border-radius: 4px; margin-bottom: 10px; font-family: monospace; font-size: 0.8em; }}
            .acronym {{ background: #fff9c4; padding: 15px; border-radius: 8px; border: 1px solid #fbc02d; color: #333; }}
            li {{ margin-bottom: 10px; }}
            a {{ text-decoration: none; color: #0277bd; font-weight: 600; }}
            .date {{ font-size: 0.8em; color: #777; }}
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>Market Watch</h2>
            {"".join([f'<div class="stock-box">{t}: MONITORING</div>' for t in stocks.keys()])}
            <hr>
            <div class="acronym">
                <strong>Intel Term: {acronym}</strong><br>
                <small>{definition}</small>
            </div>
        </div>
        <div class="main">
            <div class="card">
                <h1>Director's Intelligence Hub</h1>
                <p><strong>Last Updated:</strong> {display_now} EDT</p>
                <p><i>Real-time monitoring of AESA, SIGINT, and Israeli Defense Tech.</i></p>
            </div>
    """

    # 6. FETCH NEWS
    for topic in (verticals + competitors):
        query = urllib.parse.quote(f'"{topic}" when:1d')
        rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        
        try:
            # Added a 10 second timeout and error checking
            response = requests.get(rss_url, timeout=10)
            response.raise_for_status() 
            
            # Using 'html.parser' instead of 'xml' to reduce dependency errors
            soup = BeautifulSoup(response.content, "html.parser")
            
            html_content += f"<h3>{topic.upper()}</h3><ul>"
            items = soup.find_all('item')[:3]
            
            if not items:
                html_content += "<li>No new updates in the last 24 hours.</li>"
            else:
                for item in items:
                    title = item.title.text if item.title else "No Title"
                    link = item.link.text if item.link else "#"
                    html_content += f"<li><a href='{link}' target='_blank'>{title}</a></li>"
            html_content += "</ul>"
        except Exception as e:
            print(f"Skipping {topic} due to error: {e}")
            continue

    html_content += "</div></body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_dashboard()
