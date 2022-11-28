
# pass rule in first function
def first(rule, non_term_user_def, term_user_def, diction, firsts):  # EX: rule = sub = ['A', 'k', 'O']

    # This is a (recursion base case)
    # if terminal or epsilon return it as is
    if len(rule) != 0 and (rule is not None):
        # if rule[0] is terminal
        if rule[0] in term_user_def:
            return rule[0]
        # if rule[0] is epsilon
        elif rule[0] == '#':
            return '#'

    # if Non-Terminals
    if len(rule) != 0:
        if rule[0] in list(diction.keys()):

            # fres temporary list of result
            fres = []

            # bring rule[0] RHS, EX: rule[0]='A', RHS of 'A' is ['a', "A''"]
            rhs_rules = diction[rule[0]]

            # call first on each rule of RHS
            for itr in rhs_rules:
                # recursive call first(itr) , EX:  its = 'a' in the first iteration
                indivRes = first(itr, non_term_user_def, term_user_def, diction, firsts)

                # if first of its is a list, then we will append all elements in the list to fres list.
                if type(indivRes) is list:
                    for i in indivRes:
                        fres.append(i)
                # if first it just single element
                else:
                    fres.append(indivRes)

            # if no epsilon in result received return fres
            if '#' not in fres:
                return fres

            # if epsilon in result received return fres
            else:
                # apply epsilon, rule => f(ABC)=f(A)-{e} U f(BC)
                newList = []
                # remove epsilon from fres
                fres.remove('#')

                # if rule have more than one element, rule = ['A', 'B', 'C']  , A --> d | #
                if len(rule) > 1:

                    # find first for all rules after rule[0], EX: ['B', 'C']
                    ansNew = first(rule[1:])

                    # if ansNew is not empty
                    if ansNew != None:
                        # if ansNew is a list
                        if type(ansNew) is list:
                            newList = fres + ansNew
                        # if ansNew is an element
                        else:
                            newList = fres + [ansNew]

                    # if ansNew is empty
                    else:
                        newList = fres
                    return newList
                """
                if there are no element in rule after rule[0] and First(rule[0]) contains epsilon then we will add it again
                """
                fres.append('#')
                return fres


"""
calculation of follow use 'rules' list, and 'diction' dict from above follow function input is the split result on
Non-Terminal whose Follow we want to compute
"""


def follow(nt, start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows):
    # create new set to store result of computed 'follow'
    solset = set()

    # for start symbol return $ (recursion base case)
    if nt == start_symbol:
        # return '$'
        solset.add('$')

    # for each non-terminal
    for curNT in diction:  # PROGRAM, 'STMTS','STMT', 'EXPR', 'TERM', 'FACTOR', 'EXPONENT', 'FINAL','STMTS\'','EXPR\'','TERM\'','FACTOR\'']
        # curNT RHS
        """
        rules = ["S -> A B C | C",
        "A -> a | b B | #",
        "B -> p | #",
        "C -> c"] C--> c | #
        """
        # print('solset: ',solset)

        rhs = diction[curNT]
        # go for all productions of NT

        for subrule in rhs:
            if nt in subrule:
                # print('nt: ', nt)
                while nt in subrule:
                    # find index of nt
                    index_nt = subrule.index(nt)

                    # bring all element after nt
                    subrule = subrule[index_nt + 1:]

                    # empty condition - call follow on LHS
                    if len(subrule) != 0:
                        # compute first if symbols on RHS of target Non-Terminal exists
                        res = first(subrule, non_term_user_def, term_user_def, diction, firsts)

                        # if epsilon in result apply rule - (A->aBX)- follow of / follow(B)=(first(X)-{ep}) U follow(A)
                        if '#' in res:
                            # create a new list
                            newList = []

                            # remove epsilon from res
                            res.remove('#')

                            # find follow of curNT
                            ansNew = follow(curNT, start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts,
                                            follows)

                            # if ansNew is not empty
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = res + ansNew
                                else:
                                    newList = res + [ansNew]
                            # if ansNew is empty
                            else:
                                newList = res
                            res = newList

                    else:
                        # when nothing in RHS, go circular and take follow of LHS only if (NT in LHS)!=curNT
                        if nt != curNT:

                            List = []

                            if nt == 'S' or nt == 'W' or nt == "L" or "O":
                                if nt == 'S' or nt == "L":
                                    for i in follows[start_symbol]:
                                        List.append(i)

                                    res = List
                                    return List

                                elif nt == 'W' or nt == "O":

                                    first_T_ = firsts["N"]
                                    for i in first_T_:
                                        if i == '#':
                                            continue
                                        List.append(i)

                                    for j in follows['T']:
                                        List.append(j)

                                    res = List
                                    return List

                            res = follow(curNT, start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts,
                                         follows)

                    # add follow result in set form
                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)


def print_all(diction, desctiption):
    print(f"\n Rules {desctiption} \n")
    for y in diction:
        print(f"{y}->{diction[y]}")


def preprocesssing(rules, diction):
    """
        :param rules: store rules before processing
        :param nonterm_userdef: List of all non-terminals
        :param term_userdef: List of all terminals
        :param diction: store rules after processing (Now it is empty)
        :param firsts: store computed firsts (Now it is empty)
        :return: return first for each non-terminal
        """
    # loop on each rule to remove unnecessary spaces
    for rule in rules:  # EX: "A -> A d | a B | a C"
        k = rule.split("->")  # EX: "k = ['A ',' A d | a B | a C ']"

        # remove spaces from LHS and RHS of the rule
        k[0] = k[0].strip()  # EX: k[0] = 'k'
        k[1] = k[1].strip()  # EX: k[1] = 'A d | a B | a C'

        # store k[1] which is the RHS of the rule in variable RHS
        RHS = k[1]  # RHS = 'A d | a B | a C'

        # split RHS and then store it in multirhs list
        multirhs = RHS.split('|')  # multirhs = ['A d ',' a B ',' a C']

        # remove spaces from each element in the list multirhs (multirhs[i]) and then split each element if we find a space
        for i in range(len(multirhs)):
            # Befor strip: multirhs[0] = 'A d ', multirhs[1] = ' a B ', multirhs[2] = ' a C'
            multirhs[i] = multirhs[i].strip()
            # After strip:multirhs[0] = 'A d', multirhs[1] = 'a B', multirhs[2] = 'a C'

            # split each element in the list multirhs (multirhs[i]) and then store it again in multirhs[i]
            multirhs[i] = multirhs[i].split()  # multirhs[0] = ['A','d'] ,multirhs[1] = ['a','B'], multirhs[2] = ['a','C']

        # store the rule after the processes (remove spaces, split)
        diction[k[0]] = multirhs  # {'S': [['A', 'k', 'O']], 'A': [['A', 'd'], ['a', 'B'], ['a', 'C']]}

    # # print all rules in the screen
    # print_all(diction, ':')

    # eliminate left recursion
    # diction = removeLeftRecursion(diction)

    # print all rules in the screen
    # print_all(diction, 'after elimination of left recursion:')

    # eliminate left factoring
    # diction = LeftFactoring(diction)

    # print all rules after left factoring
    # print_all(diction, 'after elimination of left factoring:')

    return diction


def computeAllFirsts(rules, nonterm_userdef, term_userdef, diction, firsts):
    # clean all rules (strip and split rules, eliminate left recursion, eliminate left factoring)
    diction = preprocesssing(rules, diction)
    """
    All rules until now:
    S->[['A', 'k', 'O']]
    A->[['a', "A''"]]
    A''->[['B', "A'"], ['C', "A'"]]
    C->[['c']]
    B->[['b', 'B', 'C'], ['r']]
    A'->[['d', "A'"], ['#']]
    """

    # calculate first for each rule  (call first() on all RHS)
    # diction.keys() --> bring all non-terminals , EX: [S,A,A'',C,B,A'], y = 'S' in the first iteration
    for y in list(diction.keys()):

        # create new set t
        t = set()

        """
        diction.get(y) --> bring all RHS, EX: [[['A', 'k', 'O']], [['a', "A''"]],
        [['B', "A'"], ['C', "A'"]],[['c']],[['b', 'B', 'C'], ['r']],[['d', "A'"], ['#']]]
        """
        for sub in diction.get(y):  # EX: diction.get(y) = [['A', 'k', 'O']], sub in first iteration is ['A', 'k', 'O']
            # find first for one element of all RHS, EX: What is the first of S ?
            res = first(sub, nonterm_userdef, term_userdef, diction, firsts)
            # if res is not empty
            if res != None:
                # if res is a list
                if type(res) is list:
                    # add all element in res to set t
                    for u in res:
                        t.add(u)
                # if res is an element add to set t directly
                else:
                    t.add(res)

        # save result in 'firsts' dictionary
        firsts[y] = t

    # return results
    return firsts

    # print("\nCalculated firsts: ")
    # key_list = list(firsts.keys())
    # index = 0
    # for gg in firsts:
    #     print(f"first({key_list[index]}) "
    #           f"=> {firsts.get(gg)}")
    #     index += 1


def computeAllFollows(start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows):
    # for all non-terminals in diction
    for NT in diction:  # diction --> ['PROGRAM', 'STMTS', 'STMT', 'EXPR', 'TERM', 'FACTOR',
        # 'EXPONENT', 'FINAL','STMTS\'','EXPR\'','TERM\'','FACTOR\'']

        # create a new set
        solset = set()
        # if NT == 'S' or NT == 'W' or NT == "S'":
        #     if NT == 'S' or NT == "S'":
        #         for i in follows[start_symbol]:
        #             solset.add(i)
        #             sol = list(solset)
        #
        #     if NT == 'W':
        #
        #         first_T_ = firsts["T'"]
        #         for i in first_T_:
        #             if i == '#':
        #                 continue
        #             solset.add(i)
        #
        #         for i in follows['T']:
        #             solset.add(i)
        #             sol = list(solset)
        if NT == 'S' or NT == 'W' or NT == "L":
            if NT == 'S' or NT == "L":
                for i in follows[start_symbol]:
                    solset.add(i)
                    sol = list(solset)

            if NT == 'W' or NT == 'O':

                first_T_ = firsts['N']
                for i in first_T_:
                    if i == '#':
                        continue
                    solset.add(i)

                for i in follows['T']:
                    solset.add(i)
                    sol = list(solset)
        else:
            # calculate follow for non-terminal
            sol = follow(NT, start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows)

        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[NT] = solset

    return follows

    # print("\nCalculated follows: ")
    # key_list = list(follows.keys())
    # index = 0
    # for gg in follows:
    #     print(f"follow({key_list[index]})"
    #           f" => {follows[gg]}")
    #     index += 1


# create parse table
def createParseTable():
    import copy
    global diction, firsts, follows, term_userdef

    # print Firsts and Follow Result table
    print("\nFirsts and Follow Result table\n")

    # find space size
    mx_len_first = 0
    mx_len_fol = 0

    # for each non-terminal
    for u in diction:
        k1 = len(str(firsts[u]))  # EX: firsts[S]:  {'b', 'c', 'p', 'a'}
        k2 = len(str(follows[u]))
        if k1 > mx_len_first:
            mx_len_first = k1
        if k2 > mx_len_fol:
            mx_len_fol = k2
    #
    # first_and_follow = f"{{:<{10}}} "\
    #       f"{{:<{mx_len_first + 5}}} "\
    #       f"{{:<{mx_len_fol + 5}}}\n"\
    #       .format("Non-T", "FIRST", "FOLLOW")

    first_and_follow = f"{{:<{10}}} " \
                       f"{{:<{mx_len_first + 5}}}\n" \
        .format("Non-T", "FIRST")  # , "FOLLOW"
    # # print head of the first and follow table
    # print(f"{{:<{10}}} "
    #       f"{{:<{mx_len_first + 5}}} "
    #       f"{{:<{mx_len_fol + 5}}}"
    #       .format("Non-T", "FIRST", "FOLLOW"))

    # print first and follow table values for eah non-terminal in the grammar
    # for u in diction:
    #     print(f"{{:<{10}}} "
    #           f"{{:<{mx_len_first + 5}}} "
    #           f"{{:<{mx_len_fol + 5}}}"
    #           .format(u, str(firsts[u]), str(follows[u])))

    for u in diction:
        first_and_follow += f"{{:<{10}}} " \
                            f"{{:<{mx_len_first + 5}}}\n" \
            .format(u, str(firsts[u]))

    first_and_follow += f"\n\n{{:<{10}}} " \
                        f"{{:<{mx_len_first + 5}}}\n" \
        .format("Non-T", "Follow")

    for u in diction:
        first_and_follow += f"{{:<{10}}} " \
                            f"{{:<{mx_len_first + 5}}}\n " \
            .format(u, str(follows[u]))
    # for u in diction:
    #      first_and_follow += f"{{:<{10}}} " \
    #                     f"{{:<{mx_len_first + 5}}}\n " \
    #                      .format(u, str(firsts[u]))
    # , str(follows[u])
    print(first_and_follow)
    # create matrix of row(NT) x [col(T) + 1($)]
    # create list of non-terminals
    ntlist = list(diction.keys())

    # create list of terminals
    terminals = copy.deepcopy(term_user_def)
    terminals.append('$')

    # create the initial empty state of ,2D matrix
    mat = []
    for x in diction:
        row = []
        for y in terminals:
            row.append('')
        # of $ append one more col
        mat.append(row)

    # Classifying grammar as LL(1) or not LL(1)
    grammar_is_LL = True

    # rules implementation
    for lhs in diction:  # EX: diction--> [S, A, C, B, A'], lhs --> S

        # RHS for lhs, EX: lhs --> S, diction[S] --> [['A', 'k', 'O']]
        rhs = diction[lhs]

        # for each element in RHS --> [['A', 'k', 'O']], y --> ['A', 'k', 'O']
        for y in rhs:
            res = first(y, non_term_user_def, term_user_def, diction, firsts)  # EX: first(['A', 'k', 'O']) --> a

            # epsilon is present, take union with follow
            if '#' in res:

                if type(res) == str:

                    firstFollow = []
                    fol_op = follows[lhs]

                    if fol_op is str:
                        firstFollow.append(fol_op)
                    else:
                        for u in fol_op:
                            firstFollow.append(u)
                    res = firstFollow
                    print('Res: ', res)
                else:
                    print('Here !!!')
                    res.remove('#')
                    res = list(res) + list(follows[lhs])
            # add rules to table
            ttemp = []
            if type(res) is str:
                ttemp.append(res)
                res = copy.deepcopy(ttemp)
            for c in res:
                xnt = ntlist.index(lhs)
                yt = terminals.index(c)
                if mat[xnt][yt] == '':
                    mat[xnt][yt] = mat[xnt][yt] \
                                   + f"{lhs}->{' '.join(y)}"
                else:
                    # if rule already present
                    if f"{lhs}->{y}" in mat[xnt][yt]:
                        continue
                    else:
                        grammar_is_LL = False
                        mat[xnt][yt] = mat[xnt][yt] \
                                       + f",{lhs}->{' '.join(y)}"

    # final state of parse table
    pares_table_string = []
    print("\nGenerated parsing table:\n")
    frmt = "{:>15}" * len(terminals)
    # print(frmt.format(*terminals))
    pares_table_string.append(frmt.format(*terminals))
    j = 0
    for y in mat:
        frmt1 = "{:>15}" * len(y)
        # print(f"{ntlist[j]} {frmt1.format(*y)}")
        pares_table_string.append(f"{frmt1.format(*y)}\n")
        j += 1
    # {ntlist[j]}
    return (mat, grammar_is_LL, terminals, first_and_follow, pares_table_string)


def validateStringUsingStackBuffer(parsing_table, grammarll1, table_term_list, input_string,
                                   term_userdef, start_symbol):
    print(f"\nValidate String => {input_string}\n")

    # # for more than one entries
    # # - in one cell of parsing table
    if grammarll1 == False:
        return f"\nInput String = " \
               f"\"{input_string}\"\n" \
               f"Grammar is not LL(1)"

    # implementing stack buffer
    # first put start symbol in the stack at the end append $ sign
    stack = [start_symbol, '$']
    buffer = []

    # reverse input string store in buffer
    input_string = input_string.split()
    input_string.reverse()
    buffer = ['$'] + input_string

    stack_string = "{:>20} {:>20} {:>20}\n".format("Buffer", "Stack", "Action")

    # print head of the table
    # print("{:>20} {:>20} {:>20}".
    #       format("Buffer", "Stack", "Action"))

    while True:
        # end loop if all symbols matched
        if stack == ['$'] and buffer == ['$']:
            # print("{:>20} {:>20} {:>20}"
            #       .format(' '.join(buffer),
            #               ' '.join(stack),
            #               "Valid"))

            stack_string += "{:>20} {:>20} {:>20}\n".format(' '.join(buffer), ' '.join(stack), "Valid")
            return "\nValid String!", stack_string

        elif stack[0] not in term_userdef:
            # take font of buffer (y) and tos (x)
            x = list(diction.keys()).index(stack[0])
            y = table_term_list.index(buffer[-1])
            if parsing_table[x][y] != '':
                # format table entry received
                entry = parsing_table[x][y]
                stack_string += "{:>20} {:>20} {:>25}\n". \
                    format(' '.join(buffer), \
                           ' '.join(stack), \
                           f"T[{stack[0]}][{buffer[-1]}] = {entry}")
                # print("{:>20} {:>20} {:>25}".
                #       format(' '.join(buffer),
                #              ' '.join(stack),
                #              f"T[{stack[0]}][{buffer[-1]}] = {entry}"))
                lhs_rhs = entry.split("->")
                print("lhs_rhs: ", lhs_rhs)
                lhs_rhs[1] = lhs_rhs[1].replace('#', '').strip()
                print("lhs_rhs[1]: ", lhs_rhs[1])
                entryrhs = lhs_rhs[1].split()
                print("lhs_rhs[1]: ", lhs_rhs[1].strip())
                stack = entryrhs + stack[1:]

            else:
                return f"\nInvalid String! \nNo rule at " \
                       f"Table[{stack[0]}][{buffer[-1]}].", stack_string
        else:
            # stack top is Terminal
            if stack[0] == buffer[-1]:
                # print("{:>20} {:>20} {:>20}\n"
                #       .format(' '.join(buffer),
                #               ' '.join(stack),
                #               f"Matched:{stack[0]}"))

                stack_string += "{:>20} {:>20} {:>20}\n" \
                    .format(' '.join(buffer), \
                            ' '.join(stack), \
                            f"Matched:{stack[0]}")
                buffer = buffer[:-1]
                stack = stack[1:]

            else:
                return f"\nInvalid String!\n " \
                       f"Unmatched terminal \nsymbols in the stack({stack[0]}) \n buffer({buffer[-1]})", stack_string


# DRIVER CODE - MAIN

sample_input_string = None

# sample set 1 (Result: Not LL(1))
# rules=["A -> S B | B",
#        "S -> a | B c | #",
#        "B -> b | d"]
# nonterm_userdef=['A','S','B']
# term_userdef=['a','c','b','d']
# sample_input_string="b c b"


# sample set 2 (Result: LL(1))
# rules=["S -> A | B C",
#        "A -> a | b",
#        "B -> p | #",
#        "C -> c"]
# nonterm_userdef=['A','S','B','C']
# term_userdef=['a','c','b','p']
# sample_input_string="p c"


# sample set 3 (Result: LL(1))
# rules=["S -> A B | C",
#        "A -> a | b | #",
#        "B-> p | #",
#        "C -> c"]
# nonterm_userdef=['A','S','B','C']
# term_userdef=['a','c','b','p']
# sample_input_string="a c b"

#
# # sample set 4 (Result: Not LL(1))
# rules = ["S -> A B C | C",
#          "A -> a | b B | #",
#          "B -> p | #",
#         "C -> c"]
# nonterm_userdef=['A','S','B','C']
# term_userdef=['a','c','b','p']
# sample_input_string="b p p c"

#
# sample set 5 (With left recursion)
# rules=["A -> B C c | g D B",
#        "B -> b C D E | #",
#        "C -> D a B | c a",
#        "D -> # | d D",
#        "E -> E a f | c"
#       ]
# nonterm_userdef=['A','B','C','D','E']
# term_userdef=["a","b","c","d","f","g"]
# sample_input_string="b a c a c"


# sample set 6
# rules=["E -> T E'",
#        "E' -> + T E' | #",
#        "T -> F T'",
#        "T' -> * F T' | #",
#        "F -> ( E ) | id"
# ]
# nonterm_userdef=['E','E\'','F','T','T\'']
# term_userdef=['id','+','*','(',')']
# # sample_input_string="id * * id"
# # example string 1
# sample_input_string="( id * id )"
# # example string 2
# sample_input_string="( id ) * id + id"


# # sample set 7 (left factoring & recursion present)
# rules = ["S -> A k O",
#          "A -> A d | a B | a C",
#          "C -> c",
#          "B -> b B C | r"]
#
# nonterm_userdef = ['A', 'B', 'C']
# term_userdef = ['k', 'O', 'd', 'a', 'c', 'b', 'r']
# sample_input_string = "a r k O"


# sample set 8 (Multiple char symbols T & NT)
# rules = ["S -> NP VP",
#          "NP -> P | PN | D N",
#          "VP -> V NP",
#          "N -> championship | ball | toss",
#          "V -> is | want | won | played",
#          "P -> me | I | you",
#          "PN -> India | Australia | Steve | John",
#          "D -> the | a | an"]
# #
# nonterm_userdef = ['S', 'NP', 'VP', 'N', 'V', 'P', 'PN', 'D']
# term_userdef = ["championship", "ball", "toss", "is", "want",
#                 "won", "played", "me", "I", "you", "India",
#                 "Australia","Steve", "John", "the", "a", "an"]
# sample_input_string = "India won the championship"
#

#
# sample set 9 (Multiple char symbols T & NT)

"""
P: Program
S: STMTS
M: STMT
S': STMTS’
E: EXPR
E': EXPR’
T: TERM
T': TERM’
F: FACTOR
W: POWER
W' :POWER’
"""
# rules = ["P -> S",
#          "S -> M | M ; S ",
#          "M -> id = E",
#          "E -> E + T | E - T | T",
#          "T -> T * W | T / W | W",
#          "W -> F ^ W | F ",
#          "F -> ( E ) | id | integer | @ F | ! F "]

#
# rules = ["P -> S",
#         "S -> M S'",
#         "M -> id = E",
#         "E -> T E''",
#         "T -> W T''",
#         "W -> F W'",
#         "F -> ( E ) | id | integer | @ F | ! F",
#         "S' -> # | ; S",
#         "E' -> + T | - T ",
#         "T' -> * W | / W ",
#         "W' -> ^ W | #",
#         "E'' -> E' E'' | #",
#         "T'' -> T' T'' | #"
#          ]

# rules = [
#     "P -> S",
#     "S -> M S'",
#     "S' -> # | ; S",
#     "M -> id = E",
#     "E -> T E'",
#     "E' -> + T E' | - T E' | #",
#     "T -> W T'",
#     "T' -> * W T' | / W T' | #",
#     "W -> F W'",
#     "W' -> ^ W | #",
#     "F -> ( E ) | id | integer | @ F | ! F"
# ]

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
#   P -> S
#   S -> M S'
#   M -> id = E
#   E -> T E''
#   T -> W T''
#   W -> F W'
#   F -> ( E )
#      | id
#      | integer
#      | @ F
#      | ! F
#  S' -> ϵ
#      | ; S
#  E' -> + T
#      | - T
#  T' -> * W
#      | / W
#  W' -> ^ W
#      | ϵ
# E'' -> E' E''
#      | ϵ
# T'' -> T' T''
#      | ϵ

# rules = ["P -> S",
#          "S -> M | S ; M ",
#          "M -> id = E",
#          "E -> E + T | E - T | T",
#          "T -> T * W | T / W | W",
#          "W -> W ^ F | F ",
#          "F -> ( E ) | id | integer | @ F | ! F "]

#
# rules = ["PROGRAM -> STMT",
#          "STMTS -> STMT STMTS'",
#          "STMT -> id = EXPR",
#          "EXPR -> TERM EXPR''",
#          "TERM -> POWER TERM''",
#          "POWER -> FACTOR POWER'",
#          "FACTOR -> ( EXPR ) | id | integer| ! FACTOR  | @ FACTOR",
#          "STMTS' -> ; STMT STMTS' | #",
#          "EXPR' -> + TERM | - TERM | #",
#          "TERM' -> * POWER  | / POWER | #",
#          "EXPR'' -> EXPR' EXPR'' | #",
#          "TERM'' -> TERM' TERM'' | #",
#          "POWER' -> ^ FACTOR POWER' | #"
# ]
#
# rules = [
#     "PROGRAM -> STMTS",
# "STMTS -> STMT STMTS'",
# "STMT ->  id = EXPR",
# "EXPR -> TERM EXPR'",
# "TERM -> POWER TERM'",
# "POWER -> FACTOR POWER'",
# "FACTOR -> ( E ) | id | integer | @ FACTOR | ! FACTOR",
# "STNTS' -> # | ; STMTS | #",
# "EXPR' -> + TERM EXPR' | - TERM EXPR'  | #",
# "TERM' -> * POWER TERM' | / POWER TERM' | #",
# "POWER' -> ^ POWER | # "]


# , 'EXPR\'\'' ,'TERM\'\'', "E''", "T''"
# nonterm_userdef = ['PROGRAM','STMT', 'EXPR', 'EXPR\'','TERM','TERM\'', 'POWER','POWER\'', 'FACTOR', 'STMTS', "STMTS'"]

# rules = [
#     "P -> S",
#     "S -> M S'",
#     "S' -> # | ; S",
#     "M -> id = E",
#     "E -> T E'",
#     "E' -> + T E' | - T E' | #",
#     "T -> W T'",
#     "T' -> * W T' | / W T' | #",
#     "W -> F W'",
#     "W' -> ^ W | #",
#     "F -> ( E ) | id | integer | @ F | ! F"
# ]
#
# non_term_user_def = ['P', 'S', 'M', 'E', 'T', 'F', 'W', "E'", "T'", "W'", "S'"]
#
# term_user_def = ["id", "integer", "(", ")", "*",
#                  "!", "@", "/", "^", "=", ";", "+", "-"]

sample_input_string = "id = id + id"
# diction - store rules inputted
diction = {}
# firsts - store computed firsts
firsts = {}
# follows - store computed follows
follows = {}

# computes all FIRSTs for all non-terminals
firsts = computeAllFirsts(rules, non_term_user_def, term_user_def, diction, firsts)
print(firsts)
# assuming first rule has start_symbol
start_symbol = list(diction.keys())[0]

# computes all follows for all non-terminals
follows = computeAllFollows(start_symbol, rules, non_term_user_def, term_user_def, diction, firsts, follows)

# then generate parse table, after we compute first and follow
(parsing_table, result, tabTerm, first_and_follow, pares_string) = createParseTable()
#
for i in range(len(pares_string)):
    print("[", i, "]: ", pares_string[i].strip())

# validate string input using stack-buffer concept
if sample_input_string is not None:
    validity, stack_string = validateStringUsingStackBuffer(parsing_table, result,
                                                            tabTerm, sample_input_string,
                                                            term_user_def, start_symbol)

    print(stack_string)
    print(validity)
else:
    print("\nNo input String detected")
