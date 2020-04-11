from input_listener import InputListener
from commands import dispatcher


class NotesProgram:
    def __init__(self):
        self.input_listener = InputListener()

    def run(self):
        while True:
            try:
                command, args = self.input_listener.listen_command()
                dispatcher.dispatch(command, args)
            except KeyboardInterrupt:
                dispatcher.dispatch('exit', 'interrupted')


if __name__ == "__main__":
    program = NotesProgram()
    program.run()
