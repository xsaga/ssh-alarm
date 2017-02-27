# ssh-alarm
Control SSH access attempts and send results via email. Find connected IP geolocation.

## Python files included in this project

* **gemail.py**: Module to send emails from a Gmail account using smtplib. In order to make it work, you must create a file named '.gmail_login' in the same directory and include your Gmail address in the first line and the password in the second line. Then enable 'less secure apps' or if your Gmail account uses 2FA create an app password and use it in the '.gmail_login' file. 

* **ipinfo.py**: Module to find the geolocation of an ip address using the *freegeoip.net* public API.

* **sshlog.py**: Reads the '/var/log/auth.log' file and filters the relevant SSH entries. The output goes to 'sshlog.html'. Each entry in that file is color-coded depending on the severity of the log and includes the geolocation of the IP address. Then it sends 'sshlog.html' via email. This program also creates the file '.ipdb'. It includes all the IP addresses that connected (or tried to connect) to your computer. Color code:
 * red: Accepted user and password from a public IP address.
 * orange: Accepted user and password from a private IP address (LAN).
 * yellow: Failed connection from a valid user name.
 * blue: Failed connection from an invalid user name.

* **getip.py**: Program to get the public IP address of your computer and send it to your Gmail account. Useful if you want to connect remotely to your computer when your ISP gives you a dynammic IP address. It also creates the file '.pubiplist' that contains all the public IP addresses assigned to your computer.

## Example output
Gmail renders it with color.
```html
<p><font color="blue">Apr 19 19:18:55 raspberrypi sshd[845]: Failed password for invalid user abcd from 192.168.0.21 PRIVATE</font><p>
<p><font color="gold">Apr 19 19:51:23 raspberrypi sshd[1111]: Failed password for pi from 192.168.0.21 PRIVATE</font><p>
<p><font color="darkorange">Apr 19 19:51:32 raspberrypi sshd[1111]: Accepted password for pi from 192.168.0.21 PRIVATE</font><p>
<p><font color="blue">Apr 21 07:14:36 raspberrypi sshd[848]: Failed password for invalid user 1234 from 103.XXX.XXX.XXX Vietnam, city: Hanoi</font><p>
<p><font color="red">Apr 21 11:50:19 raspberrypi sshd[2816]: Accepted password for pi from 158.XXX.XXX.XXX Spain, city: Bilbao</font><p>
```
