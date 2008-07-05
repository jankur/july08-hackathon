#!/usr/bin/env python

# Standard Python imports
import wsgiref.handlers
import os

# GAE imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):
  def get(self):
    template_values = {
        'board': ['A', 'D', 'Qu', 'G',
          'A', 'D', 'Qu', 'G',
          'A', 'D', 'Qu', 'G',
          'A', 'D', 'Qu', 'G',
          'A', 'D', 'Qu', 'G']
        }
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
