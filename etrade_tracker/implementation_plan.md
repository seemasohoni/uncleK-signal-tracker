# Plan: E*Trade Performance Tracker

This project will track daily gains and losses for multiple E*Trade accounts starting from Jan 1st, 2026, and provide a dashboard for performance visualization and gameplan notes.

> [!IMPORTANT]
> **Update Strategy**: Using the **Official E*Trade API** (OAuth 1.0a). 
> - You will need to obtain an **API Key** and **Secret** from the E*Trade Developer Portal.
> - The initial authentication will require you to log in via a browser once and paste a verification code into the script. After that, we can use persistent tokens for a limited time.

> [!IMPORTANT]
> **Jan 1st Baseline**: Since we are starting this today (Jan 26), we need your account balances as of Jan 1st, 2026, to calculate the YTD (Year-To-Date) performance correctly.

## Proposed Changes

### [Core Logic]

#### [NEW] `data_manager.py`
Handle persistent storage of account balances and P/L calculations.
- Use a JSON or CSV file to store date-wise balances per account.
- Calculate daily change ($ and %) and cumulative YTD change.

#### [NEW] `update_balances.py`
The main interactive script to update today's data.
- Authenticate with E*Trade API.
- Fetch balances for all linked accounts.
- Prompt for "Next Day Gameplan" notes.
- Update the dashboard data.

### [Dashboard UI]

#### [NEW] `index.html` (Dashboard)
A premium, dark-mode trading terminal dashboard.
- **Performance Highlights**: Total YTD P/L, daily change.
- **Account Breakdown**: Table/Cards showing each account's current status.
- **Equity Curve**: A chart (using Chart.js) showing balance growth since Jan 1st.
- **Gameplan Section**: Large, editable or display area for the daily notes.

## Verification Plan

### Automated Verification
- Unit test for P/L calculation logic (ensuring math is correct for gains/losses).
- Validation of data storage format.

### Manual Verification
1. Run the update script and enter sample data for a few previous dates.
2. Verify the dashboard correctly reflects the tally and curves.
3. Verify the gameplan notes are saved and displayed correctly.
