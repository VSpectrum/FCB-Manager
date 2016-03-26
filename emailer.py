from config import *

def send_email(recipient, subject, body):
    import smtplib

    gmail_user = emailer_ad
    gmail_pwd = emailer_pass
    FROM = emailer_ad
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'Successfully sent mail'
    except:
        print "Failed to send mail"

