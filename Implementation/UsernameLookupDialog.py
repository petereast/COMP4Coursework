from PyQt4.QtCore import *
from PyQt4.QtGui import *

from GlobalResources import *

from DatabaseInit import *

class UsernameLookup(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Select a user")

        self.raise_()
        self.parent = parent
        self.layout = QVBoxLayout()
        self.list = QListView()
        self.list.clicked.connect(self._select_user)
        self.users = UsersInfo().get_all_users()

        data = QStandardItemModel()

        for user in self.users:
            data.appendRow(QStandardItem(user[1]))

        self.list.setModel(data)

        self.layout.addWidget(self.list)
        self.setLayout(self.layout)

        # Get a list of names,
        # Onclick pass names down to the parent.
    def _select_user(self):
        user = self.users[self.list.selectedIndexes()[0].row()]
        self.parent.attendees_entry.setText(self.parent.attendees_entry.text()+", {0}".format(user[2]))
        self.close()
