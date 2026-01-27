import time
import re
from playwright.sync_api import sync_playwright
import os
import sys
from datetime import datetime, time as dt_time, timedelta

def get_pst_now():
    """Returns the current time in PST (UTC-8)."""
    # GitHub Actions runners are in UTC. PST is UTC-8.
    return datetime.now() - timedelta(hours=8)

def play_alarm():
    """Plays a system sound on macOS."""
    print("\a", end="", flush=True) # Basic terminal beep
    try:
        # Playing a system sound on macOS
        os.system('afplay /System/Library/Sounds/Glass.aiff')
    except:
        pass

def has_hpt(content):
    """Detects HPT targets in the post content."""
    # Pattern: HPT followed by any text and a decimal/number
    return bool(re.search(r'HPT\s+[A-Z0-9.\s]+', content, re.IGNORECASE))

def format_post_content(content):
    """Parses and formats post content for better readability."""
    # Ensure Technical Trend and SPX Pattern are on new lines
    content = re.sub(r"(\w+ - SPX Pattern is)", r"\n\1", content, flags=re.IGNORECASE)
    content = re.sub(r"(SPX Pattern is)", r"\n\1", content, flags=re.IGNORECASE)
    content = re.sub(r"(Technical Trend)", r"\n<strong>\1</strong>", content, flags=re.IGNORECASE)

    # Bold key phrases
    headers = ["Review of the day", "SPX Morning Trend", "SPX Afternoon Trend"]
    for header in headers:
        content = re.sub(f"({header})", r"<strong>\1</strong>", content, flags=re.IGNORECASE)
    
    # Bold SPX Pattern specifically and ensure it's on a new line if caught late
    content = re.sub(r"((\w+ - )?SPX Pattern is [^.]+\.)", r"\n<strong>\1</strong>", content, flags=re.IGNORECASE)

    # Highlight HPT targets within text
    content = re.sub(r"(HPT\s+[A-Z0-9.\s]+(?:\d+\.\d+|\d+))", r"<span class='hpt-highlight'>\1</span>", content, flags=re.IGNORECASE)

    # Put index signals on new lines
    # Pattern: Look for SPY -, QQQ -, IWM -
    content = re.sub(r"(SPY\s*-\s*)", r"\n\1", content)
    content = re.sub(r"(QQQ\s*-\s*)", r"\n\1", content)
    content = re.sub(r"(IWM\s*-\s*)", r"\n\1", content)
    
    return content.strip()

def generate_summary_page(threads, target_date):
    """
    Generates a premium HTML summary page with HPT highlighting.
    """
    now = get_pst_now()
    day_str = now.strftime("%A")
    full_date_str = now.strftime("%B %d, %Y")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UncleK Terminal - {target_date}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #05070a;
            --card-bg: rgba(16, 20, 28, 0.8);
            --accent-primary: #60a5fa;
            --accent-secondary: #34d399;
            --alert-color: #fbbf24;
            --hpt-color: #fb923c;
            --text-main: #f1f5f9;
            --text-muted: #64748b;
            --border-color: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.08);
        }}
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        body {{
            font-family: 'Outfit', sans-serif;
            background: var(--bg-color);
            background-image: 
                radial-gradient(circle at 10% 10%, rgba(59, 130, 246, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 90% 90%, rgba(249, 115, 22, 0.08) 0%, transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 2rem 1rem;
            line-height: 1.5;
        }}
        
        .container {{
            max-width: 950px;
            margin: 0 auto;
        }}
        
        header {{
            margin-bottom: 2rem;
            text-align: center;
        }}
        
        .terminal-header {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: rgba(255, 255, 255, 0.03);
            padding: 8px 16px;
            border-radius: 999px;
            border: 1px solid var(--border-color);
            margin-bottom: 1rem;
        }}
        
        .status-dot {{
            width: 8px;
            height: 8px;
            background: var(--accent-secondary);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--accent-secondary);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
            100% {{ opacity: 1; }}
        }}
        
        h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        
        .date-display {{
            font-size: 1.1rem;
            color: var(--text-muted);
            font-weight: 400;
        }}

        /* Live Mode Controls */
        .live-mode-banner {{
            background: rgba(96, 165, 250, 0.1);
            border: 1px solid rgba(96, 165, 250, 0.2);
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(8px);
        }}

        .live-status {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
            font-size: 0.9rem;
        }}

        #live-toggle-btn {{
            background: var(--accent-primary);
            color: #000;
            border: none;
            padding: 8px 20px;
            border-radius: 8px;
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
        }}

        #live-toggle-btn:hover {{
            transform: translateY(-2px);
            filter: brightness(1.1);
        }}

        #live-toggle-btn.active {{
            background: #ef4444; /* Red for Stop */
            color: #fff;
        }}
        
        .thread-group {{
            margin-bottom: 3.5rem;
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border-radius: 24px;
            border: 1px solid var(--glass-border);
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }}
        
        .post {{
            padding: 2rem;
            border-bottom: 1px solid var(--border-color);
            position: relative;
            transition: background 0.3s ease;
        }}
        
        .post:last-child {{ border-bottom: none; }}
        
        .post:hover {{ background: rgba(255, 255, 255, 0.01); }}
        
        .post-meta {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1.25rem;
        }}
        
        .author-info {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        
        .author-name {{
            font-weight: 700;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .author-name.unclek {{ color: #fff; }}
        
        .time-badge {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: var(--text-muted);
            background: rgba(0,0,0,0.3);
            padding: 4px 10px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }}
        
        .post-content {{
            font-size: 1.15rem;
            color: var(--text-main);
            white-space: pre-wrap;
            word-break: break-word;
            font-weight: 300;
        }}
        
        .hpt-alert-card {{
            background: linear-gradient(to right, rgba(249, 115, 22, 0.1), transparent);
            border-left: 4px solid var(--hpt-color);
        }}
        
        .hpt-badge {{
            background: var(--hpt-color);
            color: #000;
            font-weight: 800;
            font-size: 0.65rem;
            padding: 2px 8px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .no-posts {{
            text-align: center;
            padding: 6rem;
            background: var(--card-bg);
            border-radius: 24px;
            border: 1px dashed var(--border-color);
            color: var(--text-muted);
        }}
        
        footer {{
            margin-top: 5rem;
            text-align: center;
            padding-bottom: 4rem;
        }}
        
        .hpt-highlight {{
            color: var(--hpt-color);
            font-weight: 800;
            background: rgba(249, 115, 22, 0.15);
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid rgba(249, 115, 22, 0.3);
        }}

        .config-info {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 1rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="terminal-header">
                <div class="status-dot"></div>
                <span style="font-size: 0.75rem; font-weight: 600; letter-spacing: 0.1em; color: var(--text-muted);">EWT LIVE TRACKER</span>
            </div>
            <h1>UncleK Signals</h1>
            <div class="date-display">{day_str} &bull; {full_date_str}</div>
        </header>

        <div class="live-mode-banner">
            <div class="live-status">
                <span id="live-indicator-dot" style="width: 10px; height: 10px; background: #475569; border-radius: 50%;"></span>
                <span id="live-status-text">LIVE MODE: OFF</span>
            </div>
            <button id="live-toggle-btn">START LIVE MODE</button>
        </div>
        
        <main id="signals-main">
"""
    if threads:
        for thread_id, posts in threads.items():
            unclek_posts = [p for p in posts if p['author'] == "UncleK"]
            if not unclek_posts:
                continue

            html_content += f'            <div class="thread-group">\n'
            for p in unclek_posts:
                is_hpt = has_hpt(p['content'])
                css_class = ""
                if p['author'] == "UncleK":
                    css_class = "unclek"
                    if is_hpt:
                        css_class += " hpt-alert-card"
                
                hpt_tag = '<span class="hpt-badge">HPT TARGET</span>' if is_hpt else ''
                formatted_content = format_post_content(p['content'])
                timestamp = p.get('timestamp', '0')
                
                html_content += f"""                <div class="post {css_class}" data-timestamp="{timestamp}" data-hpt="{'true' if is_hpt else 'false'}">
                    <div class="post-meta">
                        <div class="author-info">
                            <span class="author-name {'unclek' if p['author'] == 'UncleK' else ''}">{p['author']} {hpt_tag}</span>
                        </div>
                        <span class="time-badge">{p['time']}</span>
                    </div>
                    <div class="post-content">{formatted_content}</div>
                </div>\n"""
            html_content += '            </div>\n'
    else:
        html_content += '            <div class="no-posts">Monitoring for signals... No activity from UncleK yet today.</div>\n'

    html_content += """        </main>
        <footer>
            <div class="config-info">Auto-polling active: 5:00 AM &mdash; 1:30 PM PST</div>
            <div class="config-info" id="last-refresh-time">Last updated: Just now</div>
        </footer>
    </div>

    <script>
    let isLive = false;
    let refreshInterval = null;
    let lastSeenPostTimestamp = 0;
    const btn = document.getElementById('live-toggle-btn');
    const statusText = document.getElementById('live-status-text');
    const dot = document.getElementById('live-indicator-dot');
    const lastRefreshEl = document.getElementById('last-refresh-time');

    // Synthesis for Cat Call (Wolf Whistle) Sound
    function playAlert() {
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            
            // Part 1: Slide Up
            const osc1 = ctx.createOscillator();
            const gain1 = ctx.createGain();
            osc1.type = 'sine';
            osc1.frequency.setValueAtTime(800, ctx.currentTime);
            osc1.frequency.exponentialRampToValueAtTime(2500, ctx.currentTime + 0.15);
            
            gain1.gain.setValueAtTime(0, ctx.currentTime);
            gain1.gain.linearRampToValueAtTime(0.4, ctx.currentTime + 0.05);
            gain1.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.2);
            
            osc1.connect(gain1);
            gain1.connect(ctx.destination);
            osc1.start();
            osc1.stop(ctx.currentTime + 0.2);

            // Part 2: Slide Down (Cat Call finish)
            setTimeout(() => {
                const osc2 = ctx.createOscillator();
                const gain2 = ctx.createGain();
                osc2.type = 'sine';
                osc2.frequency.setValueAtTime(2200, ctx.currentTime);
                osc2.frequency.exponentialRampToValueAtTime(1000, ctx.currentTime + 0.3);
                
                gain2.gain.setValueAtTime(0, ctx.currentTime);
                gain2.gain.linearRampToValueAtTime(0.4, ctx.currentTime + 0.05);
                gain2.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.4);
                
                osc2.connect(gain2);
                gain2.connect(ctx.destination);
                osc2.start();
                osc2.stop(ctx.currentTime + 0.4);
            }, 250);
            
            console.log("Cat Call played!");
        } catch(e) { console.error("Audio failed", e); }
    }

    function updateLastSeen() {
        const posts = document.querySelectorAll('.post');
        posts.forEach(p => {
            const ts = parseInt(p.getAttribute('data-timestamp'));
            if (ts > lastSeenPostTimestamp) lastSeenPostTimestamp = ts;
        });
    }

    async function checkForUpdates() {
        console.log("Checking for updates...");
        try {
            const response = await fetch(window.location.href, { cache: 'no-store' });
            const text = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(text, 'text/html');
            
            const newPosts = doc.querySelectorAll('.post');
            let foundNewHPT = false;
            let addedCount = 0;

            newPosts.forEach(p => {
                const ts = parseInt(p.getAttribute('data-timestamp'));
                if (ts > lastSeenPostTimestamp) {
                    addedCount++;
                    if (p.getAttribute('data-hpt') === 'true') foundNewHPT = true;
                }
            });

            if (addedCount > 0) {
                console.log(`Detected ${addedCount} new posts! Refreshing UI...`);
                if (foundNewHPT) playAlert();
                // We reload the whole page to get the new server-generated HTML structure easily
                window.location.reload();
            } else {
                lastRefreshEl.innerText = "Last checked: " + new Date().toLocaleTimeString();
            }
        } catch (e) {
            console.error("Refresh failed", e);
        }
    }

    btn.addEventListener('click', () => {
        isLive = !isLive;
        if (isLive) {
            btn.innerText = "STOP LIVE MODE";
            btn.classList.add('active');
            statusText.innerText = "LIVE MODE: ACTIVE";
            dot.style.background = "#22c55e";
            dot.style.boxShadow = "0 0 10px #22c55e";
            updateLastSeen();
            // Check every 2 minutes
            refreshInterval = setInterval(checkForUpdates, 120000);
            // Play a small sound just for confirmation
            playAlert();
        } else {
            btn.innerText = "START LIVE MODE";
            btn.classList.remove('active');
            statusText.innerText = "LIVE MODE: OFF";
            dot.style.background = "#475569";
            dot.style.boxShadow = "none";
            clearInterval(refreshInterval);
        }
    });

    // Initialize last seen
    updateLastSeen();
    </script>
</body>
</html>"""
    
    with open("unclek_summary.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def is_within_time_window():
    """Checks if current PST time is between 5:00 AM and 1:30 PM, Mon-Fri, excluding holidays."""
    now = get_pst_now()
    # Check if Mon-Fri (0-4)
    if now.weekday() > 4:
        return False
        
    # Check for 2026 US Holidays (Jan 1, Jan 19, Feb 16, May 25, Jun 19, Jul 3/4, Sep 7, Oct 12, Nov 11, Nov 26, Dec 25)
    holidays_2026 = [
        "2026-01-01", "2026-01-19", "2026-02-16", "2026-05-25", 
        "2026-06-19", "2026-07-03", "2026-07-04", "2026-09-07",
        "2026-10-12", "2026-11-11", "2026-11-26", "2026-12-25"
    ]
    if now.strftime("%Y-%m-%d") in holidays_2026:
        return False

    current_time = now.time()
    start = dt_time(5, 0)
    end = dt_time(13, 30)
    return start <= current_time <= end

def scrape_uncle_k(email, password, last_known_count=0):
    """
    Scrapes the signals and returns threads, and whether there are new posts.
    """
    now = get_pst_now()
    site_today = now.strftime("%b %d")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla")
        page = context.new_page()

        print(f"Navigating to login page...", flush=True)
        page.goto("https://www.elliottwavetrader.net/login")
        print(f"Filling credentials...", flush=True)
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        print(f"Submitting login...", flush=True)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        print(f"Login successful. Navigating to Tag page...", flush=True)

        page.goto("https://www.elliottwavetrader.net/trading-room/tag/UncleKSignals")
        print(f"Waiting for entries to load...", flush=True)
        try:
            page.wait_for_selector(".atc-entry", timeout=30000)
            # Save full scraped page content as discussed
            with open("response.html", "w", encoding="utf-8") as f:
                f.write(page.content())
        except:
            browser.close()
            return None, False, 0

        all_entries = page.query_selector_all(".atc-entry")
        threads = {}
        uncle_k_thread_ids = set()
        total_posts_processed = 0
        new_hpt_found = False

        # Phase 1: Identify threads
        for entry in all_entries:
            date_el = entry.query_selector(".atc-datePart")
            if not date_el or site_today not in date_el.inner_text():
                continue
            
            author_el = entry.query_selector(".atc-username")
            parent_id = entry.get_attribute("parentid")
            is_reply = entry.get_attribute("isreply") == "true" or parent_id not in [None, "0", ""]
            
            if author_el and "UncleK" in author_el.inner_text() and not is_reply:
                thread_id = entry.get_attribute("threadid")
                if thread_id:
                    uncle_k_thread_ids.add(thread_id)

        # Phase 2: Collect data & count
        current_post_count = 0
        for entry in all_entries:
            thread_id = entry.get_attribute("threadid")
            if thread_id in uncle_k_thread_ids:
                author_el = entry.query_selector(".atc-username")
                time_el = entry.query_selector(".atc-timePart")
                content_el = entry.query_selector(".atc-entrytext")
                entry_time_el = entry.query_selector(".atc-entrytime")
                
                if author_el and content_el:
                    current_post_count += 1
                    post_data = {
                        "author": author_el.inner_text().strip(),
                        "time": time_el.inner_text().strip() if time_el else "",
                        "content": content_el.inner_text().strip(),
                        "timestamp": entry_time_el.get_attribute("timestamp") if entry_time_el else "0"
                    }
                    if thread_id not in threads:
                        threads[thread_id] = []
                    threads[thread_id].append(post_data)

        # Check for new posts
        has_new = current_post_count > last_known_count
        
        # Check newly added posts for HPT (Phase 2.5)
        # For simplicity, if count increased, check all for HPT alerts
        if has_new:
            for thread_id in threads:
                for p in threads[thread_id]:
                    if p['author'] == "UncleK" and has_hpt(p['content']):
                        # Only alert if this HPT wasn't in the previous count logic 
                        # (Ideally we'd track IDs, but count is a good proxy for this demo)
                        new_hpt_found = True

        for thread_id in threads:
            threads[thread_id].sort(key=lambda x: int(x['timestamp']))

        print(f"Found {len(uncle_k_thread_ids)} UncleK threads and {current_post_count} posts.", flush=True)
        browser.close()
        return threads, has_new, current_post_count, new_hpt_found

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='UncleK Signal Scraper')
    parser.add_argument('--run-once', action='store_true', help='Run once and exit')
    args, unknown = parser.parse_known_args()
    
    # Extract credentials from sys.argv or env
    # For GitHub Actions, we often use env vars directly or pass them
    email = os.getenv("EWT_EMAIL")
    password = os.getenv("EWT_PASSWORD")
    
    # Fallback to sys.argv for local testing
    if not email and len(sys.argv) > 1: email = sys.argv[1]
    if not password and len(sys.argv) > 2: password = sys.argv[2]
    
    if args.run_once:
        print(f"Running in single-scrape mode...", flush=True)
        threads, has_new, new_count, new_hpt_alert = scrape_uncle_k(email, password, 0)
        if threads:
            generate_summary_page(threads, get_pst_now().strftime("%b %d"))
            print("Summary page updated successfully.", flush=True)
        sys.exit(0)

    last_count = 0
    print(f"Starting UncleK Signal Polling [5:00 AM - 1:30 PM PST]...", flush=True)
    first_run = True

    while True:
        if is_within_time_window():
            now_pst = get_pst_now()
            now_str = now_pst.strftime("%H:%M:%S")
            print(f"[{now_str}] Polling for updates (PST)...", flush=True)
            
            threads, has_new, new_count, new_hpt_alert = scrape_uncle_k(email, password, last_count)
            
            if threads and (has_new or first_run):
                print(f"[{now_str}] Updating summary page...", flush=True)
                generate_summary_page(threads, now_pst.strftime("%b %d"))
                last_count = new_count
                if first_run:
                    print(f"[{now_str}] Initial summary generated.", flush=True)
                    first_run = False
                
                if new_hpt_alert:
                    print(f"[{now_str}] !!! HPT TARGET SIGNAL DETECTED !!! Triggering Alarm...", flush=True)
                    play_alarm()
            else:
                print(f"[{now_str}] No new signals found.", flush=True)
        else:
            print("Outside polling window (5:00 AM - 1:30 PM PST Mon-Fri). Sleeping for 1 hour...", flush=True)
            time.sleep(3600)
            continue

        print("Waiting 15 minutes for next poll...", flush=True)
        time.sleep(900)
