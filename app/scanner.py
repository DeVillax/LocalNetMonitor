import nmap
import os
from notifications import Email


def write_device(document, host):
	"""
	Add the device to the txt file.
	
	:param document: name of the file
	:param host: Dictionary of the host obtained from nmap
	"""
	with open(document, "a+") as txt:
		hostname = host["hostnames"][0]["name"] 
		vendor = "N/A"
		mac = "N/A"
		user = "Unknown"
		address = host["addresses"]["ipv4"]
					
		if hostname == "":
			hostname = "N/A"
					
		if "mac" in host["addresses"]:
			mac = host["addresses"]["mac"]
					
		if len(host["vendor"]) != 0:
			vendor = host["vendor"][mac]
					
		state = host["status"]["state"]
		line = [address, hostname, mac, state, vendor, user]
		txt.write(",".join(column for column in line) + "\n")


def is_new_host(host, macs):
	"""
	Checks whether a given host is new on the network
	
	:param host: Dictionary of the host obtained from nmap
	:param macs: List with MAC addresses stroed on the txt file
	
	:return: True or False
	"""
	new = False
	if "mac" in host["addresses"]:
		mac = host["addresses"]["mac"]
		if mac not in macs:
			new = True
	return new


def notification(subject, recipient, content, sender=None, pwd=None):
	"""
	Send an email to a given address.
	:param subject: subject of the email
	:param recipient: destination email address
	:param content: content of the email
	:param sender: sender email address
	:param pwd: sender email address's password
	"""

	if not sender:
		sender = os.environ.get("SCANNER_EMAIL")
			
	if not pwd:
		pwd = os.environ.get("SCANNER_KEY")
			
	email = Email(587, "smtp.gmail.com", sender, pwd)
	email.send_email(subject, recipient, content)


def has_status_changed(mac, state, document):
	"""
	Checks whether the state of the device has changed. In other words,
	checks whether the device is connected to or disconnected of the network
	It modifies the txt file.
	
	:param mac: MAC address of the host you are checking.
	:param state: New state of the host
	:param document: name of the txt file
	
	:return: True or False
	
	"""
	status = {"up", "down"}
	modified = False
	if state.lower() in status:
		with open(document, "r+") as txt:
			lines = txt.readlines()
			txt.seek(0)
			for line in lines:
				if mac in line:
					status.discard(state)
					opposite = list(status)[0]
					if opposite in line:
						sub = line.replace(opposite, state)
						txt.write(sub)
						modified = True
					else:
						txt.write(line)
				else:
					txt.write(line)
			txt.truncate()
	else:
		print("The given status is not correct.")
	return modified


def main():
	filename = "hosts.txt" 		
	nm = nmap.PortScanner()
	nm.scan("YOUR-LOCAL-NETWORK-IP-ADDRESS/SUBNET-MASK", arguments="-sP", sudo=True)  # Perform a ping sweep of your network
	try:
		document = open(filename)
	except FileNotFoundError:
		# This will only be executed the first time you launch this code 
		# and will set the baseline of devices connected to your network
		for host in nm.all_hosts():
			write_device(filename, nm[host])
	else:
		lines = document.readlines()
		macs = [mac.split(",")[2] for mac in lines]
		document.close()
		
		new_devices = []
		reconnected_devices = []
		left_devices = []
		
		for host in nm.all_hosts():
			if is_new_host(nm[host], macs):
				write_device(filename, nm[host])
				new_devices.append("{host}, {hostname}, {mac}".format(host=host, hostname=nm[host].hostname(), mac=nm[host]["addresses"]["mac"]))
			else:
				if "mac" in nm[host]["addresses"]:
					mac = nm[host]["addresses"]["mac"]
					macs.remove(mac)
					if has_status_changed(mac, "up", filename):
						reconnected_devices.append("{host}, {hostname}, {mac}".format(host=host, hostname=nm[host].hostname(), mac=nm[host]["addresses"]["mac"]))

		macs.remove("N/A")	

		if len(macs) != 0:
			for mac in macs:
				if has_status_changed(mac, "down", filename):
					for line in lines:
						data = line.split(",")
						if mac in data:
							left_devices.append("{host}, {hostname}, {mac}".format(host=data[0], hostname=data[1], mac=mac))

		recipient = ""
		# Send notification if new devices have connected to your network
		if len(new_devices) != 0:
			notification("New devices on your network", recipient, "\n".join(new_devices))
		
		# Send notification if devices, which were previously connected to your network and left it, are online again.
		if len(reconnected_devices) != 0:
			notification("Devices reconnected to your network", recipient, "\n".join(reconnected_devices))
		
		# Send notification if devices have left your network.
		if len(left_devices) != 0:
			notification("Devices left your network", recipient, "\n".join(left_devices))
	
			
if __name__ == '__main__':
	main()

