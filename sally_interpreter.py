# James Durtka
#
# Toy language "Sally"
#		sally_interpreter.py - Interpreter for "Sally" language
#

import sys
import logging

from sally_parser import Parser, NodeVisitor
from sally_lexer import Lexer, STRING, SPECIAL, WORD, EOF
from sally_stack import Stack
from sally_base import BasePackage

class Interpreter(NodeVisitor):
	def __init__(self, parser, dataStack, basePackage, globalDictionary, rStack):
		self.parser = parser
		self.dataStack = dataStack
		self.basePackage = basePackage
		self.globalDictionary = globalDictionary
		self.rStack = rStack
	
	def visit_Word(self, node, depth):
		word = node.token.value.lower()
		try:
			#is it in the global dictionary?
			wordDef = self.globalDictionary[word]
		except KeyError:
			#no
			wordDef = None
		if not wordDef:
			#search through the base package
			self.basePackage.doWord(word, self, self.dataStack, self.globalDictionary, self.rStack)
			
		#otherwise, recursively create an interpreter to run the word definition
		else:
			if len(wordDef) >= 1:
				self.visit(wordDef[-1].next,depth)
		
		#next...
		self.visit(node.next,depth)
	
	#BLOCK in stream = push entire block to stack
	def visit_Block(self, node, depth):
		self.dataStack.push(node)
		self.visit(node.next,depth)
		
	#NAMED in stream = add to dictionary
	def visit_Named(self, node, depth):
		name = node.token.value
		body = node.body
		try:
			self.globalDictionary[name].append(body)
		except KeyError:
			logging.debug("WORD DEFINED: '" + name + "'")
			self.globalDictionary[name] = []
			self.globalDictionary[name].append(body)
		self.visit(node.next,depth)
	
	#STRING in stream = push string to stack
	def visit_StringNode(self, node, depth):
		value = node.token.value
		self.dataStack.push(value)
		self.visit(node.next,depth)	
		
	#EOB simply signifies the end of a BLOCK or NAMED
	def visit_EOBNode(self, node, depth):
		pass
		
	#EOF signifies the end of the file
	def visit_EOFNode(self, node, depth):
		pass
		
	def run(self):
		tree = self.parser.block()
		self.visit(tree, 0)

#run a file in the global environment
def run_file(name, dataStack, basePackage, globalDictionary, rStack):
	try:
		with open(name,'rb') as f:
			text = f.read()
			lexer = Lexer(text)
			parser = Parser(lexer)
			interpreter = Interpreter(parser, dataStack, basePackage, globalDictionary, rStack)
			interpreter.run()
	except Exception, e:
		logging.error(e, exc_info=True)
		logging.error("INTERPRETER:run_file failed")
		
def main():

	#see if anything came in on the command prompt
	loadfile = ''
	if (len(sys.argv)) > 1:
		loadfile = sys.argv[1]

	#setup logging
	logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='sally.log',
                    filemode='w')
	consoleLogFormatter = logging.Formatter("[%(levelname)-5.5s]  %(message)s")
	rootLogger = logging.getLogger()
	
	consoleHandler = logging.StreamHandler()
	consoleHandler.setLevel(logging.INFO)
	consoleHandler.setFormatter(consoleLogFormatter)
	
	rootLogger.addHandler(consoleHandler)
	
	if loadfile == '':
		logging.info('INTERACTIVE MODE')
	
	
	#setup the global environment
	dataStack = Stack()
	rStack = Stack()
	basePackage = BasePackage()
	globalDictionary = {}

	#run base.sal to load default dictionary words
	logging.info("Attempting to run base.sal")
	run_file('base.sal', dataStack, basePackage, globalDictionary, rStack)
	
	while True:
		#not interpreting a file, enter interactive mode
		if loadfile == '':
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
		
				logging.debug("Command entry: " + text)
				#Interpret this line
				lexer = Lexer(text)
				parser = Parser(lexer)
				interpreter = Interpreter(parser, dataStack, basePackage, globalDictionary, rStack)
				interpreter.run()
				print('')
		else:
			logging.info("Attempting to run " + loadfile)
			#run the file specified, then exit to interactive mode
			run_file(loadfile, dataStack, basePackage, globalDictionary, rStack)
			loadfile = ''
		
if __name__ == '__main__':
	main()