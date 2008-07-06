#!/usr/bin/env python

import os
import cgi
import datetime
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

import datamodel as dm
import util

class AddHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      return
  
    date = datetime.datetime.now()
    desc = "Created by %s" % user.nickname() 
    transaction = dm.Transaction(date=date, description=desc)
    transaction.put()
    tu = dm.TransactionUser(transaction=transaction, user=user)
    tu.put()

    self.redirect("/edit?tid=%s" % transaction.key())

class EditHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      return

    tid = self.request.get('tid', '')
    if not tid:
      # TODO: Something nicer?
      self.redirect("/")
      return

    # TODO: Handle exception
    tstate = util.TransactionState(transaction=dm.Transaction.get(tid),
				   user=users.get_current_user())

    tpl_values = {
      'nickname': user.nickname(),
      'transaction': tstate.transaction(),
      'num_users': len(tstate.all_transaction_users()),
      'users': tstate.all_transaction_users()
    }

    path = os.path.join(os.path.dirname(__file__), "templates", "edit.tpl")
    self.response.out.write(template.render(path, tpl_values))

  def post(self):
    self.response.out.write("DONE")
    return
    date = datetime.datetime.now()
    t = Transaction(date=date, 
                    description='Test transaction')
    t.put()
    self.response.out.write('<html><body>You wrote:<pre>')
    self.response.out.write(cgi.escape(self.request.get('description')))
    self.response.out.write('</pre></body></html>')

def main():
  application = webapp.WSGIApplication([('/add', AddHandler),
                                        ('/edit', EditHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
