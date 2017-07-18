#!/usr/bin/python

import cgi
form = cgi.FieldStorage()
with open ('/www-sense/sense.txt','w') as fileOutput:
	fileOutput.write(form.getValue('txt_nw'))
	fileOutput.write(form.getValue('txt_pwd'))
	fileOutput.write(form.getValue('txt_key'))
