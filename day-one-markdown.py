import json

# Read the JSON file
with open('20201124-DayOne.json', 'r') as file:
    data = json.load(file)

# Convert JSON entries to Markdown
markdown_content = ""

for entry in data['entries']:
    title = entry['creationDate']
    content = entry['text']
    
    
    # Check if 'photos' key exists
    if 'photos' in entry:
        photo_identifier = entry['photos'][0]['identifier']
        main_entry = f"## {title}\n\n{content}\n\n![{photo_identifier}](dayone-moment://{photo_identifier})\n\n"
    else:
        main_entry = f"## {title}\n\n{content}\n\n"
    
    if 'weather' in entry:
        weather_temp = ((entry['weather']['temperatureCelsius'] * 9) / 5) +32 # convert C to F
        weather_description = entry['weather']['conditionsDescription']
        weather_entry = f"# {weather_temp}°, {weather_description}\n\n"
    else:
        pass

    markdown_content += main_entry
    markdown_content += weather_entry

# Write Markdown content to a file
with open('journal_entries.md', 'w') as file:
    file.write(markdown_content)
