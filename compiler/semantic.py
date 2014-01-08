#!/usr/bin/env python3

from . import AST
from .AST import addToClass

import color
from color import colorConst as const

functions = {}
errors = []
varsInScope = []
	
@addToClass(AST.ProgramNode)
def verify(self):
	for c in self.children:
		functions[c.name] = c

	if "main" not in functions.keys():
		errors.append("No main function")
		
	for c in self.children:
		c.verify()
		
	return errors
		
@addToClass(AST.FunctionNode)
def verify(self):
	del varsInScope[:]
	for varname in self.children[0].children:
		varsInScope.append(varname.tok)
		
	self.children[1].verify()
	
@addToClass(AST.CodeNode)
def verify(self):
	for c in self.children:
		c.verify()
		
@addToClass(AST.CallNode)
def verify(self):
	params = self.children[1].children
	name = self.children[0].tok
	
	if name not in functions.keys():
		errors.append("Undefined function: %s" % name)
	else:
		if(len(params) != len(functions[self.children[0].tok].children[0].children)):
			errors.append("Wrong number of parameters passed to function: %s" % name)
			
		for c in self.children[1].children:
			c.verify()

@addToClass(AST.TokenNode)
def verify(self):
	if isinstance(self.tok, str):
		try:
			return const.c[self.tok]
		except KeyError:
			if self.tok not in varsInScope:
				errors.append("Variable %s undefined or not in scope" % self.tok)
	return self.tok
	
@addToClass(AST.OpNode)
def verify(self):
	for c in self.children:
		c.verify()
	
@addToClass(AST.AssignNode)
def verify(self):
	varsInScope.append(self.children[0].tok)
	self.children[1].verify()

@addToClass(AST.OutNode)
def verify(self):
	self.children[1].verify()
	
@addToClass(AST.WhileNode)
def verify(self):
	self.children[0].verify()
	self.children[1].verify()
		
@addToClass(AST.IfNode)
def verify(self):
	self.children[0].verify()
	self.children[1].verify()
		
@addToClass(AST.CompNode)
def verify(self):
	for c in self.children:
		c.verify()
		
if __name__ == '__main__':
	from compiler import parser
	from compiler.parser import parse
	import sys
	
	prog = open(sys.argv[1]).read()
	ast = parse(prog)
	ast.verify()
	if len(errors) == 0:
		print("Code is semantically valid")
	for error in errors:
		print(error)
	
