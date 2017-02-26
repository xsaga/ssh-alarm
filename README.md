# ssh-alarm
Control SSH access attempts and send results via email. Find connected IP geolocation.

## Python files included in this project

* **gemail.py**: Module to send emails from a Gmail account using smtplib. In order to make it work, you must create a file named '.gmail_login' in the same directory and include your Gmail address in the first line and the password in the second line.

* **ipinfo.py**: Module to find the geolocation of an ip address using the *freegeoip.net* public API.

* **sshlog.py**: Reads the '/var/log/auth.log' file and filters the relevant SSH entries. The output goes to 'sshlog.html'. Each entry in that file is color-coded depending on the severity of the log and includes the geolocation of the IP address. Then it sends 'sshlog.html' via email. This program also creates the file '.ipdb'. It includes all the IP addresses that connected (or tried to connect) to your computer.     

Color code:
	* red: Accepted user and password from a public IP address.
	* orange: Accepted user and password from a private IP address (LAN).
	* yellow: Failed connection from a valid user name.
	* blue: Failed connection from an invalid user name.
* **getip.py**: Program to get the public IP address of your computer and send it to your Gmail account. Useful if you want to connect remotely to your computer when your ISP gives you a dynammic IP address. It also creates the file '.pubiplist' that contains all the public IP addresses assigned to your computer.
