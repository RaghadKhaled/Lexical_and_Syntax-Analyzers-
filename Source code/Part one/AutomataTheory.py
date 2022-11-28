from os import popen
import time

class Automata:
    """class to represent an Automata"""
    #constructer for init 
    def __init__(self, language = set(['0', '1'])):
        self.states = set() #init state by set 
        self.startstate = None 
        self.finalstates = []
        self.transitions = dict() 
        self.language = language #insert language
    
    #method for return epsilon
    @staticmethod
    def epsilon():
        return ":e:"

    # method to establish start state
    def setstartstate(self, state):
        self.startstate = state
        # add to state set
        self.states.add(state)
    

    # method to insert final states
    def addfinalstates(self, state):
        #returns True if the specified state is of the specified type, otherwise False 
        if isinstance(state, int):
            # add state to array state 
            state = [state]
        # to add every final state in array to self.finalstates
        for s in state:
            if s not in self.finalstates:
                # add final to array
                self.finalstates.append(s)
    # method to add transion of automata
    def addtransition(self, fromstate, tostate, inp):
        #returns True if the specified inp is of the specified type, otherwise False
        if isinstance(inp, str):
            # convert into set
            inp = set([inp])
        # add from state into self.states
        self.states.add(fromstate)
        # add to state into self.states
        self.states.add(tostate)
        # check if from state in transion dict
        if fromstate in self.transitions:
            #check if to state exist in transion dist (ex: a in transion[b])
            if tostate in self.transitions[fromstate]:
                #add new transion into dict with previous transion 
                self.transitions[fromstate][tostate] = self.transitions[fromstate][tostate].union(inp)
            else:
                #add new transion into dict
                self.transitions[fromstate][tostate] = inp
        else:
            # if from state not in dict 
            self.transitions[fromstate] = {tostate : inp}
     # method for adding transion to dict 
    def addtransition_dict(self, transitions):
        # for every (transitions[fromstate][tostate]) add inp
        for fromstate, tostates in transitions.items():
            for state in tostates:
                self.addtransition(fromstate, state, tostates[state])
    # method to get transion of inp
    def gettransitions(self, state, key):
        #returns True if the specified state is of the specified type, otherwise False
        if isinstance(state, int):
            state = [state]
        trstates = set() #init set
        for st in state: # to search of transion 
            if st in self.transitions:
                for tns in self.transitions[st]:
                    if key in self.transitions[st][tns]:
                        trstates.add(tns)
        return trstates  #return transion 
    # method for get transion has epsilon lable 
    def getEClose(self, findstate):
        allstates = set() # init set 
        states = set([findstate]) 
        while len(states)!= 0:
            state = states.pop()
            allstates.add(state)
            if state in self.transitions:
                for tns in self.transitions[state]:
                    if Automata.epsilon() in self.transitions[state][tns] and tns not in allstates:
                        states.add(tns)
        return allstates
    # for printing the finite automata content 
    def display(self): 
        print ("states:", self.states) # print states
        print ("start state: ", self.startstate) # print start state
        print ("final states:", self.finalstates) # print final states or accept
        print ("transitions:") # print tramsions or move 
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    print ("  ",fromstate, "->", state, "on '"+char+"'",)
            print
    # to get the finite automata content in text manner for GUI
    def getPrintText(self):
        text = "language: {" + ", ".join(self.language) + "}\n" #  language
        text += "states: {" + ", ".join(map(str,self.states)) + "}\n" # states
        text += "start state: " + str(self.startstate) + "\n" # start state
        text += "final states: {" + ", ".join(map(str,self.finalstates)) + "}\n" # final states or accept
        text += "transitions:\n" # tramsions or move 
        linecount = 5
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                for char in tostates[state]:
                    text += "    " + str(fromstate) + " -> " + str(state) + " on '" + char + "'\n"
                    linecount +=1
        return [text, linecount]
    # method for construction
    def newBuildFromNumber(self, startnum):
        translations = {} # init dict
        for i in list(self.states): # for evry state
            translations[i] = startnum # add state with number 
            startnum += 1
        rebuild = Automata(self.language) # creat another automata 
        rebuild.setstartstate(translations[self.startstate]) # set start state
        rebuild.addfinalstates(translations[self.finalstates[0]]) # set final states 
        for fromstate, tostates in self.transitions.items(): # add tranisions
            for state in tostates:
                rebuild.addtransition(translations[fromstate], translations[state], tostates[state])
        return [rebuild, startnum] 

    def newBuildFromEquivalentStates(self, equivalent, pos):
        rebuild = Automata(self.language) # define automata 
        for fromstate, tostates in self.transitions.items(): # add tranisions
            for state in tostates: # in current state add all to state
                rebuild.addtransition(pos[fromstate], pos[state], tostates[state])
        rebuild.setstartstate(pos[self.startstate]) # set start state
        for s in self.finalstates: # set final states
            rebuild.addfinalstates(pos[s])
        return rebuild
    # DOT file represents a graph which consists of nodes and edges
    # Method for get dot file for the graph 
    def getDotFile(self):
        dotFile = "digraph DFA {\nrankdir=LR\n"
        if len(self.states) != 0:
            dotFile += "root=s1\nstart [shape=point]\nstart->s%d\n" % self.startstate
            for state in self.states:
                if state in self.finalstates:
                    dotFile += "s%d [shape=doublecircle]\n" % state
                else:
                    dotFile += "s%d [shape=circle]\n" % state
            for fromstate, tostates in self.transitions.items():
                for state in tostates:
                    for char in tostates[state]:
                        dotFile += 's%d->s%d [label="%s"]\n' % (fromstate, state, char)
        dotFile += "}"
        return dotFile

