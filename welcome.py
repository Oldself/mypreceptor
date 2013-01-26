# -*- coding: utf-8 -*-
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MyHandler(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            self.redirect('/app/index.html')
        else:
            self.redirect('/fr/hello.html')

application = webapp.WSGIApplication([('/.*', MyHandler)], debug=True)

if __name__ == "__main__":
    run_wsgi_app(application)