#!/usr/bin/python

'''
HyPnOt - a small python blog CMS using flat files instead of a table-based DB.
Runs under Apache mod_wsgi (https://code.google.com/p/modwsgi/)
Edit config.py. You do not have to change anything here.

Complaints: @modalexii (<- is not a programmer and is amazed that this works at all)
'''

def getconfig(param):
	from os.path import dirname
	from sys import path
	p = dirname(__file__)
	path.append(p)
	import config
	val = eval('config.%s' % (param))
	return val

def createsession(username):
	weblinkroot = getconfig('weblinkroot')
	import string
	from random import sample
	r = '%s%s%s' % (string.ascii_uppercase, string.ascii_lowercase, string.digits)
	sessionid = ''.join(sample(r, 32))
	exp = ''
	writetosessionfile(sessionid, username = username)
	return ('Set-Cookie', 'sessionid=%s; Path=%s; Secure; HttpOnly' % (sessionid, weblinkroot))

def destroysession(sessionid):
	weblinkroot = getconfig('weblinkroot')
	writetosessionfile(sessionid)
	return ('Set-Cookie', 'sessionid=%s; Expires=Thu, 01 Jan 1970 00:00:01 GMT; Path=%s' % (sessionid, weblinkroot))

def writetosessionfile(sessionid, username = None):
	'''(over)write value to line of sessionfile'''
	datadir = getconfig('datadir')
	entry = '%s;;%s\n' % (username, sessionid)
	sessionfile = '%s/sessions' % (datadir)
	sessiondata = open(sessionfile, 'r').readlines(512)

	if username:
		# recording a new session
		sessiondata.append(entry)
	else:
		# destroying a newly ended session
		for l in sessiondata:
			if sessionid in l:
				sessiondata.remove(l)

	w = open(sessionfile, 'wb')
	w.writelines(sessiondata)
	w.close()

def newfile(data, editing = False):
	from datetime import datetime
	datadir = getconfig('datadir')
	weblinkroot = getconfig('weblinkroot')
	title = data.get('title', [''])[0]
	title = scrubstring(title)
	if not title:
		title = 'Untitled Post'
	subtitle = data.get('subtitle', [''])[0]
	subtitle = scrubstring(subtitle)
	body = data.get('body', [''])[0]
	body = scrubstring(body)
	if editing:
		date = data.get('preservedate', [''])[0]
		number = data.get('preservenumber', [''])[0]

		# remove the old file afer an edit that altered the name
		# this is hard to read - rewrite me!!!!
		deadmanwalking = '%s-%s' % (number, ''.join( w for w in data.get('oldtitle', [''])[0].split(' '))[:12]) 
		f = '%s/posts/%s.post' % (datadir, deadmanwalking)
		try:
			delfile(f)
		except OSError:
			# causes: permissions, bug, or ->post data was tampered with<-
			pass
	else:
		date = datetime.now().strftime("%d %b %Y")
		number = getnextpostnumber()

	name = '%s-%s' % (number, ''.join( w for w in title.split(' '))[:12])
		
	newpost = open('%s/posts/%s.post' % (datadir, name),'wb')
	newpost.write('%s;;%s;;%s;;\n%s' % (date, title, subtitle, body))
	newpost.close()

	return '%s/%s' % (weblinkroot, name)

def delfile(path):
	from os import remove
	remove(path)

def getnextpostnumber():
	from subprocess import Popen, PIPE
	e = '%s/posts' % (getconfig('datadir'))
	l = Popen(['ls', '-r', e, ], stdout = PIPE,)
	h = Popen(['head', '-n', '1'], stdin = l.stdout, stdout = PIPE,)
	s = h.communicate()[0]
	n = s[:4]
	n = int(n) + 1
	n = '%04d' % n
	n = str(n)
	return n

def scrubstring(string):
	from scrubber import Scrubber
	scrubber = Scrubber(autolink=True)
	try:
		string = string.decode('ascii')
	except UnicodeDecodeError:
		string = string.decode('utf-8')
	string = scrubber.scrub(string)
	return string.encode('utf-8')
