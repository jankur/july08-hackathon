#!/usr/bin/env python

import os
import cgi
import datetime
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

from datamodel import Transaction

class AddHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      return
    tpl_values = {
      'nickname': user.nickname(),
    }

    path = os.path.join(os.path.dirname(__file__), "templates", "add.tpl")
    self.response.out.write(template.render(path, tpl_values))

class SubmitHandler(webapp.RequestHandler):
  def post(self):
    date = datetime.datetime.now()
    t = Transaction(date=date, 
                    description='Test transaction')
    t.put()
    self.response.out.write('<html><body>You wrote:<pre>')
    self.response.out.write(cgi.escape(self.request.get('description')))
    self.response.out.write('</pre></body></html>')

def main():
  application = webapp.WSGIApplication([('/add', AddHandler),
                                        ('/submit', SubmitHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
