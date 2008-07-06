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
    # TODO: Move parent setting to datamodel.py?
    tu = dm.TransactionUser(transaction=transaction,
			    parent=transaction,
                            user=user)
    tu.put()

    self.redirect("/edit?tid=%s" % transaction.key())

class EditHandler(webapp.RequestHandler):
  def get(self):
    if not self._SetState(): return
    self._WriteResponse()

  def post(self):
    if not self._SetState(): return
    errors = self.errors

    tstate = self.tstate
    tmp = self.request.get('description')
    if not tmp:
      errors.append("Description must be set")
    else:
      tstate.transaction().description = tmp

    # TODO: Edit date
    # TODO: Ensure that (person, paid, owed) all three arrays are in the same
    # order
    persons = self.request.get_all('person')
    paids = self.request.get_all('paid')
    oweds = self.request.get_all('owed')

    # TODO:
    if len(persons) != len(paids) or len(paids) != len(oweds):
      errors.append("Inconsistent number of parameters?")
    else:
      self._FillInPersons(persons, paids, oweds)

    if len(self.errors) == 0 and len(self.user_errors) == 0:
      tstate.Save()
    else:
      errors.append("DID NOT SAVE")
    
    self._WriteResponse()

  def _FillInPersons(self, persons, paids, oweds):
    for i in range(len(persons)):
      # TODO: Have a list of friends table?
      if not persons[i]:
	self.user_errors[persons[i]] = "Invalid email address"
      else:
	u = users.User(email=persons[i])
	tu = self.tstate.transaction_user(u)
	if not tu:
	  tu = self.tstate.AddTransactionUser(u)
	if paids[i] < 0:
	  self.user_errors[persons[i]] = "Invalid amount"
	else:
	  try:
	    tu.amount_paid = float(paids[i])
	  except ValueError:
	    self.user_errors[persons[i]] = "Bad amount paid"
	try:
	  tu.amount_owed = float(oweds[i])
	except ValueError:
	  self.user_errors[persons[i]] = "Bad amount owed"

  def _WriteResponse(self):
    user = self.user
    tstate = self.tstate
    tpl_values = {
      'nickname': user.nickname(),
      'transaction': tstate.transaction(),
      'users': tstate.all_transaction_users(),
      'errors': self.errors,
      'user_errors': self.user_errors.values()
    }
    path = os.path.join(os.path.dirname(__file__), "templates", "edit.tpl")
    self.response.out.write(template.render(path, tpl_values))

  def _SetUser(self):
    self.user = users.get_current_user()
    if not self.user:
      self.redirect(users.create_login_url(self.request.uri))
      return False
    return True

  def _SetTransactionState(self):
    tid = self.request.get('tid', '')
    if not tid:
      # TODO: Something nicer?
      self.redirect("/")
      return False

    # TODO: Handle exception
    tstate = util.TransactionState(transaction=dm.Transaction.get(tid),
				   user=users.get_current_user())
    self.tstate = tstate
    return True

  def _SetState(self):
    if not self._SetUser(): return False
    if not self._SetTransactionState(): return False
    self.errors = []
    self.user_errors = {}
    return True

def main():
  application = webapp.WSGIApplication([('/add', AddHandler),
                                        ('/edit', EditHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
