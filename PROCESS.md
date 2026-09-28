# Process

## Tools

I used VS Code to edit and inspect the project, PowerShell and `uv` to run the Python scripts, and Git to keep versions of the work. `fetch.py` uses `requests` to download the NASA POWER CSV once. `plot.py` uses Python's built-in `csv` module to read the committed raw file and Matplotlib to create the image.

I also used Codex as a learning and programming assistant. It helped me understand the course commands, diagnose path and package problems, and develop a first version of the radial visualisation. I checked the actual NASA CSV before using the code: its daily records contain year, month, day, and a solar-radiation value. I then reviewed the generated image and asked for concrete changes to its visual hierarchy, including the title spacing and the size of the central label. The final script still reads the raw data locally rather than asking an AI system to invent or replace measurements.

## Kept

I kept the radial calendar idea. A normal line chart showed the values correctly, but it treated the year as a long strip. The circular layout makes the yearly cycle visible: January starts at the top, months progress clockwise, and December returns to the beginning. I kept one ray per day because it retains daily irregularity. I also kept both ray length and colour tied to the same radiation value, so the artwork remains traceable to the data. The subtle rings, month dividers, and colour scale help a reader understand that the image is a calendar rather than a decorative sun.

## Rejected

I rejected the first plain orange line chart. It was useful as an early check that the CSV could be read and plotted, but it did not communicate why sunlight data has an annual rhythm, and it looked too similar to a default chart. I also rejected an early radial version with oversized title text and a centre label that extended beyond its circle. That design made the words compete with the data. I reduced the header, moved the chart down to create a clear title area, and reduced the central text until it fitted inside the circle.
