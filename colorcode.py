#!/usr/bin/env python3

from compiler import AST
from compiler.AST import addToClass

from color import colorConst as const
from functools import reduce

import sys
import os

operations = {
	'+' : lambda x, y: x+y,
	'-' : lambda x, y: x-y,
	'*' : lambda x, y: x*y,
	'/' : lambda x, y: x/y,
}
comparators = {
	'<' : lambda x, y: x<y,
	'>' : lambda x, y: x>y,
	'==' : lambda x, y: x==y,
	'!=' : lambda x, y: x!=y,
}

parameters = []
vars = {}
image = []
functions = {}
returns = []
	
@addToClass(AST.ProgramNode)
def execute(self):
	for c in self.children:
		functions[c.name] = c

	functions['main'].execute()
		
@addToClass(AST.FunctionNode)
def execute(self):
	for param_name in reversed(self.children[0].children):
		vars[param_name.tok] = parameters.pop()
		
	self.children[1].execute()
	
@addToClass(AST.CodeNode)
def execute(self):
	result = None
	for c in self.children:
		result = c.execute()
		
	returns.append(result)
		
@addToClass(AST.CallNode)
def execute(self):
	for param in self.children[1].children:
		parameters.append(param.execute())

	functions[self.children[0].tok].execute()
	return returns.pop()

@addToClass(AST.TokenNode)
def execute(self):
	if isinstance(self.tok, str):
		try:
			return const.c[self.tok]
		except KeyError:
			try:
				return vars[self.tok]
			except KeyError:
				print("*** Error: variable %s undefined !" % self.tok)
	return self.tok
	
@addToClass(AST.OpNode)
def execute(self):
	args = [c.execute() for c in self.children]
	if len(args) == 1:
		args.insert(0, 0)
	return reduce(operations[self.op], args)
	
@addToClass(AST.AssignNode)
def execute(self):
	vars[self.children[0].tok] = self.children[1].execute()

@addToClass(AST.OutNode)
def execute(self):
	image.append(self.children[1].execute())
	
@addToClass(AST.WhileNode)
def execute(self):
	while(self.children[0].execute()):
		self.children[1].execute()
		
@addToClass(AST.IfNode)
def execute(self):
	if(self.children[0].execute()):
		self.children[1].execute()
		
@addToClass(AST.CompNode)
def execute(self):
	args = [c.execute() for c in self.children]
	return reduce(comparators[self.op], args)
		
if __name__ == '__main__':
	from compiler import parser
	from compiler.parser import parse
	from compiler import imagewriter
	from compiler.imagewriter import writeSquareImage
	from compiler import semantic
	from compiler.semantic import verify
	import sys
	prog = open(sys.argv[1]).read()
	ast = parse(prog)
	errors = ast.verify()
	if len(errors) == 0:
		ast.execute()
		writeSquareImage(image, os.path.splitext(sys.argv[1])[0]+'.png')
	else:
		for error in errors:
			print(error)
