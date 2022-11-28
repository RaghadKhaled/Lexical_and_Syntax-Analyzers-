from tkinter import *
from PIL import ImageTk, Image
from tkinter.scrolledtext import ScrolledText
import main

root = Tk()
root.title("LL(1) parsar")
# root.minsize(1200, 800)

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# setting tkinter window size
root.geometry("%dx%d" % (width, height))


def click_button():

    """
    P: PROGRAM
    S: STMTS
    L: STMTS’
    M: STMT
    E: EXPR
    R: EXPR’
    T: TERM
    N: TERM’
    O: POWER
    W: POWER’
    F: FACTOR
    """

    rules = [
        "P -> S",
        "S -> M L",
        "L -> # | ; S",
        "M -> id = E",
        "E -> T R",
        "R -> + T R | - T R | #",
        "T -> O N",
        "N -> * O N | / O N | #",
        "O -> F W",
        "W -> ^ O | #",
        "F -> ( E ) | id | integer | @ F | ! F"
    ]
    non_term_user_def = ['P', 'S', 'L', 'M', 'E', 'R', 'T', 'N', 'O', 'W', 'F']
    term_user_def = [';', 'id', '=', '+', '-', '*', '/', '^', '(', ')', 'integer', '@', '!']

    Text_5.delete('1.0', END)
    Text_6.delete('1.0', END)
    # set vertical non terminals (start)
    Text_8.delete('1.0', END)
    Text_9.delete('1.0', END)
    Text_10.delete('1.0', END)
    Text_11.delete('1.0', END)
    Text_12.delete('1.0', END)
    Text_13.delete('1.0', END)
    Text_14.delete('1.0', END)
    Text_15.delete('1.0', END)
    Text_16.delete('1.0', END)
    Text_17.delete('1.0', END)
    Text_18.delete('1.0', END)
    # set vertical non terminals (start)

    # set horizontal terminals (start)
    Text_19.delete('1.0', END)
    Text_20.delete('1.0', END)
    Text_21.delete('1.0', END)
    Text_22.delete('1.0', END)
    Text_23.delete('1.0', END)
    Text_24.delete('1.0', END)
    Text_25.delete('1.0', END)
    Text_26.delete('1.0', END)
    Text_27.delete('1.0', END)
    Text_28.delete('1.0', END)
    Text_29.delete('1.0', END)
    Text_30.delete('1.0', END)
    Text_31.delete('1.0', END)
    Text_32.delete('1.0', END)
    # set horizontal terminals (start)

    sample_input_string = Text_1.get("1.0", 'end-1c')


    # diction - store rules inputted
    diction = {}
    # firsts - store computed firsts
    firsts = {}
    # follows - store computed follows
    follows = {}

    # computes all FIRSTs for all non-terminals
    firsts = main.computeAllFirsts(rules, non_term_user_def, term_user_def, diction, firsts)
    print(firsts)
    # assuming first rule has start_symbol
    start_symbol = list(diction.keys())[0]

    # computes all follows for all non-terminals
    follows = main.computeAllFollows(start_symbol, rules, non_term_user_def, term_user_def, diction, firsts, follows)

    # then generate parse table, after we compute first and follow
    (parsing_table, result, tabTerm, first_and_follow, pares_table_string) = main.createParseTable()

    Text_6.insert("1.0", first_and_follow)
    # Text_4.insert("1.0", pares_table_string)

    # validate string input using stack-buffer concept
    if sample_input_string is not None:
        validity, stack_string = main.validateStringUsingStackBuffer(parsing_table, result,
                                                                     tabTerm, sample_input_string,
                                                                     term_user_def, start_symbol)

        Text_5.insert("1.0", stack_string)
        Label_7.config(text=validity)
        print(validity)
    else:
        print("\nNo input String detected")

    # set vertical non terminals (start)
    Text_8.insert('1.0', non_term_user_def[0])
    Text_9.insert('1.0', non_term_user_def[1])
    Text_10.insert('1.0', non_term_user_def[2])
    Text_11.insert('1.0', non_term_user_def[3])
    Text_12.insert('1.0', non_term_user_def[4])
    Text_13.insert('1.0', non_term_user_def[5])
    Text_14.insert('1.0', non_term_user_def[6])
    Text_15.insert('1.0', non_term_user_def[7])
    Text_16.insert('1.0', non_term_user_def[8])
    Text_17.insert('1.0', non_term_user_def[9])
    Text_18.insert('1.0', non_term_user_def[10])
    # set vertical non terminals (start)

    # set horizontal terminals (start)
    Text_19.insert('1.0', term_user_def[0])
    Text_20.insert('1.0', term_user_def[1])
    Text_21.insert('1.0', term_user_def[2])
    Text_22.insert('1.0', term_user_def[3])
    Text_23.insert('1.0', term_user_def[4])
    Text_24.insert('1.0', term_user_def[5])
    Text_25.insert('1.0', term_user_def[6])
    Text_26.insert('1.0', term_user_def[7])
    Text_27.insert('1.0', term_user_def[8])
    Text_28.insert('1.0', term_user_def[9])
    Text_29.insert('1.0', term_user_def[10])
    Text_30.insert('1.0', term_user_def[11])
    Text_31.insert('1.0', term_user_def[12])
    Text_32.insert('1.0', '$')
    # set horizontal terminals (start)

    X_position = 300
    Y_postion = 60
    for x in range(len(parsing_table)):
        for y in range(len(parsing_table[x])):
            Text_33 = Text(root, width=8, height=1, borderwidth=0)
            Text_33.grid(row=x, column=y)
            Text_33.insert( END,parsing_table[x][y])
            Text_33.place(x=X_position, y=Y_postion)
            X_position += 75
        Text_33.place(x=X_position, y= Y_postion)
        Y_postion += 30
        X_position = 300

# ----------- Image logo (start)

frame = Frame(root, width=30, height=40)
frame.pack()
frame.place(anchor='center', x=850, y=200)

# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("LL(1) parser logo.jpg"))

# Create a Label Widget to display the text or Image
label = Label(frame, image = img)
label.pack()

# ----------- Image logo (end)

# --------------------Input string (start)
Label_1 = Label(root, text='Input string:', font='Times 14')
Label_1.place(height=20, width=400, x=85, y=640)

Label_7 = Label(root, text='', font='Times 14')
Label_7.place(height=100, width=400, x=150, y=500)

Text_1 = Text(root, borderwidth=2)
Text_1.place(height=20, width=210, x=235, y=680)

Button_1 = Button(root, text="Check", background='#A3A3C6', font='Times 14', command=click_button)
Button_1.place(height=30, width=100, x=290, y=720)

# --------------------Input string (end)

# ----------------------Rule after modifications (start)
Label_2 = Label(root, text='Rules after modifications', font='Times 14')
Label_2.place(height=20, width=200, x=15, y=330)

Text_2 = Text(root, width=50, height=1, borderwidth=0, background='#D8D0EF')
Text_2.place(height=400, width=200, x=20, y=360)

rules_a_m = "P -> S\n\nS -> M L\n\nL -> # | ; S\n\nM -> id = E\n\nE -> T R\n\nR -> + T R | - T R | #" \
            "\n\nT -> O N\n\nN -> * O N | / O N | #\n\nO -> F W\n\nW -> ^ O | #\n\n" \
            "F -> ( E ) | id |\ninteger | @ F | ! F"


Text_2.insert("1.0", rules_a_m)

# ----------------------Rule after modifications (end)

# ----------------------Rule before modifications (start)
Label_3 = Label(root, text='Rules before modifications', font='Times 14')
Label_3.place(height=20, width=200, x=15, y=30)

Text_3 = Text(root, width=50, height=1, borderwidth=0, bg="#F7F6D1")
Text_3.place(height=240, width=200, x=20, y=60)

rules_b_m = "P -> S\n\nS -> M | M ; S\n\nM -> id = E\n\nE -> E + T | E - T | T" \
            "\n\nT -> T * O | T / O | O\n\nO -> F ^ O | F\n\nF -> ( E ) | id |\n integer | @ F | ! F "

Text_3.insert("1.0", rules_b_m)
# ----------------------Rule before modifications (end)

# ----------------------Parsing table (start)

