from google.appengine.ext import db
from google.appengine.api import users

class Transaction(db.Model):
  date = db.DateTimeProperty(required=True)
  description = db.StringProperty(required=True)
  # location = 
  owner = db.UserProperty()
  currency = db.StringProperty(default='USD')

class TransactionUserEntry(db.Model):
  transaction_id = db.ReferenceProperty(Transaction, required=True) 
  user_id = db.UserProperty()
  amount_paid = db.FloatProperty()
  amount_owed = db.FloatProperty()
  auto_computed = db.BooleanProperty(default=False)   

