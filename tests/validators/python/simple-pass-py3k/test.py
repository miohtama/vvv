import os

try:
	# Do some stuff
	foobar = os.environ
except Exception as e:
	# Python 2 dies here for syntax error
	pass 