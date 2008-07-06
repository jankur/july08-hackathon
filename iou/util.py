#!/usr/bin/env python

import logging

from google.appengine.ext import db

import datamodel as dm

class UnauthorizedUserException(Exception):
  def __init__(self):
    pass

class TransactionState:
  def NewTransaction(transaction, user):
    transaction.put()
    tu = dm.TransactionUser(transaction=transaction,
			    user=user,
			    parent=transaction)
    tu.put()

  def __init__(self, transaction, user):
    if not transaction.is_saved():
      transaction.put()
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

  def all_transaction_users(self):
    return self._tu_map.values()

  def AddTransactionUser(self, u):
    # TODO: If user already exists?
    tu = dm.TransactionUser(transaction=self._transaction,
                            user=u,
			    parent=self._transaction)
    self._tu_map[u] = tu
    return tu

  def SettleTransaction(self):
    (total_spent, fixed_owed, num_fixed_owed)  = self._InternalSums()
    num_to_divide = len(self._tu_map) - num_fixed_owed
    if num_to_divide < 0:
      raise Exception("Please debug me")
    if num_to_divide == 0:
      return
    equal_division = (total_spent - fixed_owed) / num_to_divide
    for tu in self._tu_map.values():
      if not tu.auto_computed:
	tu.amount_owed = equal_division

  def TotalSpent(self):
    return self._InternalSums()[0]

  def Save(self):
    try:
      db.run_in_transaction(self._SaveTransactionUsers)
      self._transaction.put()
    except Exception, e:
      raise e

  def _SaveTransactionUsers(self):
    for tu in self._tu_map.values():
      tu.put()

  def _InternalSums(self):
    total_spent = 0
    fixed_owed = 0
    num_fixed_owed = 0
    for tu in self._tu_map.values():
      # TODO: Asim does not like this < 0
      if not tu.amount_paid < 0:
	total_spent += tu.amount_paid
      if tu.auto_computed:
	if tu.amount_owed.empty():
	  # TODO: Exception?
	  tu.auto_computed = False
	else:
	  fixed_owed += tu.amount_owed
	  num_fixed_owed += 1
    return (total_spent, fixed_owed, num_fixed_owed)
