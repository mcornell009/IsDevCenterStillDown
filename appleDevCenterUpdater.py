#!/usr/bin/python

'''
Mike Cornell 2013, MIT License - idefc go nuts

remember to revise the email params with your own stuff
'''
import urllib
from time import sleep
from email.mime.text import MIMEText
import re
import smtplib
import sys


#edit me!!!
sender = 'me@whatever.com'
pw = 'password_is_a_bad_pw'
receivers = [sender,'my_team@mydomain.com']
#----------

devcenter_url = "https://developer.apple.com/support/system-status/"
statuses = dict()

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def getStatuses():
	content = urllib.urlopen(devcenter_url).read()
	start = content.index("<table")
	end = content.index("</table>")
	table = content[start:end]
	strIndexes = [(m.start(0), m.end(0)) for m in re.finditer("<td class=.*</td>", table)]
	for lineIndex in strIndexes:
		line = table[lineIndex[0]:lineIndex[1]]
		line = line.replace("&amp;","&")
		online = "online" in line
		line = line[line.index("<span>") + 6:line.index("</span>")]
		if online:
			line = line[line.index('>') + 1:line.index('</a>')]
			if (line not in statuses.keys()):
				print color.GREEN + line + color.BOLD + " now is online!" + color.END
				doMail(line)
			statuses[line]="online"	
		else:
			if (line not in statuses.keys()):
				print color.RED + line + color.BOLD + " is offline" + color.END
			statuses[line]="offline"	


def doMail(topic):
	message = """From: {}
To: {}
Subject: Apple Dev Center update
{} is now Online""".format(sender,receivers,topic)
	

	try:
	    session = smtplib.SMTP('smtp.gmail.com',587)
	    session.ehlo()
	    session.starttls()
	    session.ehlo()
	    session.login(sender,pw)
	    session.sendmail(sender,receivers,message)
	    session.quit()

	    print "Successfully sent email"
	except smtplib.SMTPException:
	    print "Error: unable to send email"

def runLoop():
	while 1:
		getStatuses()
		sleep(60)
runLoop()
