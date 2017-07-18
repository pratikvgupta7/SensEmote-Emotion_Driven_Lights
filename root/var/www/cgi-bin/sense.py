#!/usr/bin/python
import cgi,cgitb,subprocess
def isNotEmpty(s):
	return bool(s and s.strip())

v_network='test'
v_paswd='test'
v_key='test'

form = cgi.FieldStorage()
v_network = form.getvalue('txt_nw')
v_paswd = form.getvalue('txt_pwd')
v_key = form.getvalue('txt_key')
fileOutput = open('/tmp/sense.txt','w')

#fileOutput.write(str(v_network) + '\n')
#fileOutput.write(str(v_paswd) + '\n')
#fileOutput.close

#frd = open('/tmp/sense.txt','r')
#nw = frd.readline().rstrip()
#pswrd = frd.readline().rstrip()
#frd.close
if isNotEmpty(v_network):
	trial = subprocess.Popen(["wpa_passphrase",v_network,v_paswd], stdout=subprocess.PIPE)
	(output, err) = trial.communicate()
	final = open('/etc/wpa_supplicant/wpa_supplicant.conf','w')
	final.write(output.rstrip())
	final.close
if isNotEmpty(v_key):
	keywrite = open('/piemote/mskey','w')
	keywrite.write(v_key.strip())
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>SensEmote</title>"
print "</head>"
print "<body>"
print "<div"
print "style=text-align: center; height: 406px; margin-left: 0px; width: 1089px;><big><big><em><span"
print "style=font-weight: bold;><span"
print "style=font-family: Times New Roman;>Network Registered</span><br"
print "style=font-family: Times New Roman;>"
print "<br>"
print "</span></em><small"
print "style=font-family: Times New Roman; font-style: italic;>Your WiFi network is now registered with SensEmote. Remove the ethernet cable and restart the device<br>"
print "<br>"
print "<br>"
print "</small></big></big>"
print "</div>"
print "</body>"
print "</html>"

