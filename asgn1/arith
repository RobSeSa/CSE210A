#!/usr/bin/env python3
# %% [markdown]
# # ARITH - Assignment 1
# Robert Sato
# rssato
# 1517254
# 1/13/2021
# 
# Citations:
# - https://ruslanspivak.com/lsbasi-part7/ - Found under recommended parsing references

INTEGER, PLUS, MINUS, MUL, LPAREN, RPAREN, EOF= (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', '(', ')', 'EOF'
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
        #print("tokenize()\nEquation: ", self.text)
        #print("Text has len: ", len(self.text))
        while self.pos < len(self.text):
            curr = self.text[self.pos]
            #print('curr =', curr)
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
                    #print('found next is digit:', next)
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
            else:
                print("Error found unknown symbol at '{}'".format(curr))
            
            self.pos += 1

        return textAsTokens
    
    # for the parser library
    def get_next_token(self):
        # can only be called after calling tokenize
        #print("Token list is size:", len(self.tokenList))
        if self.token_pos < len(self.tokenList):
            temp = self.tokenList[self.token_pos]
            self.token_pos += 1
            return temp
        else:
            #print("No more tokens")
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
# Parser code from https://ruslanspivak.com/lsbasi-part7/ in references;
# changed for my list implementation of tokens
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
        self.value = token.value


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

    def parse(self):
        return self.expr()

def printAST(node):
    #print("type:", type(node))
    if type(node) == BinOp:
        printAST(node.left)
        printAST(node.right)
        print(node.op)
    else:
        print(node.value)

# create an interpretor that does the computation given the AST
class Interpretor(object):
    def __init__(self, rootAST):
        self.rootAST = rootAST

    def eval(self):
        return self.visit(self.rootAST)

    def visit(self, node):
        # call operation for appropriate BinOp or just Number type
        node_type = type(node).__name__
        if node_type ==  'BinOp':
            if node.op.type == PLUS:
                return self.visit(node.left) + self.visit(node.right)
            elif node.op.type == MINUS:
                return self.visit(node.left) - self.visit(node.right)
            elif node.op.type == MUL:
                return self.visit(node.left) * self.visit(node.right)
        else:
            return node.value

# Read in the input string and compute
text = input()
lexer = Lexer(text)
parser = Parser(lexer)
node = parser.parse()
interpretor = Interpretor(node)
val = interpretor.eval()
#print("=", val)
print(val)
