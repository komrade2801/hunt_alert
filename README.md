# Hunt: Showdown Server Status Checker

A simple Python script that scrapes the official Hunt: Showdown X.com (formerly Twitter) account to provide quick updates on server status. It checks for current downtime, scheduled maintenance, and when servers are back online.

## Features

-   **Real-time Scraping**: Fetches the 5 most recent tweets from `@huntshowdown`.
-   **Intelligent Analysis**: Uses regular expressions to identify keywords like "servers," "maintenance," and "down" while ignoring them in words like "Showdown."
-   **Context-Aware**: Differentiates between:
    -   🚨 **Current Downtime**: Detects if servers are offline right now.
    -   🗓️ **Scheduled Maintenance**: Identifies announcements for future downtime (e.g., "tomorrow," "on July 9th").
    -   ✅ **Maintenance Complete**: Recognizes when servers are back online.
-   **Downtime Extraction**: Automatically extracts the estimated downtime duration (e.g., "~4 hours") from the tweet if mentioned.
-   **Ignores Noise**: Skips retweets to focus only on original status updates.
-   **Clear Output**: Provides a clean, human-readable summary of the findings.

## How It Works

The script uses the `twikit` library to log into X.com and access the public tweets of the `@huntshowdown` user. It then iterates through the most recent tweets, applying a series of checks:

1.  **Keyword Matching**: It first looks for any relevant keywords using a regular expression that matches whole words only.
2.  **Context Analysis**: If a tweet is deemed relevant, it's analyzed further to determine if the maintenance is `completed`, `scheduled`, or happening `now`.
3.  **Detail Extraction**: The script attempts to find and pull out any mention of the maintenance duration.
4.  **Reporting**: Finally, it prints a formatted status report to the console. If no relevant tweet is found, it reports how long ago the last tweet of any kind was posted.

## Prerequisites

-   Python 3.7+
-   An active X.com (Twitter) account. **(Using a secondary or dedicated account is highly recommended)**.

## Installation

1.  **Clone the repository (or download the script):**
    ```sh
    git clone https://github.com/your-username/hunt-server-checker.git
    cd hunt-server-checker
    ```

2.  **Install the required Python library:**
    The script depends on `twikit`, an unofficial library for the X.com API.
    ```sh
    pip install twikit
    ```

## Configuration

Before running the script, you must add your X.com account credentials.

1.  Open the `hunt_server_checker.py` (or your script's name) file in a text editor.
2.  Locate the configuration section at the top of the file.
3.  Replace the placeholder values with your own credentials.

```python
# --- Configuration ---
# IMPORTANT: Replace with your X.com login credentials
USERNAME = "your_x_com_username"
EMAIL = "your_x_com_email"
PASSWORD = "your_x_com_password"
```

> **Security Warning**: Storing credentials directly in a script is not the most secure practice. For personal use, it's acceptable, but it is **strongly recommended to use a dedicated or "burner" X.com account** for this script instead of your personal one to protect your main account's security.

## Usage

Once configured, run the script from your terminal:

```sh
python hunt_server_checker.py
```

The script will print the latest server status directly to your console.

### Example Output (Scheduled Maintenance)
```
Found a potential server status update from @huntshowdown:
-> Tweet: "Hunters, the Live Servers will be taken offline tomorrow, July 9, at 09:00 CEST to deploy an update. Estimated downtime ~4 hours."
   Posted: 0d 18h 32m ago

--- Analysis ---
🗓️ Status: Scheduled maintenance has been announced.
   - Estimated Downtime: ~4 hours
   - This is a future event. Check the tweet for the exact date and time.
----------------
```

### Example Output (No Status Found)
```
No server status updates found in the last 5 original tweets from @huntshowdown.
The last tweet (of any kind) was 0d 2h 15m ago.
```

## Disclaimer

This script relies on web scraping and an unofficial third-party library (`twikit`). The X.com platform may change its structure or API at any time, which could cause this script to stop working without warning. The author is not responsible for any issues that arise from the use of this script. Use at your own risk.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
