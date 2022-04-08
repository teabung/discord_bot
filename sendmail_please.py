import os #We can create an environmental variable with this module.
from dotenv import load_dotenv
import smtplib

load_dotenv()
EMAIL_ADDRESS = os.getenv('USER')
EMAIL_PASSWORD = os.getenv('PASS')

#This is context manager. I don't know how this works so lets take a tutorial later!
def Error_Catch(input1):
    with smtplib.SMTP('smtp.gmail.com', 587) as smpt:
        smpt.ehlo() #Identifies ourselves with the mail server that we're using
        smpt.starttls() #encrypt our traffic
        smpt.ehlo() #reidentifies after encrypting traffic

        smpt.login(EMAIL_ADDRESS, EMAIL_PASSWORD) #login to the mail server -> we can put our email addresses and passwords but its best to use them in an environmental variable to keep them secured.

        subject = 'Hello!'
        body = 'Error input: ', input1

        msg = f'Subject: {subject}\n\n{body}'

        smpt.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)