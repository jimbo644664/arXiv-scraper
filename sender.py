import smtplib

class MailSender:
    header  = 'From: ARXIV Papers Bot <{}>\n'.format(username)
    header += 'To: {} <{}>\n'
    header += 'MIME-Version: 1.0\n'
    header += 'Content-type: text/html\n'
    header += 'Subject: {}\n'
    header += '\n'
    header += '{}\n'
    
    def __init__(self, server, username, password, addresses):
        self.server = server
        self.username = username
        self.password = password
        self.recipients = addresses

    def send_mail(self, subject, text):
        sender = self.username

        sObj = smtplib.SMTP_SSL(self.server)
        sObj.login(self.username, self.password)
        
        for user in self.recipients:
            email = self.__class__.header.format(user[0], user[1], subject, text)
            sObj.sendmail(sender, [user[1]], email)


