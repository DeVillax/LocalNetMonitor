import smtplib
import ssl
import re
import os


class NotValidEmailAddress(Exception):
    pass


class Email:
    
    def __init__(self, port, server, sender, password):
        self.port = port
        self.server = server
        self.sender = sender
        self.password = password

    def send_email(self, subject, recipient, content):
        """
        Send an email to a given address.
        
        :param subject: subject of the email 
        :param recipient: destination email address
        :param content: content of the email
        
        """
        message = 'Subject: {}\n\n{}'.format(subject, content)
        context = ssl.create_default_context()
        try:
            if not self._check_email(receipient) or not self._check_email(self.sender):
                raise NotValidEmailAddress
                
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls(context=context)
                server.login(self.sender, self.password)
                server.sendmail(self.sender, recipient, message)
        except smtplib.SMTPAuthenticationError:
            print("Error: There was a problem authenticating the sender email address.")
        except NotValidEmailAddress:
            print("Error:  Email address is not valid. Please verify the sender and recipient.")
        except smtplib.SMTPResponseException:
            print("Error: The password provided is not valid.")
            
    def _check_email(self, email):
        """
        Checks if a given email address is valid. Please note that this
        method doesn't verify whether the email exists.
        
        :param email: email address
        :return: True or False
        """
        expression = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if email and expression.match(email):
            return True
