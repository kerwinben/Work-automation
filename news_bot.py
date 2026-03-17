import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, timedelta, timezone

def generate_dashboard():
    now_utc = datetime.now(timezone.utc)
    # Adjusting for EDT (UTC-4)
    now_edt = now_utc - timedelta(hours=4)
    display_now = now_edt.strftime("%B %d, %Y | %I:%M %p")
    
    # Refined verticals with clean labels and targeted search strings
    verticals = {
        "Advanced Radar Systems": '("AESA radar" OR "Active Electronically Scanned Array")',
        "Passive Detection": '("passive radar" OR "passive coherent location")',
        "Radar Market Trends": "radar technology trends",
        "Counter-UAS Operations": '("Counter-UAS" OR "c-UAS" OR "cUAS")',
        "SIGINT & Electronic Warfare": '("COMINT" OR "SIGINT" OR "Signals Intelligence" OR "Electronic Warfare")',
        "Regional Tech Intelligence": '("Israeli Defense Tech" OR "American Defense Tech" OR "Chinese Defense Tech" OR "Russian Defense Tech")'
    }
    
    output = []
    output.append("<html><head><title>Director's Strategic Hub</title>")
    output.append("<style>body { font-family: 'Segoe UI', sans-serif; margin: 40px; background: #f0f2f5; }")
    output.append(".container { max-width: 950px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }")
    output.append(".timestamp-box { background: #e8eaf6; padding: 10px 20px; border-radius: 6px; color: #1a237e; font-weight: bold; margin-bottom: 20px; display: flex; justify-content: space-between; }")
    output.append("h1 { color: #1a237e; border-bottom: 4px solid #1a237e; padding-bottom: 10px; margin-bottom: 5px; }")
    output.append("h3 { color: #1565c0; margin-top: 30px; border-bottom: 2px solid #eee; padding-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }")
    output.append("li { margin-bottom: 12px; padding: 12px; background: #fafafa; list-style: none; border-left: 4px solid #1a237e; transition: 0.3s; }")
    output.append("a { text-decoration: none; color: #0277bd; font-weight: bold; font-size: 1.1em; }</style></head>")
    
    output.append("<body><div class='container'>")
    output.append("<h1>Director's Intelligence Hub</h1>")
    
    # --- RESTORED TIMESTAMP BLOCK ---
    output.append(f"<div class='timestamp-box'>")
    output.append(f"<span>🕒 {display_now} EDT</span>")
    output.append(f"<span>{run_label}</span>")
    output.append("</div>")

    headers = {"User-Agent": "Mozilla/5.0"}
    
    for label, search_query in verticals.items():
        output.append(f"<h3>{label}</h3><ul>")
        query = urllib.parse.quote(f'{search_query} when:36h')
        rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        
        try:
            res = requests.get(rss_url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.content, "xml")
            items = soup.find_all('item')[:5]
            
            if not items:
                output.append("<li>No new updates in the last 36 hours.</li>")
            else:
                for item in items:
                    output.append(f"<li><a href='{item.link.text}' target='_blank'>{item.title.text}</a></li>")
        except Exception as e:
            output.append(f"<li>Feed delay. Error: {str(e)}</li>")
        output.append("</ul>")

    output.append("</div></body></html>")
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write("".join(output))

if __name__ == "__main__":
    generate_dashboard()
