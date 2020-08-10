"""
Code parser
"""

from ply import lex
from ply import yacc
from interpreter import Interpreter
import sys

interpreter = Interpreter()

parsed_file = open(sys.argv[1], 'r')
code = parsed_file.read()
parsed_file.close()

tokens = [
	'INT',
	'ASSIGNMENT',
	'ARGSEP',
	'CMD_END',
	'LEX',
	'LPAREN',
	'RPAREN'
]

t_CMD_END = r';'
t_ASSIGNMENT = r'\='
t_ARGSEP = r'\,'
t_RPAREN = r'\)'
t_LPAREN = r'\('

t_ignore = ' \r\t\f\v\n'

def t_LEX(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'

	return t

def t_INT(t):
	r'-?\d+'

	return t

def t_error(t):
	t.lexer.skip(1)

lexer = lex.lex()

def p_program(p):
	'''
	program : cmd
		| program cmd
	'''
	p[0] = p[1:]

def p_cmd(p):
	'''
	cmd : func_chain CMD_END
		| assignment CMD_END
	'''
	p[0] = p[1:-1][0]
	p[0] = p[0] if type(p[0]) is list else [p[0]]

	# add command to command stack for further interpretation
	interpreter.push(p[0])

def p_args(p):
	'''
	args : args ARGSEP arg
		| arg ARGSEP arg
		| arg
	'''

	if type(p[1]) is list:
		p[0] = p[1] + [p[3]] 
	else:
		p[0] = [number for number in p[1:] if number != ',']

def p_arg(p):
	'''
	arg : INT
		| LEX
	'''

	p[0] = p[1]

def p_arg_assign(p):
	'''
	arg_assign : LEX ASSIGNMENT LEX
		| LEX ASSIGNMENT INT
	'''

	p[0] = ('ASSIGN', (p[1], p[3]))

def p_func(p):
	'''
	func : LEX LPAREN args RPAREN
		| LEX LPAREN arg_assign RPAREN 
	'''

	p[0] = ('CALL', (p[1], p[3]))

def p_assignment(p):
	'''
	assignment : LEX ASSIGNMENT INT
		| LEX ASSIGNMENT LEX
	'''

	p[0] = ('ASSIGN', (p[1], p[3]))


def p_func_chain(p):
	'''
	func_chain : func_chain func
		| func
	'''
	if type(p[1]) is list:
		
		p[0] = p[1] + [p[2]] 
	else:
		p[0] = p[1:]

def p_error(p):
	if p:
		print("Parsing error:", p.value)
		exit()

parser = yacc.yacc()
parser.parse(code)

interpreter.run()
