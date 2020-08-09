"""
Module for interpreting the code
into a python program
"""

class Interpreter:
	def __init__(self):
		self.commands = []
		self.interpreted = []
		self.figures_drawn = 0
		self.pointer = 0

	def push(self, command):
		self.commands.append(command)

	def interpret_args(self, args):
		"""Get args for python function calls"""
		stop_flag = False

		for i, arg in enumerate(args):
			if stop_flag:
				return
			if arg == 'ASSIGN':
				stop_flag = True
				yield self.build_assignment(args[i+1])
			else:
				yield str(arg)

	@staticmethod
	def build_assignment(args):
		return f"{args[0]} = {args[1]}"

	def interpret_operation(self, opname, args):
		"""Interpret operation based on operation name and arguments"""
		
		if opname == 'ASSIGN':
			self.interpreted.append(self.build_assignment(args))

		elif opname == 'CALL':
			function = args[0]
			params = ",".join(self.interpret_args(args[1:][0]))

			if function == 'cube':
				self.interpreted.insert(self.pointer, f'cube{self.figures_drawn} = Cube({params})')
				self.interpreted.append(f'cubes.append(cube{self.figures_drawn})')
				self.figures_drawn += 1

			elif function == 'translate' or 'rotate':
				self.interpreted.append(f'cube{self.figures_drawn}.{function}({params})')

			else:
				raise SyntaxError(function)

	def run(self):
		"""Run interpreter one operation at a time"""

		for command in self.commands:
			# Move pointer to position where a new cube initialization will take place
			self.pointer = len(self.interpreted)

			for opname, args in command:
				self.interpret_operation(opname, args)

		python_code = "\n".join(self.interpreted)
		template = open('lib/template.py', 'r').read()
		exec(template.replace('"PLACEHOLDER"', python_code))