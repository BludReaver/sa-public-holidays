import re

def clean_event_name(summary: str) -> str:
    return re.sub(r"\s*\([^)]*\)", "", summary).strip()

# Sample ICS content with SUMMARY lines
sample_content = """BEGIN:VEVENT
CLASS:PUBLIC
UID:2025-03-10AU-SA2regregion@www.officeholidays.com
CREATED:20250406T210925Z
DESCRIPTION: South Australia Only. The cup has been held on the second Monday of March since March 2006. Before 2006 it was held in May\\n\\n2nd Monday in March. SA Only\\n\\nInformation provided by www.officeholidays.com
URL:https://www.officeholidays.com/holidays/australia/south-australia/adelaide-cup
DTSTART;VALUE=DATE:20250310
DTEND;VALUE=DATE:20250311
DTSTAMP:20080101T000000Z
LOCATION:South Australia
PRIORITY:5
LAST-MODIFIED:20230724T000000Z
SEQUENCE:1
SUMMARY;LANGUAGE=en-us:Adelaide Cup (Regional Holiday)
TRANSP:OPAQUE
X-MICROSOFT-CDO-BUSYSTATUS:BUSY
X-MICROSOFT-CDO-IMPORTANCE:1
X-MICROSOFT-DISALLOW-COUNTER:FALSE
X-MS-OLK-ALLOWEXTERNCHECK:TRUE
X-MS-OLK-AUTOFILLLOCATION:FALSE
X-MICROSOFT-CDO-ALLDAYEVENT:TRUE
X-MICROSOFT-MSNCALENDAR-ALLDAYEVENT:TRUE
X-MS-OLK-CONFTYPE:0
END:VEVENT"""

print("Original content excerpt:")
print("-" * 80)
print(sample_content)
print("-" * 80)

# Process the content - FIXED to handle SUMMARY with attributes
cleaned_lines = []
for line in sample_content.splitlines():
    if line.startswith("SUMMARY"):
        # Find the position of the colon that separates the attribute from the value
        colon_pos = line.find(":")
        if colon_pos > -1:
            # Extract everything before the colon (including the colon)
            summary_prefix = line[:colon_pos+1]
            # Extract everything after the colon (the summary value)
            summary_value = line[colon_pos+1:]
            # Clean the summary value
            cleaned_summary = clean_event_name(summary_value)
            # Reconstruct the line
            clean_line = f"{summary_prefix}{cleaned_summary}"
            cleaned_lines.append(clean_line)
        else:
            # If no colon is found (shouldn't happen), keep the line as is
            cleaned_lines.append(line)
    else:
        cleaned_lines.append(line)

cleaned_content = "\n".join(cleaned_lines)

print("\nCleaned content excerpt:")
print("-" * 80)
print(cleaned_content)
print("-" * 80)

# Check if SUMMARY line is in the original format
print("\nChecking for original summary format:")
if "SUMMARY;LANGUAGE=en-us:Adelaide Cup (Regional Holiday)" in sample_content:
    print("Found original format: SUMMARY;LANGUAGE=en-us:Adelaide Cup (Regional Holiday)")
else:
    print("Could not find original format")

# Check if SUMMARY line is in the cleaned format
print("\nChecking for cleaned summary format in cleaned content:")
if "SUMMARY;LANGUAGE=en-us:Adelaide Cup" in cleaned_content:
    print("Found cleaned format: SUMMARY;LANGUAGE=en-us:Adelaide Cup")
elif "SUMMARY:Adelaide Cup" in cleaned_content:
    print("Found cleaned format: SUMMARY:Adelaide Cup")
else:
    print("Could not find cleaned format") 