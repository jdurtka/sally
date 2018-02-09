# James Durtka
#
# Toy language "Sally"
#		sally_stack.py - Stack for "Sally" language
#

import logging

#stack class borrowed from http://interactivepython.org/courselib/static/pythonds/BasicDS/ImplementingaStackinPython.html
class Stack:
	def __init__(self):
		self.items = []
	def __str__(self):
		return str(self.items)
	def isEmpty(self):
		return self.items == []
	def push(self, item):
		self.items.append(item)
	def pop(self):
		try:
			a = self.items.pop()
			return a
		except IndexError:
			logging.warning('Attempted to pop from an empty stack')
	def pullFrom(self,n):
		try:
			a = self.items[-n]
			del self.items[-n]
			return a
		except IndexError:
			logging.warning('Attempted to pull from beyond the end of the stack [' + str(n) + '/' + str(self.size()) + ']')
	def clear(self):
		self.items = []
	def peek(self):
		try:
			a = self.items[len(self.items)-1]
			return a
		except IndexError:
			logging.warning('Attempted to peek at an empty stack')
	def peekAt(self,n):
		try:
			a = self.items[-n]
			return a
		except IndexError:
			logging.warning('Attempted to peek from beyond the end of the stack [' + str(n) + '/' + str(self.size()) + ']')
	def size(self):
		return len(self.items)