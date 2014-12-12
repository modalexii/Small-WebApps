'''
HyPnOt - a small python blog CMS using flat files instead of a table-based DB.
Runs under Apache mod_wsgi (https://code.google.com/p/modwsgi/)
Edit config.py. You do not have to change anything here.

Complaints: @modalexii (<- is not a programmer and is amazed that this works at all)
'''

if __name__ == '__main__':
	print 'This web application must be executed by mod_wsgi. See https://code.google.com/p/modwsgi/'
	quit()
elif __name__.startswith('_mod_wsgi_'):
	from os.path import dirname
	from sys import path
	p = dirname(__file__)
	path.append(p)
	from config import *

class BlogPost:
	'''extract meta & content given file'''
	def __init__(self, postfile):
		'''expects full file name + extension, no path'''
		self.filename = postfile
		self.name = self.filename [:-5] # cut extension
		self.fullpath = '%s/posts/%s' % (datadir, self.filename)
		try:
			self.number = '%04d' % (int(self.filename[:4]))
		except ValueError:
			# file in posts dir with non int()-able [:4] - in the future, this should not pass silently
			pass
		f = open(self.fullpath, 'r') # IOError here if can't read postfile
		i = f.readline().split(';;')
		f.close()
		self.date = i[0]
		self.title = i[1]
		self.subtitle = i[2]
	def getbody(self):          
		f = open(self.fullpath, 'r')
		b = f.readlines()[1:]
		f.close()
		self.body = ''.join( str(x) for x in b)
		return self.body

