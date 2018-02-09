# James Durtka
#
# Toy language "Sally"
#		sally_parser.py - Parser for "Sally" language
#

import logging

from sally_lexer import Lexer, Token, STRING, SPECIAL, WORD, EOF

#AST structure and Parser technique derived from https://ruslanspivak.com/lsbasi-part7/
class AST(object):
	def __str__(self):
		return (type(self).__name__.upper() + '_token')
	
#"ordinary" words
class Word(AST):
	def __init__(self, token, next):
		self.next = next
		self.token = token

#[] code blocks
class Block(AST):
	def __init__(self, token, body, next):
		self.token = token
		self.next = next
		self.body = body

#:; named (i.e. word definitions)		
class Named(AST):
	def __init__(self, token, body, next):
		self.token = token
		self.next = next
		self.body = body

#end of block marker for [] and :; named blocks
class EOBNode(AST):
	def __init__(self, token):
		self.token = token

#string literals
class StringNode(AST):
	def __init__(self, token, next):
		self.token = token
		self.next = next

#special end-of-file marker
class EOFNode(AST):
	def __init__(self, token):
		self.token = token
		
class Parser(object):
	def __init__(self, lexer):
		self.lexer = lexer
		self.current_token = self.lexer.getNextToken()
	
	def error(self, errspec):
		logging.error('Parser: ' + errspec)
		raise Exception('Parser: ' + errspec)
		
	#this is basically "assert token has correct type"
	def eat(self, token_type):
		if self.current_token.type == token_type:
			self.current_token = self.lexer.getNextToken()
		else:
			self.error('Expected ' + token_type + ', got ' + self.current_token.type + ' "' + self.current_token.value + '".')
		
	#syntax for "Sally" is incredibly simple: everything is either a word, a string, or a block (which contains more words and strings)
	def block(self):
		token = self.current_token
		
		#handle special cases, such as [] blocks and :; blocks
		if token.type == SPECIAL:
			if token.value == '[':
				self.eat(SPECIAL)
				return Block(token,self.block(),self.block())
			elif token.value == ']':
				self.eat(SPECIAL)
				return EOBNode(token)
			elif token.value == ':':
				self.eat(SPECIAL)
				return Named(self.current_token,self.block(),self.block())
			elif token.value == ';':
				self.eat(SPECIAL)
				return EOBNode(token)
			else:
				self.error('Invalid special character "' + token.value + '"')
				
		#string token
		elif token.type == STRING:
			self.eat(STRING)
			return StringNode(token, self.block())
			
		#ordinary word
		elif token.type == WORD:
			self.eat(WORD)
			return Word(token, self.block())
			
		#end of file
		elif token.type == EOF:
			self.eat(EOF)
			return EOFNode(token)

#generic method directly taken from https://ruslanspivak.com/lsbasi-part7/
class NodeVisitor(object):
	def visit(self, node, depth):
		method_name = 'visit_' + type(node).__name__
		visitor = getattr(self, method_name, self.generic_visit)
		return visitor(node, depth)
		
	def generic_visit(self, node, depth):
		raise Exception('No visit_{} method'.format(type(node).__name__))

		
#test class - displays AST in a human-readable form
class ParserTest(NodeVisitor):
	def __init__(self, parser):
		self.parser = parser
	
	#Word, Block, Named, StringNode, EOFNode
	def visit_Word(self, node, depth):
		for i in range(depth):
			print(' '),
		print('WORD '),
		print node.token
		self.visit(node.next,depth)
	
	def visit_Block(self, node, depth):
		for i in range(depth):
			print(' '),
		print('BLOCK '),
		print node.token
		self.visit(node.body,depth+1)
		self.visit(node.next,depth)
		
	def visit_Named(self, node, depth):
		for i in range(depth):
			print(' '),
		print('NAMED '),
		print node.token
		self.visit(node.body, depth+1)
		self.visit(node.next,depth)
	
	def visit_StringNode(self, node, depth):
		for i in range(depth):
			print(' '),
		print('STRING '),
		print node.token
		self.visit(node.next,depth)
		
	def visit_EOBNode(self, node, depth):
		for i in range(depth):
			print(' '),
		print('EOB '),
		print node.token
		
	def visit_EOFNode(self, node, depth):
		print('EOF '),
		print node.token
		
	def run(self):
		tree = self.parser.block()
		self.visit(tree, 0)
		
			
def CLI_test():

	#CLI
	done = False
	while not done:
		try:
			try:
				text = raw_input('>> ')
			except NameError:			#Python 3
				text = input('>> ')
		except EOFError:
			break
		if not text:
			continue
		
		#Interpret this line
		lexer = Lexer(text)
		parser = Parser(lexer)
		
		test = ParserTest(parser)
		test.run()
		
if __name__ == '__main__':
	CLI_test()