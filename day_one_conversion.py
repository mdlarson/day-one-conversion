"""Script to convert Day One journal archives JSON to Markdown."""

import json

# Read the JSON file
with open('DayOneArchive.json', 'r', encoding='utf8') as file:
    data = json.load(file)

# Convert JSON entries to Markdown
MARKDOWN_CONTENT = ""

for entry in data['entries']:
    date_line = entry['creationDate']
    journal_entry = entry['text']

    # if 'location' in entry:
    #     city = entry['location']['localityName']
    #     place = entry['location']['placeName']
    #     lat = entry['location']['latitude']
    #     long = entry['location']['longitude']
    #     country = entry['location']['country']
    #     loc_line = f"{place}, {city}, {country}\n{lat}, {long}"
    # else:
    #     pass

    if 'weather' in entry:
        # convert C to F
        wx_temp = ((entry['weather']['temperatureCelsius'] * 9) / 5) + 32
        wx_description = entry['weather']['conditionsDescription']
        wx_line = f"{wx_temp}°, {wx_description}"
    else:
        pass

    if 'tags' in entry:
        tag_list = ', '.join(entry['tags'])
    else:
        pass

    MARKDOWN_CONTENT += f"##{date_line}\n"
    # MARKDOWN_CONTENT += f"##{loc_line}\n"
    MARKDOWN_CONTENT += f"###{wx_line}\n\n"
    MARKDOWN_CONTENT += f"{journal_entry}\n\n"
    MARKDOWN_CONTENT += f"*{tag_list}*\n\n"


# Write Markdown content to a file
with open('journal_entries.md', 'w', encoding='utf8') as file:
    file.write(MARKDOWN_CONTENT)
