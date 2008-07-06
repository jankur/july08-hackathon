#!/usr/bin/env python

import os
import wsgiref.handlers
import datetime

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp

from google.appengine.ext.webapp import template

from datamodel import Transaction

class MainHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      return

    transactions = Transaction.all().order('-date')
    tpl_values = {
      'username': user.nickname(),
      'transactions': transactions,
    }
    path = os.path.join(os.path.dirname(__file__), "templates", "homepage.tpl")
    self.response.out.write(template.render(path, tpl_values))

 
def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()