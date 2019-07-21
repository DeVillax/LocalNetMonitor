import unittest
from notifications import Email, NotValidEmailAddress
import os


class TestNotifications(unittest.TestCase):
	
	def setUp(self):
		sender = ""
		pwd = ""
		
		if os.environ["EMAIL_DEVELOPMENT"]:
			sender = os.environ.get("EMAIL_DEVELOPMENT")
			
		if os.environ["EMAIL_KEY"]:
			pwd = os.environ.get("EMAIL_KEY")
			
		self.email = Email(587, "smtp.gmail.com", sender, pwd)
		self.subject = "Test"
		self.content = "test"
	
	def test_send_email(self):
		"""
		Test if emails are sent. If the server doesn't report an error, this
		case is considered successful.
		"""
		recipient = "testingdevelopmentemail@gmail.com"
		self.email.send_email(self.subject, recipient, self.content)


if __name__ == '__main__':
	unittest.main()
