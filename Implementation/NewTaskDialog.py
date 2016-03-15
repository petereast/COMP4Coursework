# NewTaskDialogGui

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from GlobalResources import *
from Tasks import *

from DatabaseInit import TasksInfo

class NewTaskDialog(QDialog):
    def __init__(self, user):
        self.user = user
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.setWindowTitle("Add new task")
        self.smalltitle = QLabel("Create new task")
        self.smalltitle.setFont(GBodyFont)
        self.title = QLabel("New Task")
        self.title.setFont(GTitleFont)

        self.main_layout.addWidget(self.smalltitle)
        self.main_layout.addWidget(self.title)

        self.title_entry_label = QLabel("Title:")
        self.main_layout.addWidget(self.title_entry_label)
        self.title_entry = QLineEdit("")
        self.title_entry.textChanged.connect(self.update_window_title)
        self.main_layout.addWidget(self.title_entry)

        #self.people_entry_label = QLabel("With whom:")
        #self.main_layout.addWidget(self.people_entry_label)

        #self.people_entry = QLineEdit()
        #self.people_entry.setPlaceholderText("Type usernames here")
        #self.people_entry.textChanged.connect(self.check_names)
        #self.main_layout.addWidget(self.people_entry)

        self.description_entry_label = QLabel("Description:")
        self.main_layout.addWidget(self.description_entry_label)

        self.description_entry = QLineEdit()
        self.main_layout.addWidget(self.description_entry)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.main_layout.addWidget(self.submit_button)

        self.setLayout(self.main_layout)
        self.setFont(GBodyFont)

    def update_window_title(self):
        newtext = self.title_entry.text()[0:45]
        if len(newtext) == 45:
            newtext += "..."
        if newtext == "":
            self.title.setText("New Task")
        else:
            self.title.setText(newtext)
        self.title_entry.setText(newtext)
        self.setWindowTitle(newtext)


        self.title_entry.setFixedWidth(self.title.width())

    def check_names(self):
        # Add some name checking functionality
        pass

    def validate(self):
        valid = True
        valid *= not (self.title_entry.text().strip() == "")
        # valid *= not (self.people_entry.text().strip() == "")
        valid *= not (self.description_entry.text().strip() == "")

        return valid


    def submit(self):
        if self.validate():
            info = {"Title":self.title_entry.text(), "Description":self.description_entry.text(), "OwnerID":self.user.id, "Attendees":"''"}
            TasksInfo().add_task(info)
            self.close()
        else:
            self.title_entry.setPlaceholderText("Required")
            #self.people_entry.setPlaceholderText("Required")
            self.description_entry.setPlaceholderText("Required")
