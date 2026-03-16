import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, timedelta, timezone

def generate_dashboard():
    now_utc = datetime.now(timezone.utc)
    now_edt = now_utc - timedelta(hours=4)
    display_now = now_edt.strftime("%B %d, %Y | %I:%M %p")
    
    verticals = verticals = [
        "AESA",
        "passive radar",
        "radar technology trends",
        "passive coherent location",
        "Counter-UAS (c-UAS) systems",
        "SIGINT", 
        "Electronic Warfare",
        "Israeli Defense Tech"
    ]
    
    output = []
    output.append("<html><head><title>ELTA Strategic Hub</title>")
    output.append("<style>body { font-family: 'Segoe UI', sans-serif; margin: 40px; background: #f0f2f5; }")
    output.append(".container { max-width: 950px; margin: auto; background: white; padding: 30px; border-radius: 12px; }")
    output.append(".sam-box { background: #e3f2fd; padding: 20px; border-radius: 8px; border-left: 6px solid #1565c0; margin-bottom: 30px; }")
    output.append("h1 { color: #1a237e; border-bottom: 4px solid #1a237e; }")
    output.append("h3 { color: #c62828; margin-top: 25px; border-bottom: 1px solid #ddd; }")
    output.append("li { margin-bottom: 12px; padding: 10px; background: #fafafa; list-style: none; border-bottom: 1px solid #eee; }")
    output.append("a { text-decoration: none; color: #0277bd; font-weight: bold; }</style></head>")
    output.append(f"<body><div class='container'><h1>Director's Intelligence Hub</h1>")
    output.append(f"<p><strong>Last Updated:</strong> {display_now} EDT</p>")

    # --- SECTION 1: SAM.GOV OPPORTUNITIES ---
    output.append("<div class='sam-box'><h2>🎯 Active Gov Opportunities (SAM.gov)</h2><ul>")
    
    # SAM.gov Search for Defense Electronics / Radars
    # Refined for High-Value Leads
    # Use "OR" in capital letters between keywords
    sam_query = "radar OR SIGINT OR AESA OR PCL"
    sam_url = f"https://sam.gov/api/prod/opportunities/v1/search?index=opp&q={sam_query}&sort=-modifiedDate&mode=search&is_active=true"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        # Note: In a production environment, use a SAM.gov API Key for more than 10 hits
        sam_res = requests.get(sam_url, headers=headers, timeout=15)
        opportunities = sam_res.json().get('opportunitiesData', [])[:5]
        
        if not opportunities:
            output.append("<li>No new SAM.gov notices in the last 24h.</li>")
        for opp in opportunities:
            title = opp.get('title', 'No Title')
            sol_num = opp.get('solicitationNumber', 'N/A')
            link = f"https://sam.gov/opp/{opp.get('noticeId')}/view"
            output.append(f"<li><strong>[{sol_num}]</strong> <a href='{link}' target='_blank'>{title}</a></li>")
    except:
        output.append("<li>SAM.gov feed temporarily unavailable.</li>")
    output.append("</ul></div>")

    # --- SECTION 2: INDUSTRY NEWS ---
    for topic in verticals:
        output.append(f"<h3>{topic.upper()} NEWS</h3><ul>")
        query = urllib.parse.quote(f'"{topic}" when:1d')
        rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        try:
            res = requests.get(rss_url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.content, "xml")
            for item in soup.find_all('item')[:4]:
                output.append(f"<li><a href='{item.link.text}' target='_blank'>{item.title.text}</a></li>")
        except:
            output.append("<li>Feed delay. Check back later.</li>")
        output.append("</ul>")

    output.append("</div></body></html>")
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write("".join(output))

if __name__ == "__main__":
    generate_dashboard()
