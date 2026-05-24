import subprocess
import time
import urllib.parse

def navigate_to(place):

    destination = urllib.parse.quote(place)

    url = (
        f"https://www.google.com/maps/dir/?api=1"
        f"&destination={destination}"
        f"&travelmode=walking"
    )

    process = subprocess.Popen([
        "chromium",
        "--kiosk",
        "--noerrdialogs",
        url
    ])