class BuildAutomata:
    """class for building nfa basic structures of NFA """
    # method for construct basic automata ex: constant construction 
    @staticmethod
    def basicstruct(inp):
        state1 = 1
        state2 = 2
        basic = Automata()
        basic.setstartstate(state1)
        basic.addfinalstates(state2)
        basic.addtransition(1, 2, inp)
        return basic
    # method for  construction of  or operator (+/|)
    @staticmethod
    def plusstruct(a, b):
        [a, m1] = a.newBuildFromNumber(2)  # to get new 
        [b, m2] = b.newBuildFromNumber(m1) # to get new 
        state1 = 1
        state2 = m2
        plus = Automata()
        plus.setstartstate(state1)
        plus.addfinalstates(state2)
        plus.addtransition(plus.startstate, a.startstate, Automata.epsilon())
        plus.addtransition(plus.startstate, b.startstate, Automata.epsilon())
        plus.addtransition(a.finalstates[0], plus.finalstates[0], Automata.epsilon())
        plus.addtransition(b.finalstates[0], plus.finalstates[0], Automata.epsilon())
        plus.addtransition_dict(a.transitions)
        plus.addtransition_dict(b.transitions)
        return plus
    # method for  construction of  dot operator (.) concatenate
    @staticmethod
    def dotstruct(a, b):
        [a, m1] = a.newBuildFromNumber(1)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2-1
        dot = Automata()
        dot.setstartstate(state1)
        dot.addfinalstates(state2)
        dot.addtransition(a.finalstates[0], b.startstate, Automata.epsilon())
        dot.addtransition_dict(a.transitions)
        dot.addtransition_dict(b.transitions)
        return dot

    # method for  construction of  star  operator (*) 
    @staticmethod
    def starstruct(a):
        [a, m1] = a.newBuildFromNumber(2)
        state1 = 1
        state2 = m1
        star = Automata()
        star.setstartstate(state1)
        star.addfinalstates(state2)
        star.addtransition(star.startstate, a.startstate, Automata.epsilon())
        star.addtransition(star.startstate, star.finalstates[0], Automata.epsilon())
        star.addtransition(a.finalstates[0], star.finalstates[0], Automata.epsilon())
        star.addtransition(a.finalstates[0], a.startstate, Automata.epsilon())
        star.addtransition_dict(a.transitions)
        return star


