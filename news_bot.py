import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime, timedelta, timezone
import sys

def generate_dashboard():
    try:
        # 1. Time Setup
        now_utc = datetime.now(timezone.utc)
        now_edt = now_utc - timedelta(hours=4) 
        display_now = now_edt.strftime("%B %d, %Y | %I:%M %p")
        run_label = "Morning Update" if now_edt.hour < 12 else "Afternoon Update"

        # Global Exclusions to aggressively eliminate hobbyist/toy drone clutter
        exclusions = " -dji -toy -hobby -racing -consumer -amateur -review"

        # 2. Corrected Multi-line Technical Strings
        verticals = {
            "Advanced Radar Systems": """("AESA" OR "Active Electronically Scanned Array" OR "GaN radar" OR "digital beamforming") AND ("X-band" OR "S-band" OR "Ku-band" OR "multi-mission" OR "low-RCS")""",
            "Passive Detection": """("passive radar" OR "passive coherent location")""",
            "Radar Market Trends": f"Military radar technology trends{exclusions}",
            "Counter-UAS Operations": f"""("c-UAS" OR "Counter-UAS" OR "counter-drone" OR "swarming") AND ("GNSS-denied" OR "GPS-jammed" OR "soft-kill" OR "hard-kill" OR "directed energy" OR "threat emulation" OR "Red Air"){exclusions}""",
            "SIGINT & Electronic Warfare": """("SIGINT" OR "COMINT" OR "ELINT" OR "spectrum intelligence") AND ("RF geolocation" OR "direction finding" OR "airborne ISR" OR "CMS integration" OR "tactical data link")""",
            "Regional Tech Intelligence": """("Israeli Defense Tech" OR "American Defense Tech" OR "Chinese Defense Tech" OR "Russian Defense Tech")"""
        }
        
        # 3. HTML Construction
        output = [
            "<html><head><title>Director's Strategic Hub</title>",
            "<style>body { font-family: 'Segoe UI', sans-serif; margin: 40px; background: #f0f2f5; }",
            ".container { max-width: 950px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }",
            ".timestamp-box { background: #e8eaf6; padding: 10px 20px; border-radius: 6px; color: #1a237e; font-weight: bold; margin-bottom: 20px; display: flex; justify-content: space-between; }",
            "h1 { color: #1a237e; border-bottom: 4px solid #1a237e; padding-bottom: 10px; margin-bottom: 5px; }",
            "h3 { color: #1565c0; margin-top: 30px; border-bottom: 2px solid #eee; padding-bottom: 5px; text-transform: uppercase; }",
            "li { margin-bottom: 12px; padding: 12px; background: #fafafa; list-style: none; border-left: 4px solid #1a237e; }",
            "a { text-decoration: none; color: #0277bd; font-weight: bold; font-size: 1.1em; }</style></head>",
            "<body><div class='container'><h1>Director's Intelligence Hub</h1>",
            f"<div class='timestamp-box'><span>🕒 {display_now} EDT</span><span>{run_label}</span></div>"
        ]

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        
        for label, search_query in verticals.items():
            output.append(f"<h3>{label}</h3><ul>")
            
            query = urllib.parse.quote(f'{search_query.strip()} when:2d')
            rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            
            res = requests.get(rss_url, headers=headers, timeout=15)
            
            if res.status_code != 200:
                output.append(f"<li>Search temporarily unavailable (Status: {res.status_code})</li>")
                continue

            # Switch to 'xml' to perfectly handle RSS structural tags like <link>
            soup = BeautifulSoup(res.content, "xml")
            items = soup.find_all('item')[:5]
            
            if not items:
                output.append("<li>No new updates in the last 48 hours.</li>")
            else:
                for item in items:
                    title_tag = item.find('title')
                    link_tag = item.find('link')
                    
                    if title_tag and link_tag:
                        title_text = title_tag.get_text()
                        url = link_tag.get_text().strip()
                        
                        if url.startswith("http"):
                            output.append(f"<li><a href='{url}' target='_blank' rel='noopener noreferrer'>{title_text}</a></li>")
            
            output.append("</ul>")

        output.append("</div></body></html>")
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write("".join(output))
        print("SUCCESS: Dashboard written to index.html")

    except Exception as e:
        print(f"FAILED: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    generate_dashboard()
