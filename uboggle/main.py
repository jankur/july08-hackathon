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
  board = db.StringListProperty(str)
  date = db.DateTimeProperty(auto_now_add=True)
  solution = db.StringListProperty(str)

class MainHandler(webapp.RequestHandler):
  def get(self):
    global mysolver
    # Make the db store object representing the game.
    game = Game()
    game.board = getRandomBoard()
    game.solution = mysolver.solve(game.board) 
    game.put()
    
    template_values = {
        'game_key': str(game.key()),
        'board': game.board
    }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

class GetScore(webapp.RequestHandler):
  def post(self):
    words = self.request.get_all("words")
    game_key = str(self.request.get("game_key"))

    logging.info(words)
    logging.info(game_key)

    game = Game.get(db.Key(game_key))
    logging.info(game.solution)

    results = []
    sol_set = set(game.solution)
    for word in words:
      word = word.lower()
      if word in sol_set:
        results.append((word, "correct", self.getWordScore(word)))
      else:
        results.append((word, "incorrect", 0))
    for word in game.solution:
      if word not in words:
        results.append((word, "notpresent", 0))
        
    logging.info(results)
    self.response.out.write(simplejson.dumps(results))

  def getWordScore(self, word):
    length = len(word)
    if word.find("qu") != -1:
      length -= 1

    if length >= 3 and length <= 4:
      return 1
    elif length == 5:
      return 2
    elif length == 6:
      return 3
    elif length == 7:
      return 5
    else:
      return 11
    
def main():
  application = webapp.WSGIApplication(
      [('/', MainHandler), 
        ("/getscore", GetScore)],
      debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
