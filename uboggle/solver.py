import trie as trie_module

class Solver:
    def __init__(self, trie):
        self.trie = trie
        self.neighbors = [ [1, 4, 5],
                           [0, 2, 4, 5, 6],
                           [1, 3, 5, 6, 7],
                           [2, 6, 7],
                           [0, 1, 5, 8, 9],
                           [0, 1, 2, 4, 6, 8, 9, 10],
                           [1, 2, 3, 5, 7, 9, 10, 11],
                           [2, 3, 6, 10, 11],
                           [4, 5, 9, 12, 13],
                           [4, 5, 6, 8, 10, 12, 13, 14],
                           [5, 6, 7, 9, 11, 13, 14, 15],
                           [6, 7, 10, 14, 15],
                           [8, 9, 13],
                           [8, 9, 10, 12, 14],
                           [9, 10, 11, 13, 15],
                           [10, 11, 14] ]

    def solve(self, board):
        words = set([])
        for i in range(16):
            self._findWords(board, i, set([]), board[i], words)
        
        return list(words)

    def _findWords(self, board, cur_pos, past_positions, prefix, words):
        (valid, terminal) = self.trie.lookup(prefix)
        if not valid:
            return
        if terminal:
            words.add(prefix)
        past_positions.add(cur_pos)                
        for n in self.neighbors[cur_pos]:
            if n not in past_positions:
                self._findWords(board, n,
                                past_positions,
                                prefix + board[n],
                                words)
        past_positions.remove(cur_pos)
        
        return

