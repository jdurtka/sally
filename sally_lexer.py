# James Durtka
#
# Toy language "Sally"
#		sally_lexer.py - Lexer for the "Sally" language
#

#these are the possible chunk delimiters:

#anything between comment_start and comment_end will be ignored
comment_start = '('
comment_end = ')'
#anything surrounded by a pair of the same string_delim will be passed through as a single word
string_delims = ['"', "'"]
#any special chars will automatically cut off as their own individual word
special_chars = ['[', ']', '{', '}', ':', ';']


#Token types
STRING, SPECIAL, WORD, EOF = 'STRING', 'SPECIAL', 'WORD', 'EOF'

#Token class borrowed from https://ruslanspivak.com/lsbasi-part1/
class Token(object):
	def __init__(self, type, value):
		self.type = type
		if value is None:
			self.value = ''
		else:
			self.value = value
		
	def __str__(self):
		return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

	def __repr__(self):
		return self.__str__()


#################################################################
#
# Breaks an input string into tokens
#
#################################################################
class Lexer(object):
	def __init__(self, text):
		self.text = text
		self.restart()
		
	def error(self, errspec):
		raise Exception('Syntax error: ' + errspec)
		
	#restart from earlier in the text
	def restart(self):
		self.pos = 0
		self.current_char = self.text[self.pos]
	def restartFrom(self,pos):
		self.pos = pos
		self.current_char = self.text[self.pos]
		
	#peek ahead
	def peek(self, amount):
		peekpos = self.pos+amount
		if (peekpos > len(self.text)-1):
			return ''
		else:
			return self.text[peekpos]
		
	#Advance through the input string by a single character
	def advance(self):
		self.pos += 1
		if ( self.pos > (len(self.text)-1) ):
			self.current_char = None
		else:
			self.current_char = self.text[self.pos]
		
	#if current character is whitespace, skip until it isn't
	def skipWhitespace(self):
		rv = False
		while (self.current_char is not None) and (self.current_char.isspace()):
			self.advance()
			rv = True
		return rv
			
	#if current character begins a comment, skip to the end of the comment
	def skipComments(self):
		rv = False
		if (self.current_char is not None) and (self.current_char == comment_start):
			depth = 1
			#skip the opening character
			self.advance()
			word = ''
			
			while (self.current_char is not None) and (depth > 0):
				#tracking depth allows us to have nested comments!
				if self.current_char == comment_end:
					depth -= 1
				elif self.current_char == comment_start:
					depth += 1
					
				#whatever it is, we're definitely skipping it
				self.advance()
				
			#skip the closing delimiter
			self.advance()
				
			rv = True
		return rv
	
	#if current character begins a string, grab the entire string
	def getString(self):
		if not self.current_char in string_delims:
			return None	#hack needed to ensure that empty strings are properly recognized as such
		else:
			word = self.continueUntil(self.current_char)
			return word
			
	#Tokenizes code by cutting whitespace and distinct "chunks"
	def getNextToken(self):
		word = ''
		
		#start by skipping any whitespace and/or comments found
		f = True
		while f:
			f = self.skipWhitespace()
			f = f or self.skipComments()
		
		#EOF so soon?
		if (self.current_char is None) or (self.current_char == ''):
			return Token(EOF,'')
		
		#are we beginning a string?
		word = self.getString()
		if word is not None:
			return Token(STRING,word)
		word = ''
		#what about a special character?
		if self.current_char in special_chars:
			word = self.current_char
			self.advance()
		if (word is not None) and not (word == ''):
			return Token(SPECIAL,word)
		
		#having eliminated all of the aforementioned things at the beginning, do a loop:
		while True:
			#if we are at EOF/EOL, return empty string
			if (self.current_char is None) or (self.current_char == ''):
				return Token(WORD,word)
				
			#if we encounter a comment, string, special char, or whitespace, cut the word here
			if self.current_char == comment_start:
				return Token(WORD,word)
			if self.current_char in string_delims:
				return Token(WORD,word)
			if self.current_char in special_chars:
				return Token(WORD,word)
			if self.current_char.isspace():
				return Token(WORD,word)
				
			#if we made it this far, it must be part of the current word!
			word += self.current_char
			self.advance()
	
	#skip through the input until a matching delimiter is found
	#use for strings, comments, but no nesting same-type delimiters!
	def continueUntil(self, delim):
		#skip the opening delimiter
		self.advance()
		word = ''
		while (self.current_char is not None) and not (self.current_char == delim):
			
			#hack for dealing with escaped characters in strings
			if (self.current_char == '\\'):
				word += self.current_char
				self.advance()
				word += self.current_char
				self.advance()
			else:
				word += self.current_char
				self.advance()
				
		#skip the closing delimiter
		self.advance()
		
		return word
		
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
		token = lexer.getNextToken()
		while (not token.type == EOF):
			print(token)
			if token.value.lower() == 'bye':
				done = True
			token = lexer.getNextToken()
		print(token)
		
if __name__ == '__main__':
	CLI_test()