# where to keep data. no trailing slash.
# e.g., datadir = '/usr/local/www/hypnoter'
#
#this directory must:
#	be readable and traversable (+rx)
#	contain a writable, readable (+rw) file called "sessions"
#	contain a recursively writable, readable, and traversable (-R +rwx) directory called "posts"
datadir = '/usr/local/www/hypnoter'

# path from the web root to the blog "home". no trailing slash.
# e.g., weblinkroot = '/blog'
# or, weblinkroot = '/'
weblinkroot = '/blog'

# how to accesss the admin stuff (below "weblinkroot"). no slashes.
# e.g., adminpagename = 'admin'
# would put the admin page at http://foo.com/blog/admin
adminpagename = 'admin'

# dictionary of 'username' : 'password' pairs to access admin stuff
# e.g., credentials = { 'user1' : 'password1', 'user2' : 'Much!Better!Password!'}
credentials = { 'hypnoter' : 'changethis', }

# file to cat into html source BEFORE the body of the blog. full path, or None to use default.
# e.g., prependfile = '/usr/local/www/blogheader.txt'
# or, prependfile = None
prependfile = None

# same as "prependfile", but contents are inserted into html source AFTER blog body
appendfile = None

# the maximum number of recent posts to display in the "links" div
# e.g., linkslen = '10'
linkslen = '6'
