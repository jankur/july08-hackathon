#!/usr/bin/env python

# Standard Python imports
import wsgiref.handlers
import os
import random

# GAE imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

def getRandomBoard():
  dice = [ [ 'L', 'R', 'Y', 'T', 'T', 'E' ],
           [ 'V', 'T', 'H', 'R', 'W', 'E' ],
           [ 'E', 'G', 'H', 'W', 'N', 'E' ],
           [ 'S', 'E', 'O', 'T', 'I', 'S' ],
           [ 'A', 'N', 'A', 'E', 'E', 'G' ],
           [ 'I', 'D', 'S', 'Y', 'T', 'T' ],
           [ 'O', 'A', 'T', 'T', 'O', 'W' ],
           [ 'M', 'T', 'O', 'I', 'C', 'U' ],
           [ 'A', 'F', 'P', 'K', 'F', 'S' ],
           [ 'X', 'L', 'D', 'E', 'R', 'I' ],
           [ 'H', 'C', 'P', 'O', 'A', 'S' ],
           [ 'E', 'N', 'S', 'I', 'E', 'U' ],
           [ 'Y', 'L', 'D', 'E', 'V', 'R' ],
           [ 'Z', 'N', 'R', 'N', 'H', 'L' ],
           [ 'N', 'M', 'I', 'Qu', 'H', 'U' ],
           [ 'O', 'B', 'B', 'A', 'O', 'J' ]  ]
  dice_order = range(16)
  random.shuffle(dice_order)
  board = []
  for die in dice_order:
    board.append(dice[die][random.randint(0, 5)])
  return board

class MainHandler(webapp.RequestHandler):
  def get(self):
    template_values = {
        'board': getRandomBoard()
    }
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
