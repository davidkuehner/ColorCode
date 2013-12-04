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
	"""program : statement"""
	p[0] = AST.ProgramNode( p[1] )
  
def p_program_recursive(p):
	"""program : statement program"""
	p[0] = AST.ProgramNode( [p[1]] + p[2].children )
	
def p_structure(p):
	"""structure : while expression '{' program '}' """
	p[0] = AST.WhileNode( [ p[2], p[4] ] )
	
def p_condition(p):
	"""condition : if expression '{' program '}' """
	p[0] = AST.IfNode( [ p[2], p[4] ] )

def p_statement(p):
	"""statement : assignation ';'
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
	"""expression : IDENTIFIER"""
	p[0] = AST.TokenNode(p[1])
  
def p_expression_numcolor(p):
	"""expression : NUMBER
					| COLOR"""
	p[0] = AST.TokenNode(p[1])
  
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
  
  
