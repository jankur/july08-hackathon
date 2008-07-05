#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.api import users

class Transaction(db.Model):
  date = db.DateTimeProperty(required=True)
  description = db.StringProperty(required=True)
  # location = 
  owner = db.UserProperty()
  currency = db.StringProperty(default='USD')

class AmountProperty(db.FloatProperty):
  def empty(self, value):
    return value < 0.0

class TransactionUser(db.Model):
  transaction = db.ReferenceProperty(Transaction, required=True) 
  user = db.UserProperty()
  amount_paid = AmountProperty(default=-1)
  amount_owed = AmountProperty(default=-1)
  auto_computed = db.BooleanProperty(default=False)

