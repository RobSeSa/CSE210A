#!/usr/bin/env python3
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # WHILE - Assignment 2
# Robert Sato
# rssato
# 1517254
# 1/22/2021
# %% [markdown]
# To Do:
# - tokenize the input
# - convert arith code to take list of tokens as input
# - implement boolean expressions
# - read "straight line code"
#     - variables and assignment
# - implement if
# - implement while
# 
# Completed:
# - tokenize the input
# - convert arith code to take list of tokens as input
# - implement boolean expressions
import collections

# %%
INTEGER, PLUS, MINUS, MUL, LPAREN, RPAREN, LBRACE, RBRACE, ASSIGNMENT, VAR, TRUE, FALSE, SEMI_COLON, EOF= (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', '(', ')', '{', '}', 'ASSIGNMENT', 'VAR', 'TRUE', 'FALSE', ';', 'EOF'
)
IF, THEN, ELSE, WHILE, DO, SKIP, NOT, LESS_THAN, EQUALS, OR, AND = (
    'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'SKIP', 'NOT', '<', '==', 'OR', 'AND'
)

# token class for representing all the different types of symbols
class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __repr__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )


# %%
# "tokenize" the input string - convert the input text into a list of tokens
# accepts numbers, parenthesis, and arithmetic symbols
# Given: no decimal numbers and always 1 white space

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokenList = self.tokenize()
        self.token_pos = 0
    
    # return a list of tokens
    def tokenize(self):
        textAsTokens = []
        while self.pos < len(self.text):
            curr = self.text[self.pos]
            # setup conditionals for all cases
            if curr == ' ':
                self.pos += 1
                continue
            elif curr.isdigit():
                # keep adding digit chars until whitespace
                num = ''
                while curr.isdigit(): # keep appending
                    num += curr
                    self.pos += 1
                    if self.pos >= len(self.text):
                        break
                    curr = self.text[self.pos]
                self.pos -= 1
                # convert string of digits to int
                num = int(num)
                textAsTokens.append(Token(INTEGER, num))
            elif curr == '+':
                textAsTokens.append(Token(PLUS, curr))
            elif curr == '*':
                textAsTokens.append(Token(MUL, curr))
            elif curr == '-':
                # add functionality for negative numbers
                # if next char is a digit, do digit stuff and add as INTEGER
                next = self.text[self.pos+1]
                if next.isdigit():
                    # do digit stuff
                    self.pos += 1
                    curr = self.text[self.pos]
                    num = '-'
                    while curr.isdigit(): # keep appending
                        num += curr
                        self.pos += 1
                        if self.pos >= len(self.text):
                            break
                        curr = self.text[self.pos]
                    self.pos -= 1
                    # convert string of digits to int
                    num = int(num)
                    textAsTokens.append(Token(INTEGER, num))

                # elif a space, add as MINUS
                else:
                #elif next == ' ':
                    textAsTokens.append(Token(MINUS, curr))
                # elif a LPAREN -> ur screwed so ignore for now
            elif curr == '(':
                textAsTokens.append(Token(LPAREN, curr))
            elif curr == ')':
                textAsTokens.append(Token(RPAREN, curr))
            elif curr == '{':
                textAsTokens.append(Token(LBRACE, curr))
            elif curr == '}':
                textAsTokens.append(Token(RBRACE, curr))
            elif curr == '¬':
                textAsTokens.append(Token(NOT, curr))
            elif curr == '<':
                textAsTokens.append(Token(LESS_THAN, curr))
            elif curr == '=':
                textAsTokens.append(Token(EQUALS, curr))
            elif curr == '∨':
                textAsTokens.append(Token(OR, curr))
            elif curr == '∧':
                textAsTokens.append(Token(AND, curr))
            elif curr == ';':
                textAsTokens.append(Token(SEMI_COLON, curr))
            # assignment ':='
            elif curr == ':':
                next = self.text[self.pos+1]
                if next == '=':
                    textAsTokens.append(Token(ASSIGNMENT, ':='))
                    self.pos += 1
                else:
                    print("Error: no = following : in expected :=")
            
            # keywords
            # if
            elif curr == 'i' and (self.pos < len(self.text) - 1 and self.text[self.pos+1] == 'f'):
                # skip one and add if token
                self.pos += 1
                textAsTokens.append(Token(IF, 'if'))
            # then
            elif curr == 't' and (self.pos < len(self.text) - 3 and self.text[self.pos+1:self.pos+4] == 'hen'):
                self.pos += 3
                textAsTokens.append(Token(THEN, 'then'))

            # else
            elif curr == 'e' and (self.pos < len(self.text) - 3 and self.text[self.pos+1:self.pos+4] == 'lse'):
                self.pos += 3
                textAsTokens.append(Token(ELSE, 'else'))

            # while
            elif curr == 'w' and (self.pos < len(self.text) - 4 and self.text[self.pos+1:self.pos+5] == 'hile'):
                self.pos += 4
                textAsTokens.append(Token(WHILE, 'while'))

            # do
            elif curr == 'd' and (self.pos < len(self.text) - 1 and self.text[self.pos+1] == 'o'):
                self.pos += 1
                textAsTokens.append(Token(DO, 'do'))

            # skip
            elif curr == 's' and (self.pos < len(self.text) - 3 and self.text[self.pos+1:self.pos+4] == 'kip'):
                self.pos += 3
                textAsTokens.append(Token(SKIP, 'skip'))
            
            # true
            elif curr == 't' and (self.pos < len(self.text) - 3 and self.text[self.pos+1:self.pos+4] == 'rue'):
                self.pos += 3
                textAsTokens.append(Token(TRUE, 'true'))
            
            # false
            elif curr == 'f' and (self.pos < len(self.text) - 4 and self.text[self.pos+1:self.pos+5] == 'alse'):
                self.pos += 4
                textAsTokens.append(Token(FALSE, 'false'))

            # variable - check this after checking if 'true' 'false' 'if' etc.
            elif curr.isalpha():
                # all following characters except whitespace counts as the variable name
                var = ''
                while curr != ' ': # keep appending
                    var += curr
                    self.pos += 1
                    if self.pos >= len(self.text):
                        break
                    curr = self.text[self.pos]
                self.pos -= 1
                # convert string of digits to int
                textAsTokens.append(Token(VAR, var))

            else:
                print("Error found unknown symbol at '{}'".format(curr))
            
            self.pos += 1

        return textAsTokens
    
    # for the parser library
    def get_next_token(self):
        # can only be called after calling tokenize
        if self.token_pos < len(self.tokenList):
            temp = self.tokenList[self.token_pos]
            self.token_pos += 1
            return temp
        else:
            return Token(EOF, None)

    def print(self):
        print("Text has len: ", len(self.text))
        while self.pos < len(self.text):
            print("{}:{}".format(self.pos, self.text[self.pos]))
            self.pos += 1

    def getNextChar(self):
        self.pos += 1
        return self.text[self.pos-1]



# %%
# create an AST from the tokens
class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = int(token.value)
    def __repr__(self):
        return 'Num({value})'.format(
            value=repr(self.value)
        )

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
    def __repr__(self):
        return 'Var({value})'.format(
            value=repr(self.value)
        )


# %%
'''
EBNF Grammer from for boolean expressions: https://unnikked.ga/how-to-build-a-boolean-expression-evaluator-518e9e068a65
<expression>::=<term>{<or><term>}
<term>::=<factor>{<and><factor>}
<factor>::=<constant>|<not><factor>|(<expression>)
<constant>::= false|true
<or>::='|'
<and>::='&'
<not>::='!'
'''


# %%
# node types for boolean expressions
class BoolOp(AST):
    # handles cases for multiple boolean expressions
    def __init__(self, left, op, right):
        self.left = left
        # if expr comparison, the operation will be = or <
        # else it will be AND or OR
        self.token = self.op = op
        self.right = right

class BoolLeaf(AST):
    # handles single bool expr cases
    def __init__(self, token):
        self.token = token
        self.value = token.value
    def __repr__(self):
        return 'BoolLeaf({value})'.format(
            value=repr(self.value)
        )

class Not(AST):
    def __init__(self, child):
        self.child = child
    def __repr__(self):
        return 'Not({child})'.format(
            child=self.child
        )


# %%
# node types for commands
class VarAssign(AST):
    # handles cases for multiple boolean expressions
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return 'Assign {name} := {value}'.format(
            name = self.name,
            value = self.value
        )

class If(AST):
    # handles single bool expr cases
    def __init__(self, cond, true_branch, false_branch):
        self.cond = cond
        self.true_branch = true_branch
        self.false_branch = false_branch
    def __repr__(self):
        return 'If({cond}) then {t} else {f}'.format(
            cond=repr(self.cond),
            t = repr(self.true_branch),
            f = repr(self.false_branch)
        )

class While(AST):
    def __init__(self, cond, true_branch):
        self.cond = cond,
        self.true_branch = true_branch
    def __repr__(self):
        return 'While({cond}) do {t}'.format(
            cond=self.cond,
            t=self.true_branch
        )

class Skip(AST):
    def __init__(self, token):
        self.token = token
    def __repr__(self):
        return 'Skip({token})'.format(
            token=self.token
        )

class SEMI_COL(AST):
    def __init__(self, token, left, right):
        self.token = token
        self.left = left
        self.right = right
    def __repr__(self):
        return 'SEMI_COLON({token}, Left, Right)'.format(token=self.token)


# %%
# Parser code from https://ruslanspivak.com/lsbasi-part7/ in references;
# changed for my list implementation of tokens
class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == VAR:
            self.eat(VAR)
            return Var(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self):
        """term : factor ((MUL) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node


    # define a boolean expression type
    def b_expr(self):
        """
        <expression>::=<term>{<or><term>}
        """
        # first token in set (true, false, expr, not, b_expr)
        node = self.b_term()
        #print('self.current_token after b_expr call to b_term():', self.current_token)
        while self.current_token.type == OR:
            token = self.current_token
            self.eat(OR)
            node = BoolOp(left=node, op=token, right=self.b_term())
        return node

    def b_term(self):
        """
        <term>::=<factor>{<and><factor>}
        """
        node = self.b_factor()
        while self.current_token.type == AND:
            token = self.current_token
            self.eat(AND)
            node = BoolOp(left=node, op=token, right=self.b_factor())
        return node
    
    def b_factor(self):
        """
        <factor>::=<constant>|<not><factor>|(<expression>)
        <constant>::= false|true
        """
        token = self.current_token
        if token.type == TRUE:
            self.eat(TRUE)
            return BoolLeaf(token)
        elif token.type == FALSE:
            self.eat(FALSE)
            return BoolLeaf(token)
        elif token.type == NOT:
            self.eat(NOT)
            node = self.b_factor()
            node = Not(child=node)
            return node
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.b_expr()
            self.eat(RPAREN)
            return node
        else: # comparisons
            #print("Error handling b_factor()")
            node = self.expr()
            token = self.current_token
            self.eat(token.type)
            #print("Comparison token is:", token)
            node = BoolOp(left=node, op=token, right=self.expr())
            return node

    # for commands
    # tree implementation
    # returns 1 command as its given object types
    def get_command(self):
        if self.current_token.type != EOF:
            token = self.current_token
            type = token.type
            self.eat(type)
            if type == SKIP:
                return Skip(token)
            elif type == VAR:
                # syntax: VAR ASSIGNMENT EXPR
                name = token.value
                self.eat(ASSIGNMENT)
                expr = self.expr()
                # don't need to eat bc self.expr() eats
                return VarAssign(name, expr)
            elif type == SEMI_COLON:
                # skip: command interpreter executes sequentially down list
                pass
            elif type == IF:
                # syntax: IF b_expr THEN c_expr ELSE c_expr
                cond = self.b_expr()
                self.eat(THEN)
                true_branch = self.c_expr()
                self.eat(ELSE)
                false_branch = self.c_expr()
                return If(cond=cond, true_branch=true_branch, false_branch=false_branch)
            elif type == WHILE:
                # syntax: WHILE b_expr DO c_expr
                cond = self.b_expr()
                self.eat(DO)
                true_branch = self.c_expr()
                return While(cond=cond, true_branch=true_branch)
            # add condition for {}
            elif type == LBRACE:
                # syntax: { c_expr }
                node = self.c_expr()
                self.eat(RBRACE)
                return node
            else:
                print("***Error: Unexpected token in c_expr()\n")

    def c_expr(self):
        node = self.get_command()
        while self.current_token.type == SEMI_COLON:
            # more commands to process
            self.eat(SEMI_COLON)
            node = SEMI_COL(SEMI_COLON, left=node, right=self.get_command())
        return node

    def parse(self):
        return self.c_expr()


# %%
def test_AST(node):
    # very similar to our interpreter except print out the contents of the tree
    node_type = type(node).__name__
    # Arithmetic Expressions
    if node_type ==  'BinOp':
        print("BinOp")
        test_AST(node.left)
        test_AST(node.right)
    elif node_type == 'Num':
        print(node)
    elif node_type == 'Var':
        # not done yet
        print(node)
    
    # Boolean Expressions
    elif node_type == 'BoolOp':
        print(node)
        test_AST(node.left)
        test_AST(node.right)
    elif node_type == 'BoolLeaf':
        print(node)
    elif node_type == 'Not':
        print(node)
        test_AST(node.child)
    
    # Command Expressions
    elif node_type == 'VarAssign':
        print(node)
    elif node_type == 'If':
        print(node)
        test_AST(node.cond)
        test_AST(node.true_branch)
        test_AST(node.false_branch)
    elif node_type == 'While':
        print(node)
        test_AST(node.cond)
        test_AST(node.true_branch)
    elif node_type == 'Skip':
        print(node)
    elif node_type == 'SEMI_COL':
        print(node)
        test_AST(node.left)
        test_AST(node.right)
    else:
        print('{} node type not found !!!'.format(node_type))


# %%
def printAST(node):
    print("printAST() type:", type(node))
    if type(node) == BinOp:
        printAST(node.left)
        print(node.op)
        printAST(node.right)
    elif type(node) == BoolOp:
        printAST(node.left)
        print(node.op)
        printAST(node.right)
    elif type(node) == BoolLeaf:
        print(node)
    elif type(node) == Not:
        printAST(node.child)
    else:
        print(node)
# %%
# create an interpretor that does the computation given the AST
class Interpretor(object):
    def __init__(self, rootAST):
        self.rootAST = rootAST
        self.variables = {}

    def interpret(self):
        self.visit(self.rootAST)

    def visit(self, node):
        # very similar to our interpreter except print out the contents of the tree
        node_type = type(node).__name__
        # Arithmetic Expressions
        if node_type ==  'BinOp':
            if node.op.type == PLUS:
                return self.visit(node.left) + self.visit(node.right)
            elif node.op.type == MINUS:
                return self.visit(node.left) - self.visit(node.right)
            elif node.op.type == MUL:
                return self.visit(node.left) * self.visit(node.right)
        elif node_type == 'Num':
            return node.value
        elif node_type == 'Var':
            # look up the variable in the dictionary
            val = self.variables.get(node.value, 0)
            while type(val).__name__ == 'VAR':
                val = self.variables.get(val.value, 0)
            return val
        
        # Boolean Expressions
        elif node_type == 'BoolOp':
            if node.op.type == LESS_THAN:
                return self.visit(node.left) < self.visit(node.right)
            elif node.op.type == EQUALS:
                return self.visit(node.left) == self.visit(node.right)
            elif node.op.type == AND:
                return self.visit(node.left) and self.visit(node.right)
            elif node.op.type == OR:
                return self.visit(node.left) or self.visit(node.right)
            else:
                print("Error: Unknown op.type = {} in BoolOp", node.op.type)
        elif node_type == 'BoolLeaf':
            if node.value == 'true':
                return True
            elif node.value == 'false':
                return False
            else:
                print("Error: Unknown node.value in BoolLeaf")
        elif node_type == 'Not':
            return not self.visit(node.child)
        
        # Command Expressions
        elif node_type == 'VarAssign':
            # add the variable name to dictionary
            # note: must unroll the variable until we get a Num
            """var_name = node.name
            var_value  = node.value
            while type(var_value).__name__ == 'Var':
                # the value is also a var so unroll it
                var_value = self.variables[node.value.value]
            self.variables[var_name] = var_value"""
            var_name = node.name
            var_value  = node.value
            self.variables[var_name] = self.visit(var_value)

        elif node_type == 'If':
            if self.visit(node.cond):
                self.visit(node.true_branch)
            else:
                self.visit(node.false_branch)
        elif node_type == 'While':
            while self.visit(node.cond):
                self.visit(node.true_branch)
        elif node_type == 'Skip':
            pass
        elif node_type == 'SEMI_COL':
            self.visit(node.left)
            self.visit(node.right)
        elif node_type == 'tuple':
            return self.visit(node[0])
        else:
            print('{} node type not found in interpreter!!!'.format(node_type))

text = input()
lexer = Lexer(text)
parser = Parser(lexer)
node = parser.parse()
interpreter = Interpretor(node)
interpreter.interpret()
count = 0
print("{", end='')
collection = collections.OrderedDict(sorted(interpreter.variables.items()))
for key in collection:
    if count > 0:
        print(', {key} → {value}'.format(key = key, value = collection[key]), end='')
    else:
        print('{key} → {value}'.format(key = key, value = collection[key]), end='')
    count += 1
print("}")