class GetHTML:
	def __init__(self):
		'''get or create basic html elements. methods must be added to full()'s list'''
		try:
			f = open(prependfile,'r')
		except TypeError:
			# prependfile = None
			self.prepend = '\
<html>\n\
	<head>\n\
		<title>My HyPn0t Blog</title>\n\
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n\
		<link type="text/css" rel="stylesheet" href="hypnot.css">\n\
	</head>\n\
	<body>\n'
		else:
			self.prepend = f.read()
			f.close()

		try:
			f = open(appendfile,'r')
		except TypeError:
			self.append = '\
	</body>\n\
</html>'
		else:
			self.append = f.read()
			f.close()

	def adminbar(self, activepost):
		try:
			name = activepost.name
		except AttributeError:
			# when activepost = None
			editanddelbuttons = ''
		else:
			editanddelbuttons = '\
			<form action="{weblinkroot}/{name}" method="get" autocomplete="off">\n\
				<input type="hidden" name="edit" value="1" />\n\
				<input type="submit" value="edit" class="edit">\n\
			</form>\
			<form action="{weblinkroot}/{name}" method="get" autocomplete="off">\n\
				<input type="hidden" name="delete" value="1" />\n\
				<input type="submit" value="delete" class="delete">\n\
			</form>'.format(weblinkroot = weblinkroot, name = name,)

		self.adminbar = '\
		<div id="adminbar">\n\
			<form action="{weblinkroot}/new" method="get" autocomplete="off">\n\
				<input type="submit" value="new post" class="new">\n\
			</form>\n\
			<form action="{weblinkroot}/{adminpagename}" method="get" autocomplete="off">\n\
				<input type="submit" value="all posts" class="all">\n\
			</form>\n\
			{editanddelbuttons}\
			<form action="{weblinkroot}/{adminpagename}" method="get" autocomplete="off">\n\
				<input type="hidden" name="logout" value="1" />\n\
				<input type="submit" value="logout" class="logout">\n\
			</form>\n\
		</div>\n'.format(weblinkroot = weblinkroot,
		 				 adminpagename = adminpagename,
						 editanddelbuttons = editanddelbuttons,)

	def body(self, activepost):
		'''build main page content from activepost object'''
		self.body = '\
		<div id="post">\n\
			<div class="postheader">\n\
				<h3 class="date">{date}</h3>\n\
				<h1 class="title">{title}</h1>\n\
				<h2 class="subtitle">{subtitle}</h2>\n\
			</div>\n\
			<div class="postbody">\n\
				{body}\n\
			</div>\n\
		</div>\n'.format(date = activepost.date,
						 title = activepost.title,
						 subtitle = activepost.subtitle,
						 body = activepost.getbody(),)

	def links(self, posts, activepost, context = 'bar', admin = False):
		'''build list of other post links with sortedposts list, excluding activepost'''
		'''context can be 'bar' or 'all', for styling only '''
		self.links = '\
		<div id="{context}">\n\
			<ul>\n\
				<li>\n\
					<span class="linkhome"><a href="{weblinkroot}">Home</a></span>\n\
				</li>'.format(context = context, weblinkroot = weblinkroot,)

		try:
			donotlist = activepost.filename
		except AttributeError:
			donotlist = None

		if admin:
			for i in posts[::-1]:
				i = BlogPost(i)
				self.links = '{links}\
			<li>\n\
				<form action="{linkhref}" method="get" autocomplete="off">\n\
					<input type="hidden" name="edit" value="1" />\n\
					<input type="submit" value="edit" class="edit">\n\
				</form>\n\
				<form action="{linkhref}" method="get" autocomplete="off">\n\
					<input type="hidden" name="delete" value="1" />\n\
					<input type="submit" value="delete" class="delete">\n\
				</form>\n\
				<a href="{linkhref}" class="post">\n\
					<span class="sbpostdate">{date}</span>\n\
					<span class="sbposttitle">{title}</span>\n\
					<span class="sbpostsubtitle">{subtitle}</span>\n\
				</a>\n\
			</li>\n'.format(links = self.links, 
							date = i.date,
							title = i.title,
							subtitle = i.subtitle,
							linkhref = '%s/%s' % (weblinkroot, i.name),)

		else:
			for i in posts[::-1]:
				if i != donotlist:
					i = BlogPost(i)
					self.links = '{links}\
				<li>\n\
					<a href="{linkhref}">\n\
						<span class="sbpostdate">{date}</span>\n\
						<span class="sbposttitle">{title}</span>\n\
						<span class="sbpostsubtitle">{subtitle}</span>\n\
					</a>\n\
				</li>\n'.format(links = self.links, 
								date = i.date,
								title = i.title,
								subtitle = i.subtitle,
								linkhref = '%s/%s' % (weblinkroot, i.name),)

			if donotlist:
				self.links = '{links}\
					<li>\n\
						<span class="linktoall"><a href="{weblinkroot}/all">List All Posts</a></span>\n\
					</li>'.format(links = self.links, weblinkroot = weblinkroot,)

		self.links = '%s\
			</ul>\n\
		</div>\n' % (self.links)

	def deleteconfirm(self, activepost):
		self.deleteconfirm = '\
		<div id="deleteconfirm">\n\
			<h1>Are you sure?</h1>\n\
			<h2>The following post will be deleted forever:</h2>\n\
			<div class="doomedpost">\n\
				<h2 class="deleteconfirmtitle">{title}</h2>\n\
				<h3 class="deleteconfirmsubtitle">{subtitle}</h3>\n\
			</div>\n\
			<form class="right" name="deletecancel" action="{weblinkroot}" method="get" autocomplete="off">\n\
				<input type="submit" value="Cancel" class="cancel">\n\
			</form>\n\
			<form class="right" name="deleteconfirm" action="{weblinkroot}/delete" method="post">\n\
				<input type="hidden" name="deadmanwalking" value="{name}">\n\
				<input type="submit" value="Yes, Delete" class="delete">\n\
			</form>\n\
		</div>\n'.format(title = activepost.title,
						 subtitle = activepost.subtitle,
						 name = activepost.name,
						 weblinkroot = weblinkroot,)

	def login(self):
		self.login = '\
		<div id="loginform">\n\
			<form name="loginform" action="{weblinkroot}/{adminpagename}" method="post" autocomplete="off">\n\
				<span class="authnotice">Authenticate to proceed:</span>\n\
				User: <input type="text" name="user">\n\
				Pass: <input type="password" name="pass">\n\
				<input type="submit" value="Log In">\n\
			</form>\n\
		</div>'.format(weblinkroot = weblinkroot, adminpagename = adminpagename,)

	def credsrejected(self):
		self.credsrejected = '\
		<div id="authfailnotice">\n\
			<h1 class="authfailheadline">Authentication Failure</h1>\n\
			<h2 class="authfaildetail">Incorrect username or password.</h2>\n\
		</div>\n'

	def postwriter(self, title = '', subtitle = '', body = '', date = '', number = ''):
		'''new post, or post "editor" with prepopulated fields passed'''
		if title: #if we're editing
			titleeditwarn = '<span class="editwarning">Careful: The post URL is derrived from the title. If you change the title, previously distributed links may break!</span>'
			postbuttonvalue = 'Update'
			preservefields = '\
			<input type="hidden" name="preservedate" value="{date}">\n\
			<input type="hidden" name="preservenumber" value="{number}">\n\
			<input type="hidden" name="oldtitle" value="{title}">\n\
			'.format(weblinkroot = weblinkroot, date = date, number = number, title = title,)
			# if preservefields data is tampered with, the old post link will break, but that's all
		else:
			titleeditwarn = ''
			postbuttonvalue = 'Publish'	
			preservefields = ''

		self.postwriter =  '\
		<div id="newpostform">\n\
			<form name="newpost" action="{weblinkroot}/new" method="post" autocomplete="off">\n\
				<div class="meta">\n\
					<div class="title">\n\
						<div class="heading">\n\
							<h2>Title: </h2>\n\
						</div>\n\
						<input type="text" name="title" value="{title}" />\n\
					</div>\n\
					{titleeditwarn}\n\
					<div class="subtitle">\n\
						<div class="heading">\n\
							<h2>Subtitle: </h2>\n\
						</div>\n\
						<input type="text" name="subtitle" value="{subtitle}" />\n\
					</div>\n\
				</div>\n\
				<div class="editor">\n\
					<div class="heading">\n\
						<h2>Post: </h2>\n\
					</div>\n\
					<div class="textarea">\n\
						<script src="/static/main/framework/ckeditor/ckeditor.js"></script>\n\
						<noscript>\n\
							<p>Javascript is dasabled in your browser - you will have to add all HTML formatting manually. \n\
							Enable javascript to use the editor.</p>\n\
						</noscript>\n\
						<textarea class="ckeditor" name="body">{body}</textarea>\n\
					</div>\n\
				</div>\n\
				{preservefields}\n\
				<input type="submit" value="{postbuttonvalue}" class="publish">\n\
			</form>\n\
			<form name="publishcancel" action="{weblinkroot}" method="get">\n\
				<input type="submit" value="Cancel" class="publishcancel">\n\
			</form>\n\
		</div>\n'.format(weblinkroot = weblinkroot,
						 title = title,
						 titleeditwarn = titleeditwarn,
						 subtitle = subtitle,
						 body = body,
						 preservefields = preservefields,
						 postbuttonvalue = postbuttonvalue,)

	def notfound(self):
		self.notfound = '\
		<div id="notfound">\n\
			<h2>Not Found!</h2>\n\
			<p>Sorry, that page doesn\'t exist. Try some of these instead:</p>\n\
		</div>\n'

	def redirect(self, link, nofollowtitle):
		self.redirect = '\n\
		<html>\n\
			<head>\n\
				<meta http-equiv="refresh" content="0;url={link}">\n\
			</head>\n\
			<body>\n\
				<h3>{nofollowtitle}</h3>\n\
				<p>If you are not redirected momentarily, click <a href="{link}">here</a> to proceed.</p>\n\
			</body>\n\
		</html>'.format(link = link, nofollowtitle = nofollowtitle,)
		self.prepend = None
		self.append = None

	def full(self):
		html = ''
		pieces = ['self.prepend', 'self.adminbar', 'self.body', 'self.postwriter', \
		'self.deleteconfirm', 'self.login', 'self.credsrejected', 'self.notfound', \
		'self.links', 'self.redirect', 'self.append']
		for p in pieces:
			pvar = eval(p)
			if type(pvar) == str:
				html = '%s%s' % (html, pvar)
		return html

