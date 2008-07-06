#!/usr/bin/env python

from google.appengine.ext import db

import datamodel as dm

class UnauthorizedUserException(Exception):
  def __init__(self):
    pass

class TransactionState:
  def __init__(self, transaction, user):
    self._transaction = transaction
    self._tu_map = {}
    query = dm.TransactionUser.all()
    query.filter("transaction", transaction)
    authorized = False
    for tu in query:
      self._tu_map[tu.user] = tu
      if tu.user == user:
	authorized = True
    if not authorized:
      self._transaction = None
      self._tu_map = None
      raise UnauthorizedUserException()

  def transaction(self):
    return self._transaction

  def transaction_user(self, user):
    return self._tu_map.get(user)

  def AddTransactionUser(self, tu):
    # TODO: If user already exists?
    self._tu_map[tu.user] = tu

  def SettleTransaction(self):
    (total_spent, fixed_owed, num_fixed_owed)  = _InternalSums()
    num_to_divide = len(self._tu_map) - num_fixed_owed
    if num_to_divide < 0:
      raise Exception("Please debug me")
    if num_to_divide == 0:
      return
    equal_division = (total_spent - fixed_owed) / num_to_divide
    for tu in self._tu_map.values():
      if tu.auto_computed:
	tu.amount_owed = equal_division

  def TotalSpent(self):
    return _InternalSums()[0]

  def Save(self):
    try:
      db.run_in_transaction(self._SaveTransactionUsers)
      self_.transaction.put()
    except Exception, e:
      raise e

  def _SaveTransactionUsers(self):
    for tu in self._tu_map.values():
      tu.put()

  def _InternalSums():
    total_spent = 0
    fixed_owed = 0
    num_fixed_owed = 0
    for tu in self._tu_map.values():
      if not tu.amount_paid.empty():
	total_spent += tu.amount_paid
      if tu.auto_computed:
	if tu.amount_owed.empty():
	  # TODO: Exception?
	  tu.auto_computed = False
	else:
	  fixed_owed += tu.amount_owed
	  num_fixed_owed += 1
    return (total_spent, fixed_owed, num_fixed_owed)
