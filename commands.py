from dispatcher import Dispatcher
from notes_types import Note, NoteBuilder, NotesSaver
from input_listener import InputListener

dispatcher = Dispatcher()


class BaseCommand:
    command_name = None

    def execute(self, *args, **kwargs):
        raise NotImplementedError

    def on_fail(self, *args):
        raise NotImplementedError


@dispatcher.register_command
class HelpCommand(BaseCommand):
    """show help"""

    command_name = "help"

    def execute(self, *args, **kwargs):
        for command_name, command in sorted(dispatcher.commands.items(), key=lambda t: t[0]):
            print(command_name, ' - ', command.__doc__)

    def on_fail(self, *args):
        pass


@dispatcher.register_command
class ExitCommand(BaseCommand):
    """exit notes"""

    command_name = 'exit'

    def execute(self, *args, **kwargs):
        if "interrupted" not in args:
            print("Bye")
        else:
            print('\nBye')

        notes_saver = NotesSaver()
        notes_saver.save()

        exit()

    def on_fail(self, *args):
        pass


@dispatcher.register_command
class AddNoteCommand(BaseCommand):
    """add a note"""

    command_name = 'add'

    def _get_input(self, prompt=None):
        listener = InputListener(prompt)
        return listener.get_input()

    def _get_body_lines(self):
        while True:
            user_input = self._get_input("Enter body (to finish enter /end):")
            if user_input != "/end":
                yield user_input
            else:
                break

    def execute(self, *args, **kwargs):
        note_builder = NoteBuilder()
        note_builder.set_title(self._get_input("Enter title:"))

        for line in self._get_body_lines():
            note_builder.add_body_line(line)

        note_builder.to_note()
        print("Note has been successfully added")

    def on_fail(self, *args):
        pass


@dispatcher.register_command
class ListNotesCommand(BaseCommand):
    """show all notes"""

    command_name = "list"

    def execute(self, *args, **kwargs):
        note_saver = NotesSaver()
        notes = note_saver.get_notes_list()
        if notes:
            for note in notes:
                print(note.id, note.title, sep='\n')
                print('-' * 8)
        else:
            print("You don't have any notes")

    def on_fail(self, *args):
        pass


@dispatcher.register_command
class ShowNoteCommand(BaseCommand):
    """show specific note. use: show {note number} (to see all note's numbers use "list" command"""

    command_name = "show"

    def execute(self, note_id=None, *args, **kwargs):
        notes_saver = NotesSaver()
        note = notes_saver.notes.get(int(note_id))

        print('\n', note.prettify())

    def on_fail(self, *args):
        print("Incorrect note number")


@dispatcher.register_command
class DeleteNoteCommand(BaseCommand):
    """delete a note. use: delete {note number} (to see all note's numbers use "list" command"""

    command_name = 'delete'

    def execute(self, note_id=None, *args, **kwargs):
        notes_saver = NotesSaver()
        note = notes_saver.remove_note(int(note_id))
        print(f'Note "{note.title}" was successfully deleted')

    def on_fail(self, *args):
        print("Incorrect note number")
