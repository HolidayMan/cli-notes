import pickle


class Note:
    id = None
    title = None
    body = None

    def __init__(self, title, body, save=True):
        saver = NotesSaver()
        if len(saver.notes.keys()) > 0:
            note_number = max(saver.notes.keys()) + 1
        else:
            note_number = 1
        self.id = note_number
        self.title = title
        self.body = body
        if save:
            saver.add_note(self)

    def prettify(self):
        text = self.title.title() + "\n"
        text += self.body
        return text

    def save(self):
        saver = NotesSaver()
        saver.add_note(self)


class NoteBuilder:
    def __init__(self, title='', body=''):
        self._note = Note(title, body, save=False)

    def set_title(self, title):
        self._note.title = title

    def add_body_line(self, line):
        line = line.strip()
        self._note.body += line + '\n'

    def to_note(self):
        return self._note

    def save(self):
        self._note.save()
        return self._note


class NotesSaver:
    _notes = {}
    _object = None
    filename = "./notes.data"

    def __new__(cls, *args, **kwargs):
        if cls._object:
            return cls._object
        else:
            obj = super().__new__(cls, *args, **kwargs)
            cls._object = obj
            return obj

    def __init__(self):
        if not self._notes:
            self.upload()

    def save(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self._notes, file)

    def upload(self):
        try:
            with open(self.filename, "rb") as file:
                self._notes.update(pickle.load(file))
        except FileNotFoundError:
            self._notes = {}

    def add_note(self, note):
        self._notes[note.id] = note

    @property
    def notes(self):
        return self._notes

    def get_notes_list(self):
        return self._notes.values()

    def remove_note(self, note_id):
        return self._notes.pop(note_id)