class DFAfromNFA:
    """class for building dfa from nfa and minimise it"""
    # constructor
    def __init__(self, nfa):
        self.buildDFA(nfa)
        self.minimise()
    
    #method for get DFA object
    def getDFA(self):
        return self.dfa

    
    def getMinimisedDFA(self):
        return self.minDFA

    #method for get DFA content 
    def displayDFA(self):
        self.dfa.display()

    def displayMinimisedDFA(self):
        self.minDFA.display()

    # method to build DFA from NFA
    def buildDFA(self, nfa):
        allstates = dict() # init dict for states
        eclose = dict() #init dict for closure 
        count = 1 
        state1 = nfa.getEClose(nfa.startstate) # first step : find e-closure of inital state
        eclose[nfa.startstate] = state1 # let's e-closure of inital state is state 1
        dfa = Automata(nfa.language) # get posible input 
        dfa.setstartstate(count) # init or set start state 
        states = [[state1, count]] # insert into list
        allstates[count] = state1 # insert int dict of all state in grapgh ex:(1,{0,1,3,4})
        count +=  1 # for next state
        while len(states) != 0:
            [state, fromindex] = states.pop()
            for char in dfa.language:
                # to find transion 
                trstates = nfa.gettransitions(state, char)
                # loop for check move with e to get next state set 
                for s in list(trstates)[:]:
                    if s not in eclose:
                        eclose[s] = nfa.getEClose(s)
                    trstates = trstates.union(eclose[s])
                if len(trstates) != 0:
                    if trstates not in allstates.values():
                        states.append([trstates, count]) # insert into list
                        allstates[count] = trstates
                        toindex = count
                        count +=  1 #for next state
                    else:
                        toindex = [k for k, v in allstates.items() if v  ==  trstates][0]
                    dfa.addtransition(fromindex, toindex, char) # add transion of DFA 
        for value, state in allstates.items():
            if nfa.finalstates[0] in state: # check if it is final state
                dfa.addfinalstates(value) # add final state of DFA
        self.dfa = dfa
    # method for check if string is accepted or not
    def acceptsString(self, string):
        currentstate = self.dfa.startstate  # start from start state
        for ch in string: 
            if ch==":e:": # if it is epsilon
                continue
            st = list(self.dfa.gettransitions(currentstate, ch)) # else move depend on inp
            if len(st) == 0: # not belong to set of strings
                return False
            currentstate = st[0] # continue
        if currentstate in self.dfa.finalstates: # if its reach to accept state or final
            return True # belong to set of string
        return False # in case dose not reach to accept state or final

    
    def minimise(self):
        states = list(self.dfa.states)
        n = len(states)
        unchecked = dict()
        count = 1
        distinguished = []
        equivalent = dict(zip(range(len(states)), [{s} for s in states]))
        pos = dict(zip(states,range(len(states))))
        for i in range(n-1):
            for j in range(i+1, n):
                if not ([states[i], states[j]] in distinguished or [states[j], states[i]] in distinguished):
                    eq = 1
                    toappend = []
                    for char in self.dfa.language:
                        s1 = self.dfa.gettransitions(states[i], char)
                        s2 = self.dfa.gettransitions(states[j], char)
                        if len(s1) != len(s2):
                            eq = 0
                            break
                        if len(s1) > 1:
                            raise BaseException("Multiple transitions detected in DFA")
                        elif len(s1) == 0:
                            continue
                        s1 = s1.pop()
                        s2 = s2.pop()
                        if s1 != s2:
                            if [s1, s2] in distinguished or [s2, s1] in distinguished:
                                eq = 0
                                break
                            else:
                                toappend.append([s1, s2, char])
                                eq = -1
                    if eq == 0:
                        distinguished.append([states[i], states[j]])
                    elif eq == -1:
                        s = [states[i], states[j]]
                        s.extend(toappend)
                        unchecked[count] = s
                        count += 1
                    else:
                        p1 = pos[states[i]]
                        p2 = pos[states[j]]
                        if p1 != p2:
                            st = equivalent.pop(p2)
                            for s in st:
                                pos[s] = p1
                            equivalent[p1] = equivalent[p1].union(st)
        newFound = True
        while newFound and len(unchecked) > 0:
            newFound = False
            toremove = set()
            for p, pair in unchecked.items():
                for tr in pair[2:]:
                    if [tr[0], tr[1]] in distinguished or [tr[1], tr[0]] in distinguished:
                        unchecked.pop(p)
                        distinguished.append([pair[0], pair[1]])
                        newFound = True
                        break
        for pair in unchecked.values():
            p1 = pos[pair[0]]
            p2 = pos[pair[1]]
            if p1 != p2:
                st = equivalent.pop(p2)
                for s in st:
                    pos[s] = p1
                equivalent[p1] = equivalent[p1].union(st)
        if len(equivalent) == len(states):
            self.minDFA = self.dfa
        else:
            self.minDFA = self.dfa.newBuildFromEquivalentStates(equivalent, pos)
    

class NFAfromRegex:
    """class for building nfa from regular expressions"""
    # constructor 
    def __init__(self, regex):
        self.star = '*'
        self.plus = '+'
        self.dot = '.'
        self.openingBracket = '('
        self.closingBracket = ')'
        self.operators = [self.plus, self.dot]
        self.regex = regex
        self.alphabet = [chr(i) for i in range(65,91)] # from A to Z
        self.alphabet.extend([chr(i) for i in range(97,123)]) # from a to z
        self.alphabet.extend([chr(i) for i in range(48,58)]) #symbol
        self.buildNFA()

    #method for get NFA object
    def getNFA(self):
        return self.nfa
 
    #method for get NFA content
    def displayNFA(self):
        self.nfa.display()

    # method to build NFA
    def buildNFA(self):
        language = set() # init set 
        self.stack = [] # init stack 
        self.automata = [] # init list 
        previous = "::e::" #epsilon 
        # for charcter in Ruglar expression
        for char in self.regex: 
            if char in self.alphabet: #if it is langauge
                language.add(char) # add it 
                # if it is not dot before the char then add dot to stack and it is alphabet or closing bracket or star 
                if previous != self.dot and (previous in self.alphabet or previous in [self.closingBracket,self.star]):
                    self.addOperatorToStack(self.dot)
                # else build basic 
                self.automata.append(BuildAutomata.basicstruct(char)) 
            # else if is ( 
            elif char  ==  self.openingBracket:
                 # if it is not dot before the char then add dot to stack and it is alphabet or closing bracket or star 
                if previous != self.dot and (previous in self.alphabet or previous in [self.closingBracket,self.star]):
                    self.addOperatorToStack(self.dot)
                # else add to stack 
                self.stack.append(char)
            # else if is )
            elif char  ==  self.closingBracket:
                # if it is + or . (plus or dot)
                if previous in self.operators:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                while(1):
                    if len(self.stack) == 0: # error
                        raise BaseException("Error processing '%s'. Empty stack" % char)
                    # pop of stack 
                    o = self.stack.pop()
                    if o == self.openingBracket:
                        break
                    elif o in self.operators: # plus or dot
                        self.processOperator(o) 
            # else if is * star
            elif char == self.star:
                if previous in self.operators or previous  == self.openingBracket or previous == self.star:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                self.processOperator(char)
            # else if is + or . 
            elif char in self.operators:
                if previous in self.operators or previous  == self.openingBracket:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                else:
                    self.addOperatorToStack(char) #add to stack 
            # else any other case error massage 
            else:
                raise BaseException("Symbol '%s' is not allowed" % char)
            previous = char # update previous by char 
        # pop for all operator in stake 
        while len(self.stack) != 0:
            op = self.stack.pop()
            self.processOperator(op)
        # if more than one NFA in the end must be one 
        if len(self.automata) > 1:
            print (self.automata)
            raise BaseException("Regex could not be parsed successfully")
        self.nfa = self.automata.pop()
        self.nfa.language = language # put language 

    # method to add + or dot into stack for construction
    def addOperatorToStack(self, char):
        while(1):
            if len(self.stack) == 0:
                break
            top = self.stack[len(self.stack)-1]
            if top == self.openingBracket:
                break
            # check it is char or dor to pop 
            if top == char or top == self.dot:
                op = self.stack.pop()
                self.processOperator(op)
            else:
                break
        self.stack.append(char) # add to stack 

    #method for build operator 
    def processOperator(self, operator):
        if len(self.automata) == 0:
            raise BaseException("Error processing operator '%s'. Stack is empty" % operator)
        if operator == self.star:
            a = self.automata.pop()
            self.automata.append(BuildAutomata.starstruct(a)) # build star structure
        elif operator in self.operators: # if it is plus or dot 
            if len(self.automata) < 2: # must two operaend for + and . operator 
                raise BaseException("Error processing operator '%s'. Inadequate operands" % operator)
            a = self.automata.pop() # pop a
            b = self.automata.pop() # pop b
            if operator == self.plus:
                self.automata.append(BuildAutomata.plusstruct(b,a)) # build plus structure
            elif operator == self.dot:
                self.automata.append(BuildAutomata.dotstruct(b,a)) # build dot structure

# method for drawing graph 
def drawGraph(automata, file = ""):
    """From https://github.com/max99x/automata-editor/blob/master/util.py"""
    f = popen(r"dot -Tpng -o graph%s.png" % file, 'w')
    try:
        f.write(automata.getDotFile()) # get graph and write in f file 
    except:
        raise BaseException("Error creating graph") # error
    finally:
        f.close() # close f file 

#method for install image of graph 
def isInstalled(program):
    """From http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python"""
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program) or is_exe(program+".exe"):
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file) or is_exe(exe_file+".exe"):
                return True
    return False
