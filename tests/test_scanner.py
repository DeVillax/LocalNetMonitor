import unittest
from notifications import Email
from scanner import write_device
from scanner import is_new_host
from scanner import notification
from scanner import has_status_changed


class TestScanner(unittest.TestCase):

	def setUp(self):
		self.host = {
					"hostnames": [{"name": "test_host"}],
					"addresses": {"mac": "test_mac", "ipv4": "test_ip"},
					"status": {"state": "up"},
					"vendor": {}
					}
		self.document = "test_hosts.txt"

	def test_write_device(self):
		"""
		Test if a host is written into the text file.
		"""
		write_device(self.document, self.host)
		with open(self.document) as document:
			self.assertEqual(self.host["addresses"]["ipv4"], document.readline().split(",")[0])

	def test_is_new_host(self):
		"""
		Test if a host is new.
		"""
		macs = ["test_mac2"]
		new_host = {"addresses": {"mac": "test_mac3"}}
		existing_host = {"addresses": {"mac": "test_mac2"}}

		self.assertTrue(is_new_host(new_host, macs))
		self.assertFalse(is_new_host(existing_host, macs))

	def test_notification(self):
		"""
		This test passes if the notification is successfully sent.
		"""
		subject = "Test"
		recipient = "testingdevelopmentemail@gmail.com"
		content = "test2"
		notification(subject, recipient, content)

	def test_has_status_change(self):
		"""
		Verify if the status of a given mac changes on the file
		"""
		mac = "test_mac2"
		state = "down"
		has_status_changed(mac, state, self.document)
		with open(self.document) as document:
			for line in document:
				if mac in line:
					self.assertIn(state, line)
					break
		has_status_changed(mac, "up", self.document)


if __name__ == '__main__':
	unittest.main()
