#!/usr/bin/env python3

import AST
from AST import addToClass
from functools import reduce
import color
from color import colorConst as const
from color.color import Color
import sys
import imagewriter
from imagewriter import writeSquareImage
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

vars = {}
image = []
	
@addToClass(AST.ProgramNode)
def execute(self):
	for c in self.children:
		c.execute()
		
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
	
@addToClass(AST.PrintNode)
def execute(self):
	print(self.children[0].execute())
	
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
	from parser import parse
	import sys
	prog = open(sys.argv[1]).read()
	ast = parse(prog)
	ast.execute()
	writeSquareImage(image, os.path.splitext(sys.argv[1])[0]+'.png')
