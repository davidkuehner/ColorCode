import ply.yacc as yacc
from .lex import tokens
from . import AST


operations = {
	'+' : lambda x,y: x+y,
	'-' : lambda x,y: x-y,
	'*' : lambda x,y: x*y,
	'/' : lambda x,y: x/y,
}

precedence = (
	( 'left' , 'CMP_OP' ),
	( 'left' , 'ADD_OP' ),
	( 'left' , 'MUL_OP' ),
	( 'right' , 'UMINUS' ),
)


def p_program_statement(p):
	"""program : func"""
	p[0] = AST.ProgramNode( p[1] )

def p_program_recursive(p):
	"""program : func program"""
	p[0] = AST.ProgramNode( [p[1]] + p[2].children )

def p_func(p):
	"""func : function IDENTIFIER '(' parameters ')' '{' code '}' """
	p[0] = AST.FunctionNode( p[2], [ p[4], p[7] ] )
	
def p_call(p):
	"""call : IDENTIFIER '(' call_parameters ')'"""
	p[0] = AST.CallNode( [ AST.TokenNode( p[1] ), p[3] ] )

def p_code_recursive(p):
	"""code : statement code"""
	p[0] = AST.CodeNode( [p[1]] + p[2].children )

def p_code_statement(p):
	"""code : statement"""
	p[0] = AST.CodeNode( p[1] )

def p_parameters_recursive(p): 
	"""parameters : IDENTIFIER ',' parameters"""
	p[0] = AST.ParametersNode( [  AST.TokenNode( p[1] ) ] + p[3].children )

def p_parameters_statement(p):
	"""parameters : IDENTIFIER"""
	p[0] = AST.ParametersNode(  AST.TokenNode( p[1] ) )

def p_parameters_nothing(p):
	"""parameters : """
	p[0] = AST.ParametersNode( None )
	
def p_call_parameters_recursive(p): 
	"""call_parameters : expression ',' call_parameters"""
	p[0] = AST.ParametersNode( [ p[1] ] + p[3].children )
	
def p_call_parameters(p):
	"""call_parameters : expression"""
	p[0] = AST.ParametersNode( p[1] )

def p_call_parameters_nothing(p):
	"""call_parameters : """
	p[0] = AST.ParametersNode( None )

def p_structure(p):
	"""structure : while expression '{' code '}' """
	p[0] = AST.WhileNode( [ p[2], p[4] ] )

def p_condition(p):
	"""condition : if expression '{' code '}' """
	p[0] = AST.IfNode( [ p[2], p[4] ] )

def p_statement(p):
	"""statement : assignation ';'
				| expression ';'
				| structure
				| condition"""
	p[0] = p[1]

def p_assignation(p):
	"""assignation : IDENTIFIER '=' expression"""
	p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_stream_out(p):
	"""assignation : IMAGE STREAM_OUT expression"""
	p[0] = AST.OutNode([AST.TokenNode(p[1]), p[3]])

def p_expression_identifier(p):
	"""expression : IDENTIFIER
				| NUMBER
				| COLOR"""
	p[0] = AST.TokenNode(p[1])
	
def p_expression_call(p):
	"""expression : call"""
	p[0] = p[1]

def p_expression_uminus(p):
	"""expression : ADD_OP expression  %prec UMINUS"""
	p[0] = AST.OpNode(p[1],[p[2]])

def p_expression_brac(p):
	"""expression : '(' expression ')'"""
	p[0] = p[2]

def p_expression_comp(p):
	"""expression : expression CMP_OP expression"""
	p[0] = AST.CompNode(p[2],[p[1],p[3]])

def p_expression_op(p):
	"""expression : expression ADD_OP expression
						| expression MUL_OP expression"""
	p[0] = AST.OpNode(p[2],[p[1],p[3]])

def p_error(p):
	"""error expression"""
	print("Syntax error in line %d" % p.lineno)
	yacc.errok()

def parse(program):
	return yacc.parse(program)

yacc.yacc( outputdir = 'generated' )

if __name__ == "__main__":
	import sys
	import os
	try:
		prog = open(sys.argv[1]).read()
	except IOError:
		print ("No file found, input is taken as program")
		prog = sys.argv[1]
	# result = yacc.parse(prog, debug=1)
	result = yacc.parse(prog, debug=1)
	print("%s \n\n %s" % (prog, result))
	graph = result.makegraphicaltree()
	name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
	graph.write_pdf(name)
	print ("wrote ast to", name)
