import webapp2

class MainPage(webapp2.RequestHandler):

    def sanitize(self, data):
        import cgi
        try:
            data = str(data)
            data = cgi.escape(data)
        except UnicodeError:
            data = cgi.escape(data).encode('ascii', 'xmlcharrefreplace')
        return data

    def assemblewebcode(self, requestedblocks, blockparams=None):
        '''requestedblocks array determines what bits get sandwiched between 
        the html head and tail, and in what order. blockparams array passes
        info to blocks that require it.'''
        # head
        content = "<html>\n"
        content += "    <head>\n"
        content += "        <title>\n"
        content += "            TwitteRecon\n"
        content += "        </title>\n"
        content += "        <meta name=\"description\" content=\"Look Up a Twitter User's Account Info, Sign Up (Creation) Date, Client, Time Zone, ID and more\">\n"
        content += "        <meta http-equiv=\"content-type\" content=\"text/html;charset=UTF-8\">\n"
        content += "        <link rel=\"stylesheet\" type=\"text/css\" media=\"screen\" href=\"style/twitterecon.css\"/>\n"
        content += "        <link rel=\"icon\" type=\"image/png\" href=\"http://icons.iconarchive.com/icons/wefunction/woofunction/32/user-business-search-icon.png\"/>\n"
        content += "    </head>\n"
        content += "    <body>\n"
        content += "        <div class=\"bodywrap\">\n"
        #content += "        <img src=\"style/graphics/twitter.png\" />"
        content += "        <a href=\"/\">\n"
        content += "            <img src=\"http://icons.iconarchive.com/icons/icontexto/social-inside/128/social-inside-twitter-icon.png\"/>\n"
        content += "        </a>\n"
        # /head
        for block in requestedblocks:
                if block == "htmlform":
                    content += "            <br />\n"
                    content += "            <h2>Enter a Twitter handle:</h2>\n"
                    content += "            <form name=\"twitterhandleinput\" action=\"/\" method=\"post\">\n"
                    content += "                <input type=\"text\" name=\"twitterhandle\" />\n"
                    content += "                <input type=\"submit\" value=\"Lookup\" />\n"
                    content += "            </form>\n"

                elif block == "userinfo":
                    import cgi, time
                    userinfo = blockparams[0]
                    content += "            <table>\n"           
                    content += "                <div id=\"identity\">\n"
                    content += "                    <tr>\n"
                    content += "                        <td class=\"bb\" colspan=\"4\">\n"
                    content += "                            <img src=\"%s\" class=\"profile\" />\n" % (self.sanitize(userinfo["profile_image_url_https"]))
                    content += "                            <br /><h3 class=\"profile\">@%s</h3>\n" % (self.sanitize(userinfo["screen_name"]))
                    content += "                        </td>\n"
                    content += "                    </tr>\n"
                    content += "                    <tr>\n"
                    content += "                        <td class=\"right\">Name:</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["name"]))
                    content += "                        <td class=\"right\">Numeric ID:</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["id"]))
                    content += "                    </tr>\n"
                    content += "                    <tr>\n"
                    # entities is a mess of nested lists and dictionaries
                    try:
                        e = userinfo["entities"]
                        e = e["url"]
                        e = e["urls"]
                        e = e[0]
                        expanded_url = e["expanded_url"]
                    except KeyError:
                        expanded_url = "None"
                    content += "                        <td class=\"right\">Website (orig):</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(expanded_url))
                    content += "                        <td class=\"right\">Website (t.co):</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["url"]))
                    content += "                    </tr>\n"
                    content += "                    <tr>\n"
                    content += "                        <td class=\"right\">Verified:</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["verified"]))
                    content += "                        <td class=\"right\">Multiple Contributors:</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["contributors_enabled"]))
                    content += "                    </tr>\n"
                    content += "                    <tr>\n"
                    content += "                        <td class=\"right\">Description:</td>\n"
                    content += "                        <td class=\"left\" colspan=\"3\">%s</td>\n" % (self.sanitize(userinfo["description"]))
                    content += "                    </tr>\n"
                    content += "                </div>\n"
                    content += "                <div id=\"locale\">\n"
                    content += "                    <tr>\n"
                    content += "                        <td class=\"bb\" colspan=\"4\"><h3>Locale</h3></td>\n"
                    content += "                    </tr>\n"
                    content += "                    <tr>\n"
                    content += "                        <td class=\"right\">Language:</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["lang"]))
                    content += "                        <td class=\"right\">Location:</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["location"]))
                    content += "                    </tr>\n"
                    content += "                    <tr>\n"
                    content += "                        <td class=\"right\">Time Zone:</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["time_zone"]))
                    content += "                        <td class=\"right\">Uses Geolocation:</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["geo_enabled"]))
                    content += "                    </tr>\n"
                    content += "                </div>\n"
                    content += "                <div id=\"use\">\n"
                    content += "                    <tr>\n"
                    content += "                        <td class=\"bb\" colspan=\"4\"><h3>Twitter Use</h3><td>\n"
                    content += "                    </tr>\n"
                    content += "                    <tr>\n"
                    d = self.sanitize(userinfo["created_at"])
                    d = d.split(' ')
                    created_at = d[0] + ' ' + d[1] + ' ' + d[2] + ' ' + d[-1] + ' ' + d[3] + ' GMT'
                    content += "                        <td class=\"right\">Account Created:</td>\n"
                    content += "                        <td class=\"left\" colspan=\"3\">%s</td>\n" % (self.sanitize(created_at))
                    content += "                    </tr>\n"
                    content += "                    <tr>\n"
                    content += "                        <td class=\"right\">Tweets:</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["statuses_count"]))
                    content += "                        <td class=\"right\">Favorited:</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["favourites_count"]))
                    content += "                    </tr>\n"
                    content += "                    <tr>\n"
                    content += "                        <td class=\"right\">Followers:</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["followers_count"]))
                    content += "                        <td class=\"right\">Following:</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["friends_count"]))
                    content += "                    </tr>\n"
                    content += "                    <tr>\n"
                    content += "                        <td class=\"right\">Protected:</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["protected"]))
                    content += "                        <td class=\"right\">Lists Added To:</td>\n"
                    content += "                        <td class=\"left\">%s</td>\n" % (self.sanitize(userinfo["listed_count"]))
                    content += "                    </tr>\n"
                    # return list of recent sources
                    sources = blockparams[1]
                    content += "                    <tr>\n"
                    content += "                        <td class=\"right\">Recent Sources:</td>\n"
                    content += "                        <td class=\"left\" colspan=\"3\">%s</td>\n" % (', ').join(self.sanitize(i) for i in set(sources))
                    content += "                    </tr>\n"
                    content += "                </div>\n"
                    content += "            </table>\n"
                    date = time.strftime("%a %d %b %Y %H:%M:%S %Z")
                    content += "            <br />\n"
                    content += "            <small>[ Report generated %s by twitterecon.appspot.com ]</small>\n" % (date)
                elif block == "invalidhandle":
                    content += "            <h2>Invalid handle</h2>\n"
                    content += "            Sorry, that's not a valid twitter handle. Go back and retry.\n"
                elif block == "twittererror":
                    # gets passed error object - need to parse it down
                    error = blockparams[0]
                    error = error.response_data
                    if "\"code\":34" in error:
                        # 404 - page not found
                        # return the same error as an invalid handle would return
                        requestedblocks.append("invalidhandle")
                    elif "\"code\":88" in error:
                        # 503 - api rate limit
                        content += "            <h2>Over Capacity</h2>\n"
                        content += "            Sorry, this site is getting too many requests . Please try later.\n"
                    else:
                        content += "            <h2>Twitter Error</h2>\n"
                        content += "            Sorry, this computer had trouble talking to the computers over at Twitter.<br/> Try again, or email admin@unsecu.re if the problem persists.\n"
                        #content += " %s" % error
                else:
                    content += ''' <h2>No Content Added [debug] </h2>\n '''
        # tail
        content += "        </div> <!-- bodywrap -->\n"
        content += "        <div class=\"stickyfooter\">\n"
        content += "            <a href=\"https://github.com/modalexii/webapps/tree/master/wsgi/twitterecon\" target=\"_blank\">\n"
        content += "                <img src=\"https://cdn1.iconfinder.com/data/icons/windows8_icons/26/github.png\"></a></br />\n"
        #content += "                <img src=\"style/graphics/github.png\"></a></br />"
        content += "            </a>\n"
        content += "            No affiliation with Twitter, inc.\n"
        content += "        </div> <!-- stickyfooter -->\n"
        content += "    </body>\n"
        content += "</html>\n"
        # /tail
        
        return content

    def respond(self, webcode):
            '''add headers as needed and pass webcode to web server'''
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write(webcode)

    def getrecentsources(self, api, user):
        ''' query timeline and return a list of twitter clients used'''
        sources = []
        statuses = api.statuses.user_timeline(screen_name = user)
        for tweet in statuses:
            source = tweet["source"]
            if source[:2] == "<a": # if a link is returned, parse it
                sources.append(source.split('>')[-2][:-3])
            else:
                sources.append(source)
        return set(sources)

    def get(self):
            '''process HTTP GET requests'''
            webcode = self.assemblewebcode(["htmlform"])
            self.respond(webcode)

    def post(self):
        '''process HTTP POST requests'''
        from twitter import Twitter, TwitterHTTPError, OAuth
        import cgi
        import re
        api = Twitter(
            auth = OAuth(
                '1429536751-SGu6nCXXJPMJCpYi3btT5piVRctz4yJGTCIWFlt',   # OA Tok
                'nn1Gmrw4XfSOhVsNFyFgI3XZKn7s6T8qqyTSY6fLs',            # OA Sec
                'NqRjZNope125gNFhSQ3Kdw',                               # CO Key
                'QcezAKz7lLkZRDZo6TzT6DVXJ7ca1Qxbwu8MXoF4M',            # CO Sec
                )
            )
        user = self.request.get('twitterhandle').strip()
        user = self.sanitize(user)
        if re.match(r'@?[A-Za-z0-9_]{1,16}$', user):
            # user gave syntactically valid twitter handle - proceed
            try:
                userinfo = api.users.show(screen_name=user, )
                recentsources = self.getrecentsources(api, user)
                blockparams = [userinfo, recentsources]
                webcode = self.assemblewebcode(["userinfo"], blockparams)
            except TwitterHTTPError as e:
                webcode = self.assemblewebcode(["twittererror"], [e])
        else:
            # user gave syntactically invalid twitter handle - die with info
            webcode = self.assemblewebcode(["invalidhandle"])
        self.respond(webcode)

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
