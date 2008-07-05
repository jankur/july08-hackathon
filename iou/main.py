#!/usr/bin/env python

import os
import datetime
import wsgiref.handlers

from google.appengine.ext import db
from datamodel import Transaction

from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):
  def get(self):
    date = datetime.datetime.now()
    t = Transaction(date=date, 
                    description='Test transaction')
    t.put()
    self.response.out.write('IOU!')

class ShowHandler(webapp.RequestHandler):
  def get(self):
    transactions = db.GqlQuery("SELECT * FROM Transaction ORDER BY date")

    for transaction in transactions:
      date_str = transaction.date.strftime("%Y-%m-%d %H:%M:%S")
      self.response.out.write('%s \n' % date_str)

def main():
  application = webapp.WSGIApplication([('/add', MainHandler),
                                        ('/', ShowHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
