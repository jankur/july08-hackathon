class TrieNode:
    def __init__(self, char):
        self.char = char
        self.children = {}
        self.is_terminal = False

    def getChar(self):
        return self.char

    def isTerminal(self):
        return self.is_terminal

    def setTerminal(self):
        self.is_terminal = True

    def getChildren(self):
        return self.children

    def addChild(self, char):
        if self.children.has_key(char):
            return self.children[char]
        else:
            newNode = TrieNode(char)
            self.children[char] = newNode
            return newNode

    def findChild(self, char):
        if self.children.has_key(char):
            return self.children[char]
        else:
            return None


class Trie:
    def __init__(self, words):
        self.root = TrieNode('') # Create the empty root node 
        for word in words:
            self.addWord(word)

    def addWord(self, word):
        currNode = self.root
        for c in word:
            currNode = currNode.addChild(c)
        currNode.setTerminal()

    def lookup(self, word):
        currNode = self.root
        for c in word:
            currNode = currNode.findChild(c)
            if currNode == None:
                return (False, False)

        return (True, currNode.isTerminal())

