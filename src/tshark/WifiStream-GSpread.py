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
priKey = u"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCtTVbUg9IIV+hS\n0bROSZca3FMA5ffbJCSBf19/k4K1I7rEZ4SS8L6AogkpD5YMNs0YTo45nmKjAmPn\nuHIcKwmqYhHWhW79Ov+MT0YOlFb3iNupcrzKNktGeqfD1osYFb8y1FP04yFol+nn\nSLjfAYjzRl/eZ0+YaTSbQxI4LUyEm1Pc7nT3ERohny7yOd7EwG0FnqmdGU9cxmzz\ni1BRnZY/25VfsiAciZsI5LMq6LKLTps3gmKsecKPqImu5KqyVdpEuHvdnJ61Yxj2\n6U0IOi00O1FbOSXJU9jZthuZy+eFiKkF3jS3i2nSAwuMCbyoHfV+Y5NCd/ZNrHWn\nTqwNkm1lAgMBAAECggEASXi+5bUHL/tY5ve56fDgC4a59+kHRhRSF8aw7YzTvsjp\njwfWGFfRZAaOPKa7de0r0XDIclwYNES4p042roN+gwo1xs1mKxy+p7UaHec84Y/X\nlMSsjkwraLNqeaf0616Y40tKVsmOaeHxy9i0a/MiJQVCcq84+wQrReHPERr/VD4z\nlYx3kwY6knoSjx3pO9P5OBn0tyS4JQ+P4QtdKQYSkeV66qBAcz2UZLfJP0CO6HyT\nmiCCCGd+3ZtSZKGpDKSh9nJDw/NLRWGDghwj9KJaU1Cwl82eBkxa/xHxj3PtsG3P\nYAqlcYqNZ6ZAZmSSG8T6YDeioKzXorcTOj1pwkmcNwKBgQDygkRb8epwKfHwtnWN\nmrbroI18w6lVlhjvXNsxoOYTuxNYsloqWtJ1TxYp/GE3gHwwF40VF4R6LiefQucT\n4ZrNTCs0YxCQOdUl9Gav9lqxrToqj9a1/qNJE+eGZYwb36ZzkLbHsvSsWCQjQJ2y\nyvnjKzpVLNNyCPVRivNBX1x4EwKBgQC28XOxoxhlQP+jDH3EwgoV4hsFlFD5KldV\nSo1mh/ZRujnniB0iS8+mcH7qVzIsaC0O3+vnTiLf5VGTStDfftGN6F2kXrUHNhuQ\n4J2xNWX/1Lj2ZjJrs51q036cV1N9FoyzxUR9ptMu1yZFrx6xisc5G8EFuvJ543nW\nd9D4eoSjpwKBgBYII7G+vq/F/8cArJlazveFNJV7KS0vX8CPTRKrLXvpaQ6L1Yk3\nixtBPiA+X46tS5sK6LRb2JtJCix75YZ23pt8KgiuX1jbCDRUiee+l+rAdCJdwwHx\nyl/fQQ+CtkHqBbNGGHT4GyZ1M4NIYYtWyXEMAlaupd8cVT09RHBR+5KlAoGARMRw\nQ9bV5cHQFj8sy5hQ6DbtB2TgJzkmSPZUPrVe/wusln7QzMKIlLz2yCnsv0qNnWjI\nqVLywwzVZDOcXlayeNBe2tmK3OIW7JeyTxmOdONGf8CctWV4B97mWehthrjCPRUr\nELxz58iSJ2GTfRN4ndvz666BVRYQB3FUiQKs90MCgYEAmYHTBY6svGNJ82AErSeP\n3E8OWVq9C/ntR8lZb2e8K/l59/IwZkJbcIy9STWzebSN5R3Sh0S3HzV2b4hQVLC+\n3k+tprXLYMOovcjAt9446dhWxT0T8ylrDESRK9+V7lqcFMsGxM/kGHRxlw7V0acm\n/PHkLvNqWQfxx6MiFYFvut4=\n-----END PRIVATE KEY-----\n".encode('utf8')

# Filename of JSON credentials (replace with your own)
GDOCS_OAUTH_JSON       = 'uabb2017-638163c8e4c1.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'uabb2017'

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
