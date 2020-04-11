class InputListener:
    prompt = '>'

    def __init__(self, prompt=None):
        if prompt:
            self.prompt = prompt

    def listen_command(self):
        user_input = self.get_input()
        command, *args = user_input.split()
        return command, args

    def get_input(self):
        prompt = self.prompt + ' '
        user_input = ''
        while not user_input:
            user_input = input(prompt).strip()
        return user_input
