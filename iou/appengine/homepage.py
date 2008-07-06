#!/usr/bin/env python

import os
import wsgiref.handlers
import datetime

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp

from google.appengine.ext.webapp import template

import datamodel as dm

class MainHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      return

    query = dm.TransactionUser.all()
    query.filter("user", user)
    transactions = []
    for tu in query:
      transactions.append(tu.transaction)

    tpl_values = {
      'username': user.nickname(),
      'transactions': transactions,
    }
    path = os.path.join(os.path.dirname(__file__), "templates", "homepage.tpl")
    self.response.out.write(template.render(path, tpl_values))

class JSONHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      return

    query = dm.TransactionUser.all()
    query.filter("user", user)
    transactions = []
    for tu in query:
      t = tu.transaction
      d = { 'date' : t.date.strftime("%d %M %Y"), 
            'description': t.description,
            'currency': t.currency
          }
      transactions.append(d)

    self.response.out.write(simplejson.dumps(transactions))
 
def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/json', JSONHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
