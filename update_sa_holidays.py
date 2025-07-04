import re
import requests
import os
from datetime import datetime
from zoneinfo import ZoneInfo

ICS_URL = "https://www.officeholidays.com/ics-all/australia/south-australia"
OUTPUT_FILE = "sa_public_holidays.ics"
URL = ICS_URL  # Used in notifications

# Hardcoded next GitHub Action run time in UTC
NEXT_RUN_UTC = datetime(2025, 10, 1, 0, 30, tzinfo=ZoneInfo("UTC"))

def clean_event_name(summary: str) -> str:
    return re.sub(r"\s*\([^)]*\)", "", summary).strip()

def get_next_run_adelaide() -> str:
    adelaide_time = NEXT_RUN_UTC.astimezone(ZoneInfo("Australia/Adelaide"))
    return adelaide_time.strftime("%A %d %B %Y at %I:%M %p")

def send_failure_notification(error_excerpt: str):
    token = os.environ.get("PUSHOVER_APP_TOKEN")
    user = os.environ.get("PUSHOVER_USER_KEY")
    
    if not token or not user or token == "YOUR_PUSHOVER_APP_TOKEN" or user == "YOUR_PUSHOVER_USER_KEY":
        print("⚠️ Pushover credentials not configured. Skipping failure notification.")
        print(f"Error: {error_excerpt}")
        return

    import httpx
    message = (
        "‼️ SA Calendar Update Failed ‼️\n\n"
        "Your SA Public Holiday calendar could not be updated... Check the following: 🔎\n\n"
        "1. Go to your GitHub repository.\n"
        "2. Click the Actions tab.\n"
        "3. Open the failed workflow.\n"
        "4. Check which step failed.\n\n"
        f"🌐 Main site: {URL}\n"
        f"📅 Calendar source: {URL}\n\n"
        f"🕒 Next auto-update:\n{get_next_run_adelaide()} (Adelaide time)\n\n"
        f"📝 Error Log:\n{error_excerpt}"
    )

    response = httpx.post("https://api.pushover.net/1/messages.json", data={
        "token": token,
        "user": user,
        "message": message
    })

    print("✅ Failure notification sent" if response.status_code == 200 else f"❌ Failed to send notification: {response.text}")

def send_success_notification():
    token = os.environ.get("PUSHOVER_APP_TOKEN")
    user = os.environ.get("PUSHOVER_USER_KEY")
    
    if not token or not user or token == "YOUR_PUSHOVER_APP_TOKEN" or user == "YOUR_PUSHOVER_USER_KEY":
        print("⚠️ Pushover credentials not configured. Skipping success notification.")
        return

    import httpx
    message = (
        "✅ SA Public Holidays Updated ✅\n\n"
        "SA Public Holiday calendar was successfully updated via GitHub!\n\n"
        f"🕒 Next auto-update:\n{get_next_run_adelaide()} (Adelaide time)\n\n"
        "🌞 Have a nice day! 🌞"
    )

    response = httpx.post("https://api.pushover.net/1/messages.json", data={
        "token": token,
        "user": user,
        "message": message
    })

    print("✅ Success notification sent" if response.status_code == 200 else f"❌ Failed to send notification: {response.text}")

def main():
    try:
        print(f"📅 Downloading calendar from {ICS_URL}...")
        response = requests.get(ICS_URL)
        response.raise_for_status()
        content = response.text

        print("🧹 Cleaning event names...")
        cleaned_lines = []
        for line in content.splitlines():
            if line.startswith("SUMMARY"):
                colon_pos = line.find(":")
                if colon_pos > -1:
                    summary_prefix = line[:colon_pos+1]
                    summary_value = line[colon_pos+1:]
                    cleaned_summary = clean_event_name(summary_value)
                    clean_line = f"{summary_prefix}{cleaned_summary}"
                    cleaned_lines.append(clean_line)
                else:
                    cleaned_lines.append(line)
            else:
                cleaned_lines.append(line)

        print(f"💾 Saving to {OUTPUT_FILE}...")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(cleaned_lines))

        print("✅ Calendar updated successfully!")
        send_success_notification()

    except Exception as e:
        print(f"❌ Error updating calendar: {str(e)}")
        send_failure_notification(str(e))

if __name__ == "__main__":
    main()
