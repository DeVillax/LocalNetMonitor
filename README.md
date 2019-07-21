# Monitor-Your-Network

Simple script for discovering host on your network and notifiying via email when new devices have connected to, reconnected to or left it.

## 1) Dependencies

* nmap - Nmap is required for discovering assets on your local network.

## 2) How it works
The main idea behind this project is to monitor your local network to check devices connected to it as well as receiving notifications if new devices have been discovered on it.

First time you run "scanner.py" your network will be scanned to establish a baseline of devices currently connected to it. This baseline is used to detect whether new devices are present or if previous devices have left or reconnect to your network. System will notifiy via email upon new devices discovery, devices leaving or getting back online.

Please note that this was created with Raspberry Pi in mind in order to schedule a task that runs the script every 5/10/15 minutes or how often you wish. 

## 3) Quick Start
Simply place "scanner.py" and "notifications.py" on the same folder and run the first script having modified the following lines:

On "main()":
*   nm.scan("YOUR-LOCAL-NETWORK-IP-ADDRESS/SUBNET-MASK", arguments="-sP", sudo=True)   (i.e. "192.168.1.0/24")

On "notifications()":
Either:
* Pass as a sender the emaill address you want to send emails from as well as the password
* If you don't want to hardcode your email credentials, set up two environment variables called "SCANNER_EMAIL" and "SCANNER_KEY"

Congratulations! All set to run it ;)

## 4) Development environment

* Python 3.5
* Raspbian OS

## 5) Reporting issues
If you find bugs, issues, or methods that could be implemented or improved,
please raise them [here](https://github.com/NcVillalobos/DeezPy/issues). Alternatively, you can contact me to my email address
'developmentvilla@gmail.com'

## 6) Feedback 

If this library is helpful for your projects, please don't hesitate reaching out
at 'developmentvilla@gmail.com', any feedback is highly appreciated.


