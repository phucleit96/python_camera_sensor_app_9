# Import necessary libraries
import smtplib
import ssl
import os
from email.message import EmailMessage
import imghdr

# Define SMTP server details
host = "smtp.gmail.com"
port = 465

# Define sender and receiver email addresses
username = "badboy27796@gmail.com"
password = os.getenv("PASSWORD")  # Get the password from environment variable
receiver = "phuc.le.it96@gmail.com"

# Create a secure SSL context
context = ssl.create_default_context()


# Function to send an email with an image attachment
def send_email(image_path):
    print("Send mail started")

    # Create a new EmailMessage object
    email_message = EmailMessage()

    # Set the email subject
    email_message['Subject'] = "New Humanoid Showup!"

    # Set the email content
    email_message.set_content("New People got caught in the webcam!")

    # Open the image file in binary mode, read it, and attach it to the email
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, msg=email_message.as_string())
    print("Email ended")


# If this script is run directly, send an email with a specific image
if __name__ == "__main__":
    send_email("images/260.png")