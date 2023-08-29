# Sending a basic Email

import smtplib
import ssl



# -- Reading in Adress and Password -- #
with open("/home/tom/Desktop/email.txt") as file:

    for i, line in enumerate(file):
        if i == 0:sender = line.strip()
        elif i == 1:reciever = line.strip()
        else:passw = line.strip()

message = f"""\
Subject: Python

This email was sent by python!

"""

port = 465
context = ssl.create_default_context()

with smtplib.SMTP_SSL("imap.dreamhost.com", port, context=context) as server:
    server.login(sender, passw)
    server.sendmail(sender, reciever, message)

print("sent email")