'''
Created on Jun 26, 2010

@author: jbrukh

Utility to quickly send emails.
'''
import smtplib
import conf

def send_email( sender, recipients, msg ):
    """Send an email."""
    session = smtplib.SMTP(conf.SERVER)
    session.starttls()
    session.login(conf.SMTP_USER, conf.SMTP_PASS)
    smtpresult = session.sendmail(sender, recipients, msg)
  
    if smtpresult:
        errstr = ""
        for recip in smtpresult.keys():
            errstr = """Could not delivery mail to: %s
  
  Server said: %s
  %s
  
  %s""" % (recip, smtpresult[recip][0], smtpresult[recip][1], errstr)
        raise smtplib.SMTPException, errstr