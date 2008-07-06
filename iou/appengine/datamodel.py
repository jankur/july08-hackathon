#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.api import users

class Transaction(db.Model):
  date = db.DateTimeProperty(required=True)
  description = db.StringProperty(required=True)
  # location = 
  # owner = db.UserProperty()
  currency = db.StringProperty(default='USD')

class AmountProperty(db.FloatProperty):
  def __init__(self, *args, **kw):
    kw['default'] = -1.0
    db.FloatProperty.__init__(self, *args, **kw)

  def empty(self, value):
    return value < 0.0

class TransactionUser(db.Model):
  transaction = db.ReferenceProperty(Transaction, required=True) 
  user = db.UserProperty()
  amount_paid = AmountProperty()
  amount_owed = AmountProperty()
  auto_computed = db.BooleanProperty(default=False)

