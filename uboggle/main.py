#!/usr/bin/env python

# Standard Python imports
import logging
import os
import random
import wsgiref.handlers
import solver

# GAE imports
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# django imports
from django.utils import simplejson

mysolver = solver.getSolver()

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

class Game(db.Model):
  board = db.ListProperty(str)
  date = db.DateTimeProperty(auto_now_add=True)
  solution = db.ListProperty(str)

class MainHandler(webapp.RequestHandler):
  def get(self):
    global mysolver
    # Make the db store object representing the game.
    game = Game()
    game.board = getRandomBoard()
    game.solution = mysolver.solve(game.board) 
    game.put()

    logging.info(game.solution)
    
    template_values = {
        'game_key': str(game.key()),
        'board': game.board
    }
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

class GetScore(webapp.RequestHandler):
  def post(self):
    #key = self.request.get_all("key")
    words = self.request.get_all("words")
    game_key = self.request.get("game_key")
    logging.info(words)
    logging.info(game_key)
    game = db.get(game_key)
    template_values = {
        'solution': game.solution,
        'words': words,
        }
    
    logging.info(template_values)
    self.response.out.write(simplejson.dumps(template_values))

def main():
  application = webapp.WSGIApplication(
      [('/', MainHandler), 
        ("/getscore", GetScore)],
      debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
