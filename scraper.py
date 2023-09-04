import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://www.lsa.umich.edu/cg/cg_detail.aspx?content=2460EECS485001&termArray=f_23_2460"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

counter = 0
def send_email_with_hi(Body):
    # Email configuration
    counter += 1
    sender_email = 'matthewzepf15@gmail.com'
    receiver_email = 'mzepf@umich.edu'  # Replace with the recipient's email address
    password = 'youThhought'  # Use an app-specific password or store securely
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # For Gmail's TLS/STARTTLS

    # Create a message
    subject = 'EECS 485 WAITLIST NOTIFICATION'
    body = Body
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())

        # Close the SMTP server connection
        server.quit()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the div with class "hidden-md hidden-lg xs_label" containing waitlist information
    waitlist_div = soup.find("div", class_="hidden-md hidden-lg xs_label")

    if waitlist_div:
        # Extract the waitlist information
        waitlist_info = waitlist_div.find_next("div").text.strip()
        print("Waitlist Information:", waitlist_info)
        waitlist_info = waitlist_div.find_next("div").text.strip()
        print("Waitlist Information:", waitlist_info)
    else:
        print("Waitlist information not found on the page.")
else:
    print("Failed to retrieve the web page. Status code:", response.status_code)

def parse485():
    divs = soup.findAll(class_="hidden-md hidden-lg xs_label")    
    #print all of the contents of a div with class = col-md-1 
    divs = soup.findAll(class_="col-md-1")
    labSeen = False
    for div in divs:
        #print(div.text)
        if ("LAB" in div.text):
            labSeen = True
        if (labSeen):
            parseText(div.text)

# this should parse the text of the divs that have the class = col-md-1 and should check for a LAB with open seats of >=1 or a waitlist <= 2 and if so should send an email to the mzepf@umich.edu
def parseText(text):
    if ("Open Seats:" in text):
        for word in text.split():
            if (word.isdigit() and int(word) >= 1):
                send_email_with_hi(f'Open Seats: {word}')
    elif("Wait List:" in text):
        for word in text.split():
            if (word.isdigit() and int(word) <= 2):
                send_email_with_hi(f'Wait List: {word}')

# run this following script every minute or so
while (counter < 10):
    parse485()
    time.sleep(60)