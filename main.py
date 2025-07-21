import asyncio
import datetime
import re
from twikit import Client

# --- Configuration ---
# IMPORTANT: Replace with your X.com login credentials
USERNAME = ""
EMAIL = ""
PASSWORD = ""
TARGET_USERNAME = "huntshowdown"

# --- Improved Keyword Matching using Regular Expressions for Whole Words ---
# The \b ensures we match whole words only (e.g., "down" but not "showdown")
RELEVANT_KEYWORDS_PATTERN = re.compile(
    r'\b(servers|down|maintenance|offline|downtime)\b', re.IGNORECASE
)


def analyze_tweet_content(text):
    """
    Analyzes the tweet text to determine server status and extract details.
    Returns a dictionary with the analysis.
    """
    analysis = {'status': 'unknown', 'duration': None, 'details': None}
    text_lower = text.lower()

    # --- Tactic 1: Check if maintenance is over ---
    if "back online" in text_lower or "maintenance has concluded" in text_lower or "completed" in text_lower:
        analysis['status'] = 'completed'
        return analysis

    # --- Tactic 2: Check for scheduled/future maintenance ---
    if "will be taken offline" in text_lower or "scheduled maintenance" in text_lower or "tomorrow" in text_lower:
        analysis['status'] = 'scheduled'
    # Check for specific dates like "9 July," or "July 9,"
    elif re.search(r'\d{1,2}\s+\w+', text_lower):
        analysis['status'] = 'scheduled'

    # --- Tactic 3: If it's relevant but not past or future, assume it's current ---
    elif RELEVANT_KEYWORDS_PATTERN.search(text_lower):
        analysis['status'] = 'down_now'

    # --- Tactic 4: Try to extract estimated downtime ---
    duration_match = re.search(r'~?(\d+)\s*hours?', text_lower)
    if duration_match:
        analysis['duration'] = f"~{duration_match.group(1)} hours"

    return analysis


async def get_server_status():
    """
    Scrapes the last 5 tweets from @huntshowdown and analyzes them for server status.
    """
    client = Client('en-US')
    try:
        await client.login(auth_info_1=USERNAME, auth_info_2=EMAIL, password=PASSWORD)
    except Exception as e:
        print(
            f"An error occurred during login: {e}\nPlease check your credentials.")
        return

    try:
        user = await client.get_user_by_screen_name(TARGET_USERNAME)
        tweets = await user.get_tweets('Tweets', count=5)

        found_status_tweet = False
        if not tweets:
            print(f"Could not retrieve tweets for @{TARGET_USERNAME}.")
            return

        for tweet in tweets:
            if tweet.text.startswith('RT'):  # Skip retweets
                continue

            # Check if the tweet is relevant using our improved pattern
            if RELEVANT_KEYWORDS_PATTERN.search(tweet.text):
                found_status_tweet = True
                print(
                    f"Found a potential server status update from @{TARGET_USERNAME}:")
                print(f"-> Tweet: \"{tweet.text}\"")

                # --- Time Calculation ---
                tweet_time = datetime.datetime.strptime(
                    tweet.created_at, '%a %b %d %H:%M:%S %z %Y')
                now_utc = datetime.datetime.now(datetime.timezone.utc)
                time_difference = now_utc - tweet_time
                days, rem = divmod(time_difference.total_seconds(), 86400)
                hours, rem = divmod(rem, 3600)
                minutes, _ = divmod(rem, 60)
                time_ago = f"{int(days)}d {int(hours)}h {int(minutes)}m ago"
                print(f"   Posted: {time_ago}")

                # --- Run the new analysis logic ---
                analysis = analyze_tweet_content(tweet.text)

                print("\n--- Analysis ---")
                if analysis['status'] == 'completed':
                    print(
                        "✅ Status: Servers should be back online. Maintenance appears to be finished.")
                elif analysis['status'] == 'scheduled':
                    print("🗓️ Status: Scheduled maintenance has been announced.")
                    if analysis['duration']:
                        print(
                            f"   - Estimated Downtime: {analysis['duration']}")
                    print(
                        "   - This is a future event. Check the tweet for the exact date and time.")
                elif analysis['status'] == 'down_now':
                    print("🚨 Status: Servers appear to be down currently.")
                    if analysis['duration']:
                        print(
                            f"   - Mentioned Duration: {analysis['duration']}")
                else:
                    print(
                        "❓ Status: A server-related tweet was found, but the status is unclear. Please read the tweet.")

                print("-" * 16)
                break  # Stop after finding the first relevant tweet

        if not found_status_tweet:
            print(
                f"No server status updates found in the last 5 original tweets from @{TARGET_USERNAME}.")
            # Report time since the last tweet of any kind
            last_tweet_time = datetime.datetime.strptime(
                tweets[0].created_at, '%a %b %d %H:%M:%S %z %Y')
            time_difference = datetime.datetime.now(
                datetime.timezone.utc) - last_tweet_time
            days, rem = divmod(time_difference.total_seconds(), 86400)
            hours, rem = divmod(rem, 3600)
            minutes, _ = divmod(rem, 60)
            time_ago = f"{int(days)}d {int(hours)}h {int(minutes)}m ago"
            print(f"The last tweet (of any kind) was {time_ago}.")

    except Exception as e:
        print(f"An error occurred while processing tweets: {e}")
    finally:
        await client.logout()

if __name__ == "__main__":
    if USERNAME == "your_username" or EMAIL == "your_email" or PASSWORD == "your_password":
        print("Please configure your X.com login credentials in the script before running.")
    else:
        asyncio.run(get_server_status())
