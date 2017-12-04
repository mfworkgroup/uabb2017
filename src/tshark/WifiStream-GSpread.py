#!/home/pi/bin/python

import ssl
import json
import sys
import time
import datetime
import os
import gspread
import subprocess
from oauth2client.client import SignedJwtAssertionCredentials

#gspreads private key (replace with your own)
priKey = u"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCaEiEYkO1dD2T1\nhoA19f2rXk6OGgH+l+hhW5wnUxr/vhL8Vk2kuIWqJK9ze1kq6liiVRzNW1ZfjDdf\nUZMqUBHp87aq6sA4CDLXkUNDdpcsMvF38ORzzzGNguo4zntUfx87u5sncgxzw0ow\nhSHkHg/2tQvoms5sf/UWq4bpf1m6fjRdhQPEk3sG7H1ZIqhf+aEOAw2IGN3m7T0i\nBfGDKq00uVuh+LD/r33Ojt/r4ys6HHTcd4hRpM2xcQGhJnH5oROqT2e3+pSWHsS7\n0q0wOO+ZWHBY0n06g00abkfA5KROoN4tcgjb4E1SjX65Sz6/Yv2VzhEcZGOeBNDh\nL/aycK5XAgMBAAECggEAKmQylv/JT4Gc1bFcNXypfy1Dj/W39sT1O1Rpcqh7FULH\nFobodhoPLPFLFQsrTZONL50bf6VR7pg15BQd2daOF0DnUb+lg8U9t/JP/4/xqEec\nCNRPB05K5BTRPTAS3vzbKyRDXGcU5gUltJPs70cWPVszG5z8jv3mAYbQaA6SMa16\nkPpeXFpNiIRLErxZo921Jm8vNT2nQwrF3ZaOJGtfP5AGD1iyB062/hudtKnYg1Ps\nVofY1ukxFECGGz29C8rYHZeAtLvYQ9yYLs6DSIYAr1JHxGNIiYFLsiQzBaJdb1bw\n+634aE7OD/bfnLkqSCEfWi0kNayebNJ4ag6lxmiZgQKBgQDHVVAf7ZmqSQBgoWbL\np86bxuVIpiK350CJhyQpTjwxQaU4GfxsNZcXVy0IQlPxIMVeqlbb3RRp6fhtgI+7\nxmsZm6s6N4C8AlGxtlFivdc5E1qyFGv3Bx/szi9EEI0NUpmh5+969WWr263P5tKU\nGzZfXh+xaK+8Apsq0MUm/g1xqwKBgQDF3suAQHp4Vv8kV1Ds2BeVr/+0dwSCNmOo\nz2eikifmyGJtIyXRZXTgCaGBHRKPjFRdmaY/cKxxcc/ijgVxsSsEnRIkskVqo9wf\nWl1fBIkbTZ2OsqOr9Bm0hbePBThtKhPzi7b35BrozrYewcPBHGcd8YqBvBk5iBeS\nlBCibf5iBQKBgQCKJYo+VoElDyr/zVxc0JPUSmgljV6Kbe7AYbSiG+KDkKdc1kWn\nCQ0J1BUVoEJk3v1qukswXWwEa28NFQiIbt9TBBwLYOQLaOANdfm5oTBEEjHNMXIR\n5hIuIEeJuJ7JGPH4z7GdWe14yesQJzzSAHoSZj04ywDgID5B0iaQ+4l9uQKBgHZ6\nHa2QbgRqSuEuqxT1msGVHW2oKfnxqSCl926/RscHyu+AMR+9OQsAmUSe7MMpCkb1\nPjcUNxzCQfBsi1P0+kYL6pYwbCIbNS1MxUWkiJfhlGqiCiBmy5Fs02j+fjfXDxUv\n3gF2AqrNQv0NljGl2RRz0TQ3NX9ePocUwxUO+VclAoGAYlAAkgaq97DcLfvKzvUi\nvW50/M01EB92KppJ3KMCEVs+r31JLkwaaz234dk7zC7BCoyM6ik+VJEg8tH3I5/h\nHwp3GvK3LKShfEndWZKXeuVXBchhbjd+AolOgGiKJqTWXvDGrptS21bFeUfbZPwe\ncwoYViXTv3jJ7qtxZ06bgw4=\n-----END PRIVATE KEY-----\n".encode('utf8')

# Filename of JSON credentials (replace with your own)
GDOCS_OAUTH_JSON       = 'MotionLogger-f413871c4712.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'Motion Logger'

# Function to login into the spreadsheet
def login_open_sheet(oauth_key_file, spreadsheet):
        """Connect to Google Docs spreadsheet and return the first worksheet."""
        #try:
        json_key = json.load(open(oauth_key_file), strict = False)
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], priKey, ['https://spreadsheets.google.com/feeds'])

        gc = gspread.authorize(credentials)
        worksheet = gc.open(spreadsheet).sheet1
        return worksheet

# Tshark packet sniffer
def sniffer(cmd):
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	out = proc.stdout.readlines()
	return out

print 'Press Ctrl-C to quit.'
worksheet = None
while True:
        # Login if necessary.
        if worksheet is None:
                worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)

        # Start packet sniffing
	packet = sniffer("sudo tshark -i wlan1 -f \"subtype probereq\" -T fields -e wlan.sa_resolved -e wlan.sa -e radiotap.dbm_antsignal -e wlan_mgt.ssid -E separator=\',\' -a duration:5")
        # Append the data in the spreadsheet, including a timestamp
        for line in packet:
		worksheet.append_row((datetime.datetime.now(), line))
