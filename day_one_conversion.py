"""Script to convert Day One journal archives JSON to Markdown."""

import json
import re
from datetime import datetime

# read the JSON file
with open('DayOneArchive.json', 'r', encoding='utf8') as file:
    data = json.load(file)

# iterate over entries and add to journal
md_content = ""

for entry in data['entries']:
    # convert datetimes
    # example original: 2014–03–07T22:44:45Z
    raw_date = datetime.strptime(entry['creationDate'], '%Y-%m-%dT%H:%M:%SZ')
    date_line = raw_date.strftime('%A, %B %d, %Y at %I:%M%p')

    # remove images
    # example: ![](dayone-moment:\/\/C5B5BC18EEB544D8A8D6F81A4B510B09)\n\n
    entry_raw = entry['text']
    journal_entry = re.sub(r"\!\[\]\(dayone-moment\:\/\/[A-Z0-9]{32}\)",
                           "",
                           entry_raw)

    # process location data
    if 'location' in entry:
        if 'localityName' in entry['location']:
            city = entry['location']['localityName']
        place = entry['location']['placeName']
        lat = entry['location']['latitude']
        long = entry['location']['longitude']
        country = entry['location']['country']
        loc_line = f"{place}, {city}, {country} ᭼ {lat}, {long}"
    else:
        pass

    # convert weather data
    if 'weather' in entry:
        # convert C to F
        wx_temp = ((entry['weather']['temperatureCelsius'] * 9) / 5) + 32
        wx_description = entry['weather']['conditionsDescription']
        wx_line = f"{wx_temp}°, {wx_description}"
    else:
        pass

    # compile tags
    if 'tags' in entry:
        tag_list = ', '.join(entry['tags'])
    else:
        pass

    # sequence and format entry content
    md_content += f"##{date_line}\n"
    md_content += f"{loc_line}\n"
    md_content += f"{wx_line}\n\n"
    md_content += f"{journal_entry}\n\n"
    md_content += f"༶ *{tag_list}*\n\n"


# write entries to file
with open('journal_entries.md', 'w', encoding='utf8') as file:
    file.write(md_content)
