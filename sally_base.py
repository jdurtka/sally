# James Durtka
#
# Toy language "Sally"
#		sally_base.py - Base package for "Sally" language
#						Note that some of the "base package" functions are implemented in base.sal
#
import sys
import logging

from sally_lexer import Lexer, Token, EOF,SPECIAL
from sally_parser import Parser, Block

#################################################################
#
# Handles system functions which cannot (or cannot easily) be implemented directly in Forth
#
#################################################################
class BasePackage(object):
	def __init__(self):
		pass
	def error(self, errspec):
		logging.error('BasePackage: ' + errspec)
		raise Exception('BasePackage: ' + errspec)
	
	#End of the line: if a lexeme could not evaluate any other way, our last resort is to attempt
	#to treat it as an integer. If this fails, we inform the user and pass the error up
	def toInteger(self, word):
		value = int(word)
		return value
		
	#Do-everything method: implements the functions which cannot, or cannot easily, be done directly in Forth
	def doWord(self, word, interpreter, dataStack, globalDictionary, rStack):
		#################################################################
		#
		# Stack operations
		#
		#################################################################
		if word == 'dup':
			if dataStack.size() >= 1:
				dataStack.push(dataStack.peek())
		elif word == '?dup':
			n = dataStack.peek()
			if (not n == None) and not (n == 0):
				dataStack.push(n)
		elif word == '2dup':
			if dataStack.size() >= 2:
				b = dataStack.pop()
				a = dataStack.pop()
				dataStack.push(a)
				dataStack.push(b)
				dataStack.push(a)
				dataStack.push(b)
			else:
				logging.warning('Attempted to ' + word + ' from beyond the end of the stack [' + str(2) + '/' + str(dataStack.size()) + ']')
		elif word == 'drop':
			_ = dataStack.pop()
		elif word == '2drop':
			_ = dataStack.pop()
			_ = dataStack.pop()
		elif word == 'over':
			if dataStack.size() >= 2:
				b = dataStack.pop()
				a = dataStack.pop()
				dataStack.push(a)
				dataStack.push(b)
				dataStack.push(a)
			else:
				logging.warning('Attempted to ' + word + ' from beyond the end of the stack [' + str(2) + '/' + str(dataStack.size()) + ']')
		elif word == 'swap':
			if dataStack.size() >= 2:
				b = dataStack.pop()
				a = dataStack.pop()
				dataStack.push(b)
				dataStack.push(a)
			else:
				logging.warning('Attempted to ' + word + ' from beyond the end of the stack [' + str(2) + '/' + str(dataStack.size()) + ']')
			
		elif word == '2swap':
			if dataStack.size() >= 4:
				b2 = dataStack.pop()
				b1 = dataStack.pop()
				a2 = dataStack.pop()
				a1 = dataStack.pop()
				dataStack.push(b1)
				dataStack.push(b2)
				dataStack.push(a1)
				dataStack.push(a2)
			else:
				logging.warning('Attempted to ' + word + ' from beyond the end of the stack [' + str(2) + '/' + str(dataStack.size()) + ']')
			
		elif word == 'pick':
			n = dataStack.pop()+1
			m = dataStack.peekAt(n)
			if m is not None:
				dataStack.push(m)
				
		elif word == 'roll':
			n = dataStack.pop()+1
			m = dataStack.pullFrom(n)
			if m is not None:
				dataStack.push(m)
			
		elif word == 'empty?':
			if dataStack.isEmpty():
				dataStack.push(-1)
			else:
				dataStack.push(0)
		elif word == 'last?':
			if dataStack.size() <= 1:
				dataStack.push(-1)
			else:
				dataStack.push(0)
		elif word == 'empty!':
			dataStack.clear()
			
		#legacy support for "return stack"
		elif word == '>r':
			if ((rStack is not None) and (not dataStack.isEmpty())):
				n = dataStack.pop()
				rStack.push(n)
		elif word == 'r>':
			if ((rStack is not None) and (not rStack.isEmpty())):
				n = rStack.pop()
				dataStack.push(n)
		elif word == 'r@':
			if ((rStack is not None) and (not rStack.isEmpty())):
				dataStack.push(rStack.peek())
		elif word == 'r-empty!':
			rStack.clear()
		elif word == 'r-empty?':
			if rStack.isEmpty():
				dataStack.push(-1)
			else:
				dataStack.push(0)
		
		#################################################################
		#
		# Debugging functions
		#
		#################################################################
		elif word == '.s':
			print(str(dataStack))
			logging.debug('Stack dump')
			logging.debug(str(dataStack))
		elif word == '.r':
			print(str(rStack))
			logging.debug('rStack dump')
			logging.debug(str(dataStack))
		elif word == '.dict':
			logstr = '\n'
			if globalDictionary:
				for (key, value) in globalDictionary.items():
					logstr = logstr + ' ' + str(key) + ': '
					if value == None:
						logstr = logstr + 'None'
					elif value == []:
						logstr = logstr + '[]'
					else:
						logstr = logstr + '[ '
						for item in value:
							logstr = logstr + str(item)
							logstr = logstr + ','
						logstr = logstr + ']\n'
			else:
				logstr = logstr + "{ }"
			print logstr
			logging.debug('Dictionary dump')
			logging.debug(logstr)
		#################################################################
		#
		# Integer arithmetic
		#
		#################################################################
		elif word == '+':
			b = dataStack.pop()
			a = dataStack.pop()
			if not (a == None):
				dataStack.push(a+b)
			else:
				dataStack.push(b)
		elif word == '-':
			b = dataStack.pop()
			a = dataStack.pop()
			dataStack.push(a-b)
		elif word == '*':
			b = dataStack.pop()
			a = dataStack.pop()
			dataStack.push(a*b)
		elif word == '/':
			b = dataStack.pop()
			a = dataStack.pop()
			try:
				dataStack.push(a / b)
			except ZeroDivisionError:
				logging.warning('Divide-by-zero')
				dataStack.push(0)
		elif word == 'mod':
			b = dataStack.pop()
			a = dataStack.pop()
			try:
				dataStack.push(a % b)
			except ZeroDivisionError:
				logging.warning('Divide-by-zero')
				dataStack.push(0)
				
		#################################################################
		#
		# Integer comparisons
		#
		#################################################################
		elif word == '=':
			b = dataStack.pop()
			a = dataStack.pop()
			if a == b:
				dataStack.push(-1)
			else:
				dataStack.push(0)
		elif word == '>':
			b = dataStack.pop()
			a = dataStack.pop()
			if a > b:
				dataStack.push(-1)
			else:
				dataStack.push(0)
		elif word == '<':
			b = dataStack.pop()
			a = dataStack.pop()
			if a < b:
				dataStack.push(-1)
			else:
				dataStack.push(0)
		elif word == '<=':
			b = dataStack.pop()
			a = dataStack.pop()
			if a <= b:
				dataStack.push(-1)
			else:
				dataStack.push(0)
		elif word == '>=':
			b = dataStack.pop()
			a = dataStack.pop()
			if a >= b:
				dataStack.push(-1)
			else:
				dataStack.push(0)
				
				
		#################################################################
		#
		# Boolean operators
		#
		#################################################################
		
		#Logical
		elif word == 'or':
			b = dataStack.pop()
			a = dataStack.pop()
			if (not a == 0) or (not b == 0):
				dataStack.push(-1)
			else:
				dataStack.push(0)
		
		elif word == 'and':
			b = dataStack.pop()
			a = dataStack.pop()
			if (not a == 0) and (not b == 0):
				dataStack.push(-1)
			else:
				dataStack.push(0)
				
		elif word == 'xor':
			b = dataStack.pop()
			a = dataStack.pop()
			if (a == 0) != (b == 0):
				dataStack.push(-1)
			else:
				dataStack.push(0)
				
		elif word == '||':
			if dataStack.size() >= 2:
				b = dataStack.pop()
				a = dataStack.pop()
				try:
					dataStack.push(a | b)
				except:
					logging.warning('Improper datatypes for bitwise OR')
		elif word == '^^':
			if dataStack.size() >= 2:
				b = dataStack.pop()
				a = dataStack.pop()
				try:
					dataStack.push(a ^ b)
				except:
					logging.warning('Improper datatypes for bitwise XOR')
		elif word == '&&':
			if dataStack.size() >= 2:
				b = dataStack.pop()
				a = dataStack.pop()
				try:
					dataStack.push(a & b)
				except:
					logging.warning('Improper datatypes for bitwise AND')
		
		elif word == '~':
			if dataStack.size() >= 1:
				b = dataStack.pop()
				try:
					dataStack.push(~b)
				except:
					logging.warning('Improper datatype for bitwise NOT')
		#################################################################
		#
		# Block combinators
		#
		#################################################################
		elif word == 'eval':
			try:
				quote = dataStack.pop()
				lexer = Lexer(quote)
				parser = Parser(lexer)
				node = Block(Token(SPECIAL,'['), parser.block(), Token(EOF,']'))
				dataStack.push(node)
			except Exception as e:
				logging.error('Failed evaluation')
				logging.error(e)
			
		elif word == 'forget':
			quote = str(dataStack.pop())
			try:
				if globalDictionary[quote] is not None:
					globalDictionary[quote].pop()
			except KeyError:
				logging.error("Tried to forget '" + quote + "'; word not found")
			
		elif word == ',exec':
			block = dataStack.pop()
			if block is not None:
				try:
					interpreter.visit(block.body,0)
				except Exception as e:
					logging.error('Improper argument for ' + word)
					logging.error(e)
					
			dataStack.push(block)
		
		elif word == 'times':
			n = dataStack.pop()
			loopblock = dataStack.pop()
			if (n is not None) and (loopblock is not None):
				try:
					if n > 0:
						for i in range(n):
							interpreter.visit(loopblock.body,0)
				except Exception as e:
					logging.error('Improper arguments for ' + word)
					logging.error(e)
		
		elif word == 'forloop':
			loopblock = dataStack.pop()
			n = dataStack.pop()
			if (n is not None) and (loopblock is not None):
				for i in range(n):
					try:
						dataStack.push(i)
						interpreter.visit(loopblock.body,0)
						_ = dataStack.pop()
					except Exception as e:
						logging.error('Improper arguments for ' + word)
						logging.error(e)
			
		elif word == '2forloop':
			try:
				outerloopblock2 = dataStack.pop()
				innerloopblock = dataStack.pop()
				outerloopblock1 = dataStack.pop()
				n2 = dataStack.pop()
				n1 = dataStack.pop()
				if (n2 is not None) and (n1 is not None) and (innerloopblock is not None) and (outerloopblock1 is not None) and (outerloopblock2 is not None):
					for i1 in range(n1):
						dataStack.push(i1)
						interpreter.visit(outerloopblock1.body,0)
						for i2 in range(n2):
							dataStack.push(i2)
							interpreter.visit(innerloopblock.body,0)
							_ = dataStack.pop()
						interpreter.visit(outerloopblock2.body,0)
						_ = dataStack.pop()
						
			except Exception as e:
				logging.error('Improper arguments for ' + word)
				logging.error(e)
			
				
		elif word == 'ifelse':
			elseblock = dataStack.pop()
			trueblock = dataStack.pop()
			cond = dataStack.pop()
			if not cond == 0:
				if trueblock is not None:
					try:
						interpreter.visit(trueblock.body,0)
					except Exception as e:
						logging.error('Improper arguments for ' + word)
						logging.error(e)
			else:
				if elseblock is not None:
					try:
						interpreter.visit(elseblock.body,0)
					except Exception as e:
						logging.error('Improper arguments for ' + word)
						logging.error(e)
				
		elif word == 'while':
			loopblock = dataStack.pop()
			cond = dataStack.peek()
			if loopblock is not None:
				while cond:
					try:
						interpreter.visit(loopblock.body,0)
					except Exception as e:
						logging.error('Improper arguments for ' + word)
						logging.error(e)
					cond = dataStack.peek()
				
		elif word == 'until':
			loopblock = dataStack.pop()
			cond = dataStack.peek()
			if loopblock is not None:
				while not cond:
					try:
						interpreter.visit(loopblock.body,0)
					except Exception as e:
						logging.error('Improper arguments for ' + word)
						logging.error(e)
					cond = dataStack.peek()
		
		elif word == 'dip':
			block = dataStack.pop()
			n = dataStack.pop()
			if block is not None:
				try:
					interpreter.visit(block.body,0)
				except Exception as e:
					logging.error('Improper arguments for ' + word)
					logging.error(e)
			if n is not None:
				dataStack.push(n)
			
		elif word == 'keep':
			block = dataStack.pop()
			n = dataStack.peek()
			if block is not None:
				try:
					interpreter.visit(block.body,0)
				except Exception as e:
					logging.error('Improper arguments for ' + word)
					logging.error(e)
			if n is not None:
				dataStack.push(n)
			
		elif word == 'bi':
			q = dataStack.pop()
			p = dataStack.pop()
			if (p is not None) and (q is not None):
				try:
					interpreter.visit(p.body,0)
					interpreter.visit(q.body,0)
				except Exception as e:
					logging.error('Improper arguments for ' + word)
					logging.error(e)
				
		#################################################################
		#
		# String functions
		#
		#################################################################
		elif word == 'asc':
			a = dataStack.pop()
			dataStack.push(ord(a))
		elif word == 'chr':
			a = dataStack.pop()
			dataStack.push(chr(a))
		elif word == 'lcase':
			a = dataStack.pop()
			dataStack.push(str(a).lower())
		elif word == 'ucase':
			a = dataStack.pop()
			dataStack.push(str(a).upper())
		elif word == 'str':
			a = dataStack.pop()
			if a is not None:
				dataStack.push(str(a))
		elif word == 'unescape':
			a = dataStack.pop()
			if a is not None:
				try:
					dataStack.push(str(a).decode('string-escape'))
				except Exception as e:
					dataStack.push(str(a))
					logging.warning('String could not be unescaped')
					logging.debug(str(a))
					logging.debug(e)
		elif word == 'int':
			a = dataStack.pop()
			if a is not None:
				dataStack.push(int(a))
		elif word == 'cat':
			if dataStack.size() >= 2:
				b = dataStack.pop()
				a = dataStack.pop()
				c = str(a) + str(b)
				dataStack.push(c)
			else:
				logging.warning('Attempted to ' + word + ' from beyond the end of the stack [' + str(2) + '/' + str(dataStack.size()) + ']')
		elif word == 'cut':
			if dataStack.size() >= 2:
				n = dataStack.pop()
				c = dataStack.pop()
				a = c[:n]
				b = c[n:]
				dataStack.push(a)
				dataStack.push(b)
			else:
				logging.warning('Attempted to ' + word + ' from beyond the end of the stack [' + str(2) + '/' + str(dataStack.size()) + ']')
		elif word == 'charat':
			if dataStack.size() >= 2:
				n = dataStack.pop()
				c = dataStack.pop()
				a = c[n]
				dataStack.push(a)
			else:
				logging.warning('Attempted to ' + word + ' from beyond the end of the stack [' + str(2) + '/' + str(dataStack.size()) + ']')
		elif word == ',len':
			n = dataStack.peek()
			try:
				dataStack.push(len(n))
			except:
				dataStack.push(0)
		elif word == 'explode':
			n = str(dataStack.pop())
			for i in range(len(n)):
				dataStack.push(n[-(i+1)])
			dataStack.push(n)
		elif word == 'unexplode':
			n = int(dataStack.pop())
			s = ''
			for i in range(n):
				ss = dataStack.pop()
				if ss is not None:
					s += str(ss)
			dataStack.push(s)
		elif word == 'reverse':
			s = str(dataStack.pop())
			if s is not None:
				n = len(s)
				x=""
				for i in range(n):
					x += s[-(i+1)]
				dataStack.push(x)
				
		#################################################################
		#
		# Numeric base operations
		#
		#################################################################
		elif word == '>hex':
			n = dataStack.pop()
			dataStack.push("{0:x}".format(n))
		elif word == 'hex>':
			s = dataStack.pop()
			dataStack.push(int(s,16))
		elif word == '>bin':
			n = dataStack.pop()
			dataStack.push("{0:b}".format(n))
		elif word == 'bin>':
			s = dataStack.pop()
			dataStack.push(int(s,2))
		elif word == '>oct':
			n = dataStack.pop()
			dataStack.push("{0:o}".format(n))
		elif word == 'oct>':
			s = dataStack.pop()
			dataStack.push(int(s,8))
		
		#################################################################
		#
		# I/O and system functions
		#
		#################################################################
		elif word == '.':
			a = dataStack.pop()
			if a is not None:
				print(a),
		elif word == ',.':
			a = dataStack.peek()
			sys.stdout.write(dataStack.peek()),
		elif word == ',emit':
			a = dataStack.peek()
			if a:
				#prevents the addition of undesired spaces between characters
				sys.stdout.write(chr(a))
		elif word == 'cr':
			print('\n'),
		elif word == ',print':
			sys.stdout.write(str(dataStack.peek())),
		elif word == 'readline':
			text = raw_input()
			dataStack.push(text)
			
		elif word == 'load':
			name = str(dataStack.pop())
			try:
				with open(name,'rb') as f:
					text = f.read()
					dataStack.push(text)
			except:
				logging.error("Error reading file " + name)
				dataStack.push(None)
			dataStack.push(name)
		elif word == 'store':
			name = str(dataStack.pop())
			try:
				with open(name,'wb') as f:
					f.write(dataStack.pop())
			except:
				logging.error("Error writing file " + name)
			
		elif word == 'bye':
			print(' ok')
			exit()
			
		#if all else fails, attempt to treat the word as an integer
		else:
			try:
				dataStack.push(self.toInteger(word))
			
			#that fails, inform the user
			except ValueError:
				logging.error('"'+word + '" is not a known word or integer')
