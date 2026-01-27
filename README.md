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

## View results
The results are saved to `unclek_summary.html`. You can enable **GitHub Pages** in your repository settings to host this file as a live website.

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