# ------------------------ horizontal text or Non-terminals (start)
Text_8 = Text(root, width=50, height=1, borderwidth=0)
Text_8.place(height=20, width=20, x=270, y=60)

Text_9 = Text(root, width=50, height=1, borderwidth=0)
Text_9.place(height=20, width=20, x=270, y=90)

Text_10 = Text(root, width=50, height=1, borderwidth=0)
Text_10.place(height=20, width=20, x=270, y=120)

Text_11 = Text(root, width=50, height=1, borderwidth=0)
Text_11.place(height=20, width=20, x=270, y=150)

Text_12 = Text(root, width=50, height=1, borderwidth=0)
Text_12.place(height=20, width=20, x=270, y=180)

Text_13 = Text(root, width=50, height=1, borderwidth=0)
Text_13.place(height=20, width=20, x=270, y=210)

Text_14 = Text(root, width=50, height=1, borderwidth=0)
Text_14.place(height=20, width=20, x=270, y=240)

Text_15 = Text(root, width=50, height=1, borderwidth=0)
Text_15.place(height=20, width=20, x=270, y=270)

Text_16 = Text(root, width=50, height=1, borderwidth=0)
Text_16.place(height=20, width=20, x=270, y=300)

Text_17 = Text(root, width=50, height=1, borderwidth=0)
Text_17.place(height=20, width=20, x=270, y=330)

Text_18 = Text(root, width=50, height=1, borderwidth=0)
Text_18.place(height=20, width=20, x=270, y=360)

# ------------------------ horizontal text for Non-terminals (end)

# ------------------------ Vertical text for terminals (start)
Text_19 = Text(root, borderwidth=0)
Text_19.place(height=20, width=20, x=330, y=35)

Text_20 = Text(root, borderwidth=0)
Text_20.place(height=20, width=60, x=380, y=35)

Text_21 = Text(root, borderwidth=0)
Text_21.place(height=20, width=10, x=480, y=35)

Text_22 = Text(root, width=50, height=1, borderwidth=0)
Text_22.place(height=20, width=10, x=550, y=35)

Text_23 = Text(root, width=50, height=1, borderwidth=0)
Text_23.place(height=20, width=10, x=630, y=35)

Text_24 = Text(root, width=50, height=1, borderwidth=0)
Text_24.place(height=20, width=10, x=700, y=35)

Text_25 = Text(root, width=50, height=1, borderwidth=0)
Text_25.place(height=20, width=10, x=780, y=35)

Text_26 = Text(root, width=50, height=1, borderwidth=0)
Text_26.place(height=20, width=10, x=850, y=35)

Text_27 = Text(root, width=50, height=1, borderwidth=0)
Text_27.place(height=20, width=10, x=930, y=35)

Text_28 = Text(root, width=50, height=1, borderwidth=0)
Text_28.place(height=20, width=10, x=1000, y=35)

Text_29 = Text(root, width=50, height=1, borderwidth=0)
Text_29.place(height=20, width=10, x=1080, y=35)

Text_30 = Text(root, width=50, height=1, borderwidth=0)
Text_30.place(height=20, width=10, x=1150, y=35)

Text_31 = Text(root, width=50, height=1, borderwidth=0)
Text_31.place(height=20, width=10, x=1225, y=35)

Text_32 = Text(root, width=50, height=1, borderwidth=0)
Text_32.place(height=20, width=10, x=1380, y=35)

# ------------------------ Vertical text for Non-terminals (end)

# ----------------------Parsing table  (end)

# ----------------------Stack (start)
Label_5 = Label(root, text='Stack', font='Times 14')
Label_5.place(height=20, width=200, x=1050, y=430)

Text_5 = ScrolledText(root)
# Text(root, width=50, height=1, borderwidth=2)
Text_5.place(height=300, width=550, x=890, y=460)
# ----------------------Stack (end)

# ----------------------First && Follow table (start)
Label_6 = Label(root, text='First and Follow table', font='Times 14')
Label_6.place(height=20, width=200, x=550, y=430)

Text_6 = ScrolledText(root, width=50, height=10)
# Text(root, width=50, height=1, borderwidth=2)
Text_6.place(height=300, width=400, x=470, y=460)

# ----------------------First && Follow table (end)

root.mainloop()
