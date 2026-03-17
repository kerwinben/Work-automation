
    
    # Refined verticals with clean labels and targeted search strings
    
    
    import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, timedelta, timezone

def generate_dashboard():
    try:
        # Secure timestamp logic
        now_utc = datetime.now(timezone.utc)
        now_edt = now_utc - timedelta(hours=4) 
        display_now = now_edt.strftime("%B %d, %Y | %I:%M %p")
        
        # Determine Run Label
        run_label = "Morning Update" if now_edt.hour < 12 else "Afternoon Update"

        verticals = {
            "Advanced Radar Systems": '("AESA radar" OR "Active Electronically Scanned Array")',
            "Passive Detection": '("passive radar" OR "passive coherent location")',
            "Radar Market Trends": "radar technology trends",
            "Counter-UAS Operations": '("Counter-UAS" OR "c-UAS" OR "cUAS")',
            "SIGINT & Electronic Warfare": '("COMINT" OR "SIGINT" OR "Signals Intelligence" OR "Electronic Warfare")',
            "Regional Tech Intelligence": '("Israeli Defense Tech" OR "American Defense Tech" OR "Chinese Defense Tech" OR "Russian Defense Tech")'
        }
        
        # 3. HTML Construction
        output = [
            "<html><head><title>Director's Strategic Hub</title>",
            "<style>body { font-family: 'Segoe UI', sans-serif; margin: 40px; background: #f0f2f5; }",
            ".container { max-width: 950px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }",
            ".timestamp-box { background: #e8eaf6; padding: 10px 20px; border-radius: 6px; color: #1a237e; font-weight: bold; margin-bottom: 20px; display: flex; justify-content: space-between; }",
            "h1 { color: #1a237e; border-bottom: 4px solid #1a237e; padding-bottom: 10px; }",
            "h3 { color: #1565c0; margin-top: 30px; border-bottom: 2px solid #eee; padding-bottom: 5px; text-transform: uppercase; }",
            "li { margin-bottom: 12px; padding: 12px; background: #fafafa; list-style: none; border-left: 4px solid #1a237e; }",
            "a { text-decoration: none; color: #0277bd; font-weight: bold; }</style></head>",
            "<body><div class='container'><h1>Director's Intelligence Hub</h1>",
            f"<div class='timestamp-box'><span>🕒 {display_now} EDT</span><span>{run_label}</span></div>"
        ]

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        for label, search_query in verticals.items():
            output.append(f"<h3>{label}</h3><ul>")
            query = urllib.parse.quote(f'{search_query} when:36h')
            rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            
            res = requests.get(rss_url, headers=headers, timeout=15)
            # CRITICAL CHANGE: Use 'html.parser' instead of 'xml' or 'lxml'
            soup = BeautifulSoup(res.content, "html.parser") 
            
            items = soup.find_all('item')[:5]
            if not items:
                output.append("<li>No new updates in the last 36 hours.</li>")
            else:
                for item in items:
                    # Google News RSS titles/links are in <title> and <link> tags
                    t = item.find('title').get_text() if item.find('title') else "No Title"
                    l = item.find('link').get_text() if item.find('link') else "#"
                    output.append(f"<li><a href='{l}' target='_blank'>{t}</a></li>")
            output.append("</ul>")

        output.append("</div></body></html>")
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write("".join(output))

    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate_dashboard()
