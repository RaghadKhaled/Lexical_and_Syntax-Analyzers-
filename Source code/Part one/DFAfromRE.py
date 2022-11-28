#ply.lex is an implementation of lex parsing tools for Python.
import ply.lex as lex
# networkx package for the Python used to create, manipulate graph networks used to draw tree
import networkx as nx
import matplotlib.pyplot as plt
# import to draw graph of DFA
from AutomataTheory import *

# Tokens
tokens = (
    'OPEN_P',
    'CLOSED_P',
    'OR',
    'STAR',
    'CONCAT',
    'LETTER',
    'LAMBDA'
)

# Rules that define the tokens
t_OPEN_P = r'\('
t_CLOSED_P = r'\)'
t_OR = r'\+'
t_STAR = r'\*'
t_CONCAT = r'\.'
t_LETTER = r'[a-zA-Z]'
t_LAMBDA = r'\#'


# Error rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

class RegexLexer:
    # A lexer to tokenize the content
    lexer = lex.lex()
    # A container containing the tokens
    parts = []

    # constructer
    def __init__(self, inp):
            self.content = '(' + inp + ')#'
            self.tokenize()


   # method of add tokens into list
    def tokenize(self):
        self.lexer.input(self.content)
        while True:
            token = self.lexer.token()
            if not token: # No more input
                break
            self.parts.append(token)

    # for printing tokens 
    def printTokens(self):
        for part in self.parts:
            print(part)

    # method add concantion (dot) step 2 in coversion 
    def _addConcats(self):
        possibleConcat = False
        concatMessage = ''
        index = 0

        for part in self.parts:
            if part.type in ['LETTER', 'LAMBDA']: # operand or #
                if possibleConcat is True:
                    concatMessage = concatMessage + '.' # add dot 
                else:
                    possibleConcat = True
            elif part.type in ['STAR', 'CLOSED_P']:# * or )
                possibleConcat = True
            elif (part.type == 'OPEN_P') & (self.parts[index - 1].type in ['LETTER', 'STAR']):
                concatMessage = concatMessage + '.'
            else:
                possibleConcat = False
            concatMessage = concatMessage + part.value
            index = index + 1

        self.content = concatMessage # after add dot
        self.parts.clear()
        self.tokenize()

    # to write in postfix notation by use reverse polish notation
    #where every operator follows all of its operands
    def writeAsRPN(self, permanent=False):
        if self.content[len(self.content) - 1] == '.':
            print("Already in rpn notation")
            return
        # First we need to have the regex written in reverse polish notation ot postfix
        operator_stack = [] # init list
        last_index = -1 # pointer of stack
        rpn_regex = ''
        for part in self.parts:
            if part.type in ['LETTER', 'STAR', 'LAMBDA']: 
                rpn_regex = rpn_regex + part.value # add to RE
                continue
            if part.type == 'OPEN_P':
                operator_stack.append(part) # put in stack
                last_index += 1 
                continue
            if part.type == 'CLOSED_P':
                while operator_stack[last_index].type != 'OPEN_P': # to pop until (
                    rpn_regex += operator_stack[last_index].value # add to RE
                    operator_stack.pop() # pop from stack
                    last_index -= 1
                # Doing one more pop to  extract the open parenthesis
                operator_stack.pop()
                last_index -= 1
                continue
            if part.type in ['OR', 'CONCAT']:
                if last_index >= 0:
                    if operator_stack[last_index].type not in ['OPEN_P', 'CLOSED_P']:
                        rpn_regex += operator_stack[last_index].value # add to RE
                        operator_stack.pop()  # pop from stack
                        operator_stack.append(part) # then add to stack
                    else:
                        operator_stack.append(part)  # add to stack
                        last_index += 1
                else:
                    operator_stack.append(part) # add to stack
                    last_index += 1
                continue

        # Clearing the stack of any operators that might have remained
        while len(operator_stack) != 0:
            rpn_regex += operator_stack[last_index].value
            operator_stack.pop() # pop from stack

        if permanent is True:
            self.parts.clear()
            self.content = rpn_regex # after postfix update content
            self.tokenize()

        return rpn_regex

    # method to creating syntax tree 
    def makeAST(self):
        self._addConcats()
        print("\nRegex after adding concatenations: " + self.content + '\n')
        self.printTokens()

        print("\nRegex written in reverse polish notation: " + self.writeAsRPN(permanent=True) + '\n')
        
        AST = nx.DiGraph() # init tree 
        node_stack = []
        last_index = -1

        for part in self.parts:
            if part.type in ['LETTER', 'LAMBDA']: # add operand or #
                AST.add_node(part, val=part.value) # add node
                node_stack.append(part) # add to stak
                last_index += 1
            elif part.type in ['OR', 'CONCAT']: # add + or .
                AST.add_node(part, val=part.value)
                for i in range(0, 2): # two operand
                    AST.add_edge(part, node_stack[last_index]) # add edage
                    node_stack.pop() # pop operand from stack
                    last_index -= 1
                node_stack.append(part) # add inner node
                last_index += 1
            elif part.type == 'STAR':
                AST.add_node(part, val=part.value) # add node
                AST.add_edge(part, node_stack[last_index]) # add edage
                node_stack.pop() # pop from stake
                node_stack.append(part)  # add inner node

        return AST
    # method to print syntax tree 
    def printAST(self):
        AST = self.makeAST()
        nx.nx_agraph.write_dot(AST, 'test.dot')
        pos = nx.nx_agraph.graphviz_layout(AST, prog='dot')
        nx.draw(AST, pos, node_color='cyan')
        nx.draw_networkx_labels(AST, pos, nx.get_node_attributes(AST, 'val'))

        plt.savefig('ast.png')
        plt.show()



