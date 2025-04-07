# SA Public Holidays Calendar Updater

A simple script to clean SA Public Holidays for display in Calendar applications.

## What It Does

This project automatically fetches South Australian public holidays from [officeholidays.com](https://www.officeholidays.com/ics-all/australia/south-australia) and cleans the event names by removing text in parentheses (like "Regional Holiday" or "Not a Public Holiday").

For example:
- "Adelaide Cup (Regional Holiday)" → "Adelaide Cup"
- "Mother's Day (Not a Public Holiday)" → "Mother's Day"

## Features

- Downloads the SA holidays calendar automatically
- Cleans up event names for cleaner display
- Maintains all original formatting and attributes
- Updates quarterly via GitHub Actions
- Sends notifications on success/failure (optional)

## How It Works

The script runs automatically through GitHub Actions at the beginning of each quarter (January, April, July, October) at 10:30 AM Adelaide time, accounting for daylight saving time.

When it runs:
1. It downloads the latest calendar from officeholidays.com
2. Cleans up the event names
3. Saves the updated ICS file
4. Commits the changes back to the repository

## Using the Calendar

You can subscribe to this calendar in your preferred calendar application by using the raw URL:
```
https://raw.githubusercontent.com/BludReaver/sa-public-holidays/main/sa_public_holidays.ics
```

### In Google Calendar:
1. Click the "+" next to "Other calendars"
2. Choose "From URL"
3. Paste the raw URL above
4. Click "Add calendar"

### In Outlook:
1. Go to Calendar
2. Click "Add calendar" > "Subscribe from web"
3. Paste the raw URL above
4. Click "Import"

### In Apple Calendar:
1. Click "File" > "New Calendar Subscription"
2. Paste the raw URL above
3. Click "Subscribe"

## Setting Up Your Own Version

1. Fork this repository
2. (Optional) Set up Pushover API keys for notifications:
   - Create a [Pushover](https://pushover.net/) account
   - Create an application to get an API token
   - Add secrets to your repository:
     - `PUSHOVER_USER_KEY`
     - `PUSHOVER_APP_TOKEN`

3. The GitHub Action will run automatically according to the schedule

## Local Development

To run this script locally:

```bash
# Install dependencies
pip install requests httpx

# Run the script
python update_sa_holidays.py
``` 