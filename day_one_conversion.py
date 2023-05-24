"""Script to convert Day One journal archives JSON to Markdown."""

import json

# Read the JSON file
with open('DayOneArchive.json', 'r', encoding='utf8') as file:
    data = json.load(file)

# Convert JSON entries to Markdown
MARKDOWN_CONTENT = ""

for entry in data['entries']:
    title = entry['creationDate']
    content = entry['text']
    
    main_entry = f"# {title}\n\n\
                    {content}\n\n"

    if 'weather' in entry:
        # convert C to F
        weather_temp = ((entry['weather']['temperatureCelsius'] * 9) / 5) + 32
        weather_description = entry['weather']['conditionsDescription']
        weather_entry = f"### {weather_temp}°, {weather_description}\n\n"
    else:
        pass

    MARKDOWN_CONTENT += main_entry
    MARKDOWN_CONTENT += weather_entry

# Write Markdown content to a file
with open('journal_entries.md', 'w', encoding='utf8') as file:
    file.write(MARKDOWN_CONTENT)