# class convert RE to DFA 
class Converter:
    FirstPos = [] 
    LastPos = []
    FollowPos = []

    DFA = nx.MultiDiGraph()

    #constructor 
    def __init__(self, rpn_tokens: list):

        self.rpn_tokens = rpn_tokens 
        self._makeFirstPos()
        self._makeLastPos()
        self._makeFollowPos()

    def _makeFirstPos(self):
        """
        This method is used to compute the first_pos list for each token.

        There are special cases that we need to address: when a branch could generate both a sequence from a word
        or nothing at all. In this case the "sub-word" that is generated by the sub-tree could start on both branches.
        Since here we are building only the first-pos collection we are interested in left side sub-trees only.

        :return: nothing
        """
        index = 0  # Used to copy positions from previous nodes
        letter_no = 1  # Each letter in the regex is associated a number in the order of appearance
        nullable = []

        for token in self.rpn_tokens:
            if token.type in ['LETTER', 'LAMBDA']: #if it is operand or #
                newpos = [letter_no]
                letter_no += 1
                index += 1
                self.FirstPos.append(newpos)
                if token.type == 'LAMBDA':
                    if token.lexpos == len(self.rpn_tokens) - 2:
                        nullable.append(False)
                    else:
                        nullable.append(True)
                else:
                    nullable.append(False)

            elif token.type == 'OR':
                newpos = self.FirstPos[index - 2].copy() + self.FirstPos[index - 1].copy() # c1 U c2
                self.FirstPos.append(newpos)
                index += 1
                if nullable[index - 3] | nullable[index - 2]:
                    nullable.append(True)
                else:
                    nullable.append(False)

            elif token.type == 'STAR':
                newpos = self.FirstPos[index - 1].copy()
                self.FirstPos.append(newpos)
                nullable.append(True)
                index += 1

            elif token.type == 'CONCAT':

                if self.rpn_tokens[index - 1].type == 'STAR':
                    nb = index - 2
                    while True:
                        if self.rpn_tokens[nb].type in ['CONCAT', 'OR']:
                            nb -= 2
                        else:
                            nb -= 1
                            break
                    newpos = self.FirstPos[nb].copy()
                    self.FirstPos.append(newpos)
                    index += 1

                    if nullable[nb]:
                        newpos = self.FirstPos[index - 2].copy()
                        self.FirstPos[index - 1] += newpos
                    if nullable[nb] & nullable[index - 2]:
                        nullable.append(True)
                    else:
                        nullable.append(False)
                else:
                    newpos = self.FirstPos[index - 2].copy()
                    self.FirstPos.append(newpos)
                    index += 1

                    if nullable[index - 3]:
                        newpos = self.FirstPos[index - 2].copy()
                        self.FirstPos[index - 1] += newpos
                    if nullable[index - 3] & nullable[index - 2]:
                        nullable.append(True)
                    else:
                        nullable.append(False)

    def _makeLastPos(self):
        index = 0  # Used to copy positions from previous nodes
        letter_no = 1  # Each letter in the regex is associated a number in the order of appearance
        nullable = []

        for token in self.rpn_tokens:
            if token.type in ['LETTER', 'LAMBDA']: #if ot is operand or #
                newpos = [letter_no]
                letter_no += 1
                index += 1
                self.LastPos.append(newpos)
                if token.type == 'LAMBDA': # if it is #
                    if token.lexpos == len(self.rpn_tokens) - 2:
                        nullable.append(False)
                    else:
                        nullable.append(True)
                else:
                    nullable.append(False)

            elif token.type == 'OR':
                newpos = self.LastPos[index - 2].copy() + self.LastPos[index - 1].copy()
                self.LastPos.append(newpos)
                index += 1
                if nullable[index - 3] | nullable[index - 2]:
                    nullable.append(True)
                else:
                    nullable.append(False)

            elif token.type == 'STAR':
                newpos = self.LastPos[index - 1].copy()
                self.LastPos.append(newpos)
                nullable.append(True)
                index += 1

            elif token.type == 'CONCAT':
                newpos = self.LastPos[index - 1].copy()
                self.LastPos.append(newpos)
                index += 1

                if self.rpn_tokens[index - 2].type == 'STAR':
                    nb = index - 3
                    while True:
                        if self.rpn_tokens[nb].type in ['CONCAT', 'OR']:
                            nb -= 2
                        else:
                            nb -= 1
                            break

                    if nullable[index - 2]:
                        newpos = self.LastPos[nb].copy()
                        self.LastPos[index - 1] += newpos

                    if nullable[nb] & nullable[index - 2]:
                        nullable.append(True)
                    else:
                        nullable.append(False)
                else:
                    if nullable[index - 2]:
                        newpos = self.LastPos[index - 3].copy()
                        self.LastPos[index - 1] += newpos
                    if nullable[index - 3] & nullable[index - 2]:
                        nullable.append(True)
                    else:
                        nullable.append(False)

    def _makeFollowPos(self):
        index = 0
        number_nop = 0

        # Counting the number of operand and #
        for token in self.rpn_tokens:
            if token.type in ['LETTER','LAMBDA']:
                number_nop += 1

        self.FollowPos = [[] for _ in range(number_nop)]

        for token in self.rpn_tokens:
            if token.type == 'STAR':
                for pos in self.LastPos[index]: 
                    newpos = self.FirstPos[index].copy() 
                    self.FollowPos[pos - 1] += newpos
                index += 1
            elif token.type == 'CONCAT':
                if self.rpn_tokens[index - 1].type == 'STAR':
                    nb = index - 2
                    while True:
                        if self.rpn_tokens[nb].type in ['CONCAT', 'OR']:
                            nb -= 2
                        else:
                            nb -= 1
                            break
                    for pos in self.LastPos[nb]:
                        self.FollowPos[pos - 1] += self.FirstPos[index - 1].copy()
                else:
                    for pos in self.LastPos[index - 2]:
                        self.FollowPos[pos - 1] += self.FirstPos[index - 1].copy()
                index += 1
            else:
                index += 1

        # Stripping duplicate values
        for collection in self.FollowPos:
            if collection is not None:
                collection = set(collection)
                
    
    # method to get the content of Firstpos,Lastpos, for GUI
    def getPrintText(self):
        text = "DFA functions :\n " # print DFA function
        fres = {}
        for part in self.rpn_tokens:
          for pos in self.FirstPos:
           fres[part.value] = pos
           self.FirstPos.remove(pos)
           break
        text += "Firstpos :" + str(fres) + "\n"
        lres = {}
        for part in self.rpn_tokens:
          for pos in self.LastPos:
           lres[part.value] = pos
           self.LastPos.remove(pos)
           break
        text += "Lastpos :" + str(lres) + "\n"
        ores = {}
        for part in self.rpn_tokens:
         if part.type in ['LETTER','LAMBDA']:
            for pos in self.FollowPos:
                 ores[part.value] = pos
                 self.FollowPos.remove(pos)
                 break
        text += "Followpos :" + str(ores) + "\n"       
        linecount = 4     
        return [text, linecount]
