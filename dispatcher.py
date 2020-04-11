class Dispatcher:
	def __init__(self):
		self.commands = {}

	def dispatch(self, command_name, command_args=None):
		if command_name in self.commands:
			command = self.commands.get(command_name)
			try:
				command.execute(*command_args)
			except Exception as e:
				command.on_fail(e)
		else:
			print("Unknown command")

	def register_command(self, command_class):
		self.commands[command_class.command_name] = command_class()
