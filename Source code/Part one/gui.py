
try:
    from tkinter import * # import tkinter library for GUI
    import tkinter.font as tkFont # import tkFont class for GUI
except ImportError as err: # for error in instalision of library
    print ("error: %s. Tkinter library is required for using the GUI.") % err.message
    sys.exit(1)

# import AutomataTheory for construct RE to NFA and NFA to DFA 
from AutomataTheory import * 
# import DFAfromRE for construct RE to DFA 
from DFAfromRE import *

dotFound = isInstalled("dot") # install image 
if dotFound:
    try:
        #import Python Imaging Library for image processing and display graph 
        from PIL import Image, ImageTk 
    except ImportError as err:
        print ("Notice: %s. The PIL library is required for displaying the graphs.") % err.message
        dotFound = False
else:
    print ("Notice: The GraphViz software is required for displaying the graphs.")

# class of creating GUI
class AutomataGUI:

    def __init__(self, root, dotFound):
        self.root = root
        self.initUI() # call method to init GUI
        self.selectedButton = 0 # for button selection 
        self.dotFound = dotFound #for graph
        startRegex = "" # string of reuglar expression
        # regexVar for manage the value of a widget such as an Entry widget or a Label widget
        self.regexVar.set(startRegex) 
        # for handle button selection 
        self.handleBuildRegexButton()

    # method creat GUI
    def initUI(self):
        self.root.title("Finite Automata") # title 
        # screen setting 
        ScreenSizeX = self.root.winfo_screenwidth()
        ScreenSizeY = self.root.winfo_screenheight()
        ScreenRatioX = 0.9
        ScreenRatioY = 1.0
        self.FrameSizeX  = int(ScreenSizeX * ScreenRatioX)
        self.FrameSizeY  = int(ScreenSizeY * ScreenRatioY)
        FramePosX   = (ScreenSizeX - self.FrameSizeX)/2
        FramePosY   = (ScreenSizeY - self.FrameSizeY)/2
        padX = 15
        padY = 15
        # creating main window
        self.root.geometry("%dx%d+%d+%d" % (self.FrameSizeX,self.FrameSizeY,FramePosX,FramePosY))
        self.root.resizable(width=False, height=False)
        # creatin frame
        parentFrame = Frame(self.root, width = int(self.FrameSizeX - 2*padX), height = int(self.FrameSizeY - 2*padY))
        parentFrame.grid(padx=padX, pady=padY, stick=E+W+N+S)

        regexFrame = Frame(parentFrame) # frame of regular expression
        # creating label
        enterRegexLabel = Label(regexFrame, text="Enter regular expression [operators allowed are plus (+), dot (.) and star (*)]:")
        self.regexVar = StringVar()
        self.regexField = Entry(regexFrame, width=80, textvariable=self.regexVar) # entry regular expression
        buildRegexButton = Button(regexFrame, text="Build", width=10, command=self.handleBuildRegexButton)
        # setting :
        enterRegexLabel.grid(row=0, column=0, sticky=W)
        self.regexField.grid(row=1, column=0, sticky=W)
        buildRegexButton.grid(row=1, column=1, padx=5)
        # creatin frame
        testStringFrame = Frame(parentFrame)
        testStringLabel = Label(testStringFrame, text="Enter a test string: ") # creating label
        self.testVar = StringVar()
        self.testStringField = Entry(testStringFrame, width=80, textvariable=self.testVar) # entry string
        testStringButton = Button(testStringFrame, text="Test", width=10, command=self.handleTestStringButton)
        # setting :
        testStringLabel.grid(row=0, column=0, sticky=W)
        self.testStringField.grid(row=1, column=0, sticky=W)
        testStringButton.grid(row=1, column=1, padx=5)

        self.statusLabel = Label(parentFrame) # creating label

        buttonGroup = Frame(parentFrame)
        self.timingLabel = Label(buttonGroup, text="Tasks : ", width=50, justify=RIGHT)
        # creating button 
        nfaButton = Button(buttonGroup, text="RE to NFA", width=15, command=self.handlenfaButton)
        dfaButton = Button(buttonGroup, text="NFA to DFA", width=15, command=self.handledfaButton)
        minDFAButton = Button(buttonGroup, text="RE to DFA", width=15, command=self.handleminDFAButton)
        # setting :
        self.timingLabel.grid(row=0, column=0, sticky=W)
        nfaButton.grid(row=0, column=1)
        dfaButton.grid(row=0, column=2)
        minDFAButton.grid(row=0, column=3)

        # creat frame of implemention taska  
        automataCanvasFrame = Frame(parentFrame, height=100, width=100)
        self.cwidth = int(self.FrameSizeX - (2*padX + 20))
        self.cheight = int(self.FrameSizeY * 0.6)
        self.automataCanvas = Canvas(automataCanvasFrame, bg='#FFFFFF', width= self.cwidth, height = self.cheight,scrollregion=(0,0,self.cwidth,self.cheight))
        hbar=Scrollbar(automataCanvasFrame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.automataCanvas.xview)
        vbar=Scrollbar(automataCanvasFrame,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.automataCanvas.yview)
        self.automataCanvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvasitems = []
        self.automataCanvas.pack()

        # setting :  
        regexFrame.grid(row=0, column=0, sticky=W, padx=(50,0))
        testStringFrame.grid(row=1, column=0, sticky=W, padx=(50,0))
        self.statusLabel.grid(row=2, column=0, sticky=W, padx=(50,0))
        buttonGroup.grid(row=3, column=0)
        automataCanvasFrame.grid(row=4, column=0, sticky=E+W+N+S)

    # get action of button to do tasks
    def handleBuildRegexButton(self):
        t = time.time()
        try:
            inp = self.regexVar.get().replace(' ','') # get reuglar expression
            if inp == '':
                self.statusLabel.config(text="Detected empty regex!")
                return
            self.createAutomata(inp) # start creat NFA and NFA to DFA
        except BaseException as e:
            self.statusLabel.config(text="Failure: %s" % e)
        # for time 
        self.timingLabel.configure(text="Operation completed in " + "%.4f" % (time.time() - t) + " seconds")
        # for display graph
        self.displayAutomata()

    # get action of button to do string check
    def handleTestStringButton(self):
        t = time.time()
        inp = self.testVar.get().replace(' ','') # get string
        if inp == '':
            inp = [':e:']
        if self.dfaObj.acceptsString(inp): # check
            self.statusLabel.config(text="Accepts :)")
        else:
            self.statusLabel.config(text="Does not accept :|")
        self.timingLabel.configure(text="Operation completed in " + "%.4f" % (time.time() - t) + " seconds")

    # method to set selected button 
    def handlenfaButton(self):
        self.selectedButton = 0
        self.displayAutomata()

    # method to set selected button 
    def handledfaButton(self):
        self.selectedButton = 1
        self.displayAutomata()

    # method to set selected button 
    def handleminDFAButton(self):
        self.selectedButton = 2
        self.displayAutomata()

    def createAutomata(self, inp):
        print ("Regex: ", inp)
        nfaObj = NFAfromRegex(inp) # from reuglar expression to NFA
        self.nfa = nfaObj.getNFA() # get NFA
        self.dfaObj = DFAfromNFA(self.nfa) # from NFA to DFA
        self.dfa = self.dfaObj.getDFA() #get DFA
        self.minDFA = self.dfaObj.getMinimisedDFA() # to get the graph of RE to DFA
        self.DFA = RegexLexer(inp) # RE to DFA
        self.DFA.printAST() # to construct syntax tree
        self.mdfa = Converter(self.DFA.parts) # take RE with syntax tree to find first,last,follow
        
        if self.dotFound: # creating graph
            drawGraph(self.dfa, "dfa")
            drawGraph(self.nfa, "nfa")
            drawGraph(self.minDFA, "mdfa")
            dfafile = "graphdfa.png"
            nfafile = "graphnfa.png"
            mindfafile = "graphmdfa.png"
            self.nfaimagefile = Image.open(nfafile)
            self.dfaimagefile = Image.open(dfafile)
            self.mindfaimagefile = Image.open(mindfafile)
            self.nfaimg = ImageTk.PhotoImage(self.nfaimagefile)
            self.dfaimg = ImageTk.PhotoImage(self.dfaimagefile)
            self.mindfaimg = ImageTk.PhotoImage(self.mindfaimagefile)

    # to display int GUI
    def displayAutomata(self):
        for item in self.canvasitems:
            self.automataCanvas.delete(item)
        if self.selectedButton == 0:
            header = "RE to NFA"
            automata = self.nfa
            if self.dotFound:
                image = self.nfaimg
                imagefile = self.nfaimagefile
        elif self.selectedButton == 1:
            header = "NFA to DFA"
            automata = self.dfa
            if self.dotFound:
                image = self.dfaimg
                imagefile = self.dfaimagefile
        elif self.selectedButton == 2:
            header = "RE to DFA"
            automata = self.minDFA
            if self.dotFound:
                image = self.mindfaimg
                imagefile = self.mindfaimagefile
            automata = self.mdfa
        # setting :
        font = tkFont.Font(family="times", size=20)
        (w,h) = (font.measure(header),font.metrics("linespace"))
        headerheight = h + 10
        itd = self.automataCanvas.create_text(10,10,text=header, font=font, anchor=NW)
        self.canvasitems.append(itd)
        [text, linecount] = automata.getPrintText()
        font = tkFont.Font(family="times", size=13)
        (w,h) = (font.measure(text),font.metrics("linespace"))
        textheight = headerheight + linecount * h + 20
        itd = self.automataCanvas.create_text(10, headerheight + 10,text=text, font=font, anchor=NW)
        self.canvasitems.append(itd)
        if self.dotFound:
            itd = self.automataCanvas.create_image(10, textheight, image=image, anchor=NW)
            self.canvasitems.append(itd)
            totalwidth = imagefile.size[0] + 10
            totalheight = imagefile.size[1] + textheight + 10
        else:
            totalwidth = self.cwidth + 10
            totalheight = textheight + 10
        if totalheight < self.cheight:
            totalheight = self.cheight
        if totalwidth < self.cwidth:
            totalwidth = self.cwidth
        self.automataCanvas.config(scrollregion=(0,0,totalwidth,totalheight))

# main 
def main():
    global dotFound
    root = Tk()
    app = AutomataGUI(root, dotFound)
    root.mainloop()

if __name__ == '__main__':
    main()
