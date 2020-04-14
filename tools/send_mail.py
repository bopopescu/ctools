from email.mime.text import MIMEText
import smtplib
import subprocess
import ConfigParser
import sys
import os

#def send_mail(config_file, file_to_send, report_details):
def send_mail(mail_id, subject, content, mail_server='10.204.216.49'):
    smtpServer = mail_server
    smtpPort = '25'
    mailSender = 'contrailbuild@juniper.net'
    mailTo = mail_id

    msg = MIMEText(content, 'html')
    msg['Subject'] = subject
    msg['From'] = mailSender
    msg['To'] = mailTo

    s = None
    try:
        s = smtplib.SMTP(smtpServer, smtpPort)
    except Exception, e:
        print "Unable to connect to Mail Server"
        return False
    s.ehlo()
    try:
        s.sendmail(mailSender, mailTo.split(","), msg.as_string())
        s.quit()
    except smtplib.SMTPException, e:
        print 'Error while sending mail'
        return False
    return True
# end send_mail

if __name__ == "__main__":
    #send_mail('vjoshi@juniper.test','Test Subject', 'Test content') 
    send_mail(sys.argv[1], sys.argv[2], sys.argv[3], '10.84.24.64')
