# uncleK-signal-tracker

Automated scraper for `elliottwavetrader.net` that tracks "UncleK" signals and displays them in a premium dashboard.

## Automation Details
- **Schedule**: Every 15 minutes, Monday through Friday.
- **Market Hours**: 5:00 AM – 1:30 PM PST.
- **Holidays**: Automatically excludes US market holidays.

## Setup Instructions

To host this on your own GitHub account:

1.  **Create a Repository**: Push these files to a new private repository on GitHub.
2.  **Add Secrets**:
    - Go to your repository **Settings** > **Secrets and variables** > **Actions**.
    - Click **New repository secret**.
    - Add `EWT_EMAIL`: Your ElliottWaveTrader email.
    - Add `EWT_PASSWORD`: Your ElliottWaveTrader password.
3.  **Enable GitHub Actions**: GitHub Actions should be enabled by default. The script will run automatically on the schedule.

## GitHub Operations

### 1. How to monitor the script
Go to your repository on GitHub and click on the **Actions** tab at the top.

You will see a list called "**UncleK Signal Scraper**".
Every 15 minutes (during market hours), a new "run" will appear here. Green means it succeeded and updated your signals; red means there was an error (usually due to login issues if secrets aren't set).

### 2. How to see your live HTML Dashboard
To view the results as a website rather than just a code file, you need to enable **GitHub Pages**:

1. Go to **Settings** (top right of your repo).
2. Click **Pages** on the left sidebar.
3. Under **Build and deployment > Branch**, change "None" to **main**.
4. Click **Save**.

Your link will look like this: `https://seemasohoni.github.io/uncleK-signal-tracker/unclek_summary.html`
*(Note: It may take 1-2 minutes for the link to become active after you save the settings.)*

Feel free to share that link when you're ready! What's the new project you'd like to dive into next?

## Live Mode & Sound Alerts
To hear the **loud Cat Call (wolf whistle)** alert for new HPT signals (especially when hosted on GitHub):
1. Open your live dashboard link.
2. Click the **"START LIVE MODE"** button in the top banner.
3. Keep the tab open.
   - The page will automatically check for updates every 2 minutes.
   - When a new "HPT Target" is detected, it will play a loud Cat Call sound.

---

### Troubleshooting Sound
- **No Sound?** Browsers require user interaction (like clicking "Start Live Mode") before they allow sound to play.
- **Not Refreshing?** Ensure you clicked the button; the indicator should be green and pulsing.

## Troubleshooting GIT Push
If you see `remote: Repository not found`, it means you need to create the repository on the web second first:
1. Go to [github.com/new](https://github.com/new)
2. Create a repo named `uncleK-signal-tracker` (Private)
3. Do **not** initialize with README or license.
4. Run `git push -u origin main` in your terminal.
