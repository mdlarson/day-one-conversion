"""Script to convert Day One journal archives from JSON to HTML/PDF."""

import json
import re
from datetime import datetime
from weasyprint import HTML

# Define regex to find unused image references
# example: ![](dayone-moment:\/\/C5B5BC18EEB544D8A8D6F81A4B510B09)\n\n
image_pattern = re.compile(
    r'^\s*!\[\]\(dayone-moment:\/\/[A-Z0-9]{32}\)\n*$', re.MULTILINE)
p_break = re.compile(r'<p>\s*<br\s*/?>')

# Initialize HTML document as list of entries
html_parts = [
    """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Journal Entries</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    """
]

# Read the JSON file
with open('DayOneSample.json', 'r', encoding='utf8') as file:
    data = json.load(file)

# Iterate over entries, parse data, append to list
for entry in data['entries']:
    # convert datetimes
    raw_date = datetime.strptime(entry['creationDate'], '%Y-%m-%dT%H:%M:%SZ')
    date_line = raw_date.strftime('%A, %B %d, %Y at %I:%M%p')

    # use regex to remove image references
    journal_entry = image_pattern.sub("", entry['text'])

    # process text to remove extraneous newlines
    journal_entry = journal_entry.replace('\n\n', '</p><p>')
    journal_entry = journal_entry.replace('\n', '<br>')
    journal_entry = journal_entry.replace('<br><br><br><br>', '<br>')
    journal_entry = journal_entry.replace('<br><br><br>', '<br>')
    journal_entry = journal_entry.replace('<p><br>', '<p>')

    # parse location data
    location_info = entry.get('location', {})
    city = location_info.get('localityName', 'Unknown')
    place = location_info.get('placeName', 'Unknown')
    lat = location_info.get('latitude', 0)
    long = location_info.get('longitude', 0)
    country = location_info.get('country', 'Unknown')

    # parse weather data
    weather_info = entry.get('weather', {})
    wx_temp = ((weather_info.get('temperatureCelsius', 0) * 9) / 5) + 32
    wx_description = weather_info.get(
        'conditionsDescription', 'No weather data')
    wx_line = f"{wx_temp}°F, {wx_description}"

    # fetch the tags
    tags = ', '.join(entry.get('tags', []))

    # append HTML entry + metadata to list
    html_parts.append(f"""
<div class="journal-entry">
    <div class="entry-metadata">
    <h3>{date_line}</h3>
    <p class="geo">☉ {wx_line}</p>
    <p class="geo">⌂ {place}, {city}, {country}</p>
    <p class="geo">☷ {lat}, {long}</p>
    <p class="tags">༶ {tags}</p>
    </div>
    <div class="entry-content">
    <p>{journal_entry}</p>
    </div>
</div>
    """)

# Close and assemble the HTML entries
html_parts.append("""
</body>
</html>
""")

html_content = ''.join(html_parts)
html_content = p_break.sub('<p>', html_content)

# Write entries to HTML file and generate PDF
with open('sample.html', 'w', encoding='utf8') as file:
    file.write(''.join(html_content))

HTML('sample.html').write_pdf('sample.pdf')