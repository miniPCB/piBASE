import calendar
from datetime import datetime

def generate_html_calendar(year, month):
    # Get the current day
    today = datetime.now().day if datetime.now().month == month and datetime.now().year == year else None

    # Create a Calendar object
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    
    # Generate the month's calendar as HTML
    html_calendar = cal.formatmonth(year, month)

    # Highlight the current day by adding a class to it
    if today:
        html_calendar = html_calendar.replace(f'>{today}<', f' class="today">{today}<')

    # Generate the full HTML page
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{calendar.month_name[month]} {year} Calendar</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                width: 14.28%;
                border: 1px solid #000;
                padding: 10px;
                text-align: center;
                cursor: pointer;
                height: 100px;
            }}
            td {{
                position: relative;
            }}
            .event {{
                position: absolute;
                bottom: 5px;
                left: 5px;
                right: 5px;
                background-color: yellow;
                font-size: 12px;
                padding: 2px;
            }}
            .today {{
                background-color: lightgreen;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>{calendar.month_name[month]} {year}</h1>
        <div>
            {html_calendar}
        </div>

        <script>
            // Function to handle double click on a date cell
            document.addEventListener('dblclick', function(event) {{
                if(event.target.tagName === 'TD' && event.target.innerText.trim() !== '') {{
                    let eventText = prompt('Add an event:');
                    if(eventText) {{
                        let eventDiv = document.createElement('div');
                        eventDiv.className = 'event';
                        eventDiv.innerText = eventText;
                        event.target.appendChild(eventDiv);
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    return html_content

# Set the current year and month
now = datetime.now()
year = now.year
month = now.month

# Generate the HTML for the current month's calendar
html_calendar = generate_html_calendar(year, month)

# Save the generated HTML to a file
with open("calendar.html", "w") as file:
    file.write(html_calendar)

print("Calendar HTML file generated: calendar.html")