def listfiles(maxlen, directory):
	'''return maxlen number of files in directory, sorted chronologically'''
	# dont read more than necessary (as glob or its components would)
	from subprocess import Popen, PIPE
	do_ls = Popen(['ls', '-r', directory, ], stdout = PIPE,)
	do_head = Popen(['head', '-n', maxlen], stdin = do_ls.stdout, stdout = PIPE,)
	r = do_head.communicate()[0]
	# split to list, remove last item (trailing newline)
	r = r.split('\n')[:-1]
	# reverse list for chronological order
	return r[::-1]

def authenticate(username, password):
	if username in credentials and credentials[username] == password:
		return True

def iscurrentsession(string):
	cookie = False
	sessiondata = open('%s/sessions' % (datadir), 'r').readlines(512)
	for i in sessiondata:
		try:
			if string in i.split(';;')[1].strip():
				cookie = True
				break
		except IndexError:
			# forgive stray newline breaking [1]
			pass
	return cookie

def application(environ, start_response):

	requestpath = environ.get('PATH_INFO', '').rstrip('/')

	page = GetHTML()

	headers = []
	headers.append(('Content-Type', 'text/html'))
	status = '200 OK'

	try:
		sessionid = environ['HTTP_COOKIE'].split('sessionid=')[0].strip()
	except KeyError:
		cookie = False
	except:
		cookie = False
		raise
	else:
		cookie = iscurrentsession(sessionid)

	if environ['REQUEST_METHOD'] == 'POST':
		'''handle POST requests'''
		from cgi import parse_qs
		try:
			request_body_size = int(environ.get('CONTENT_LENGTH', 0))
		except (ValueError):
			request_body_size = 0

		request_body = environ['wsgi.input'].read(request_body_size)
		data = parse_qs(request_body)

		if requestpath == '/%s' % (adminpagename):
			# POST to admin page - check credentials
			username = data.get('user', [''])[0]
			password = data.get('pass', [''])[0]
			if authenticate(username, password):
				from admin import createsession
				c = createsession(username)
				headers.append(c)
				m = 'Authentication successful!'
				page.redirect('%s/%s' % (weblinkroot, adminpagename), m)

			else:
				page.credsrejected()
		elif requestpath == '/new' and cookie:
			# POST to /new - write new post file
			from admin import newfile

			if data.get('preservenumber', [''])[0]:
				# treat as edit
				newlink = newfile(data, editing = True)
			else:
				# treat as brand new
				newlink = newfile(data)
			m = 'Post successful!'
			page.redirect(newlink, m)

		elif requestpath == '/delete' and cookie:
			# POST to /delete - proceed to remove post
			f = data.get('deadmanwalking', [''])[0]
			f = '%s/posts/%s.post' % (datadir, f)

			from admin import delfile
			try:
				delfile(f)
			except OSError:
				# permissions error or post data tampered - in the future, this shouldn't be silent
				pass
			m = 'Post deleted.'
			page.redirect(weblinkroot, m)

	else:
		'''handle GET requests'''
		if requestpath == '':
			# GET /
			# post meta & content
			l = listfiles('1', '%s/posts' % (datadir),)
			try:
				p = l[0]
			except IndexError:
				# no posts in posts dir
				p = '%s/placeholer-donotdelete.post' % (datadir)### HI FIX THIS PLEASE ###
			activepost = BlogPost(p) # most recent post by number
			page.body(activepost)

			# sidebar links
			n = int(linkslen) + 1 # we're removing one (activepost), so add one
			n = str(n)
			l = listfiles(n, '%s/posts' % (datadir))
			page.links(l, activepost)

		elif requestpath == '/all':
			# GET /all - list all (up to 9999) posts
			l = listfiles('9999', '%s/posts' % (datadir))
			page.links(l, context = 'all', activepost = None)

		elif requestpath == '/%s' % (adminpagename):
			if cookie:
				from cgi import parse_qs
				rawquerystring = environ['QUERY_STRING']
				querystring = parse_qs(rawquerystring)
				logout = querystring.get('logout', [''])[0]
				if logout == '1':
					from admin import destroysession
					setcookie = destroysession(sessionid)
					headers.append(setcookie)
					m = 'You have logged out.'
					page.redirect(weblinkroot, m)
				else:
					page.links(listfiles('9999', '%s/posts' % (datadir)), activepost = None, context = 'all', admin = True)
			else:
				page.login()
		elif requestpath == '/new' and cookie:
			page.postwriter()
		else:
			# arbitrary requestpaths
			from cgi import parse_qs
			rawquerystring = environ['QUERY_STRING']
			querystring = parse_qs(rawquerystring)
			edit = querystring.get('edit', [''])[0]
			delete = querystring.get('delete', [''])[0]

			try:
				posssiblepost = requestpath.strip('/')[:17]
				activepost = BlogPost('%s.post' % (posssiblepost))
			except IOError:
				status = '404 NOT FOUND'
				page.links(listfiles('9999', '%s/posts' % (datadir)), None, context = all)
				page.notfound()
			else:
				if edit == "1" and cookie:
					page.postwriter(activepost.title, activepost.subtitle, activepost.getbody(), activepost.date, activepost.number)
				elif delete == "1" and cookie:
					page.deleteconfirm(activepost)
				else:
					page.body(activepost)
					page.links(listfiles(str(int(linkslen) + 1), '%s/posts' % (datadir)), activepost)
				
 
	if cookie:
		try:
			page.adminbar(activepost)
		except UnboundLocalError:
			page.adminbar(None)

	html = page.full()
	headers.append(('Content-Length', str(len(html))))
	start_response(status, headers)

	return html$ 
