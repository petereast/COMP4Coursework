from PyQt4.QtCore import *
from PyQt4.QtGui import *

from NewTaskDialog import *

from GlobalResources import *
from DatabaseInit import *
from Tasks import *

class TaskView(QWidget):
    def __init__(self, user = None):
        super().__init__()
        self.user = user

        self.main_layout = QVBoxLayout()


        self.title = QLabel("Outstanding Tasks")
        self.title.setFont(GTitleFont)

        self.main_layout.addWidget(self.title)

        # Set up the two-pane view

        self.pane_container = QWidget()
        self.pane_layout = QHBoxLayout()

        # Left side
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout()
        ##Task list

        self.task_list_view = QListView()

        self.update_task_list()


        self.left_layout.addWidget(self.task_list_view)
        self.left_widget.setLayout(self.left_layout)

        self.pane_layout.addWidget(self.left_widget)
        # End Left pane
        # Start right pane

        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout()

        self.add_new_task_button = QPushButton("Add new Task")
        self.add_new_task_button.setFixedWidth(150)
        self.add_new_task_button.clicked.connect(self.display_new_task_dialog)
        self.right_layout.addWidget(self.add_new_task_button)

        self.spacer = QLabel(" ")
        self.spacer.setFixedHeight(300)
        self.right_layout.addWidget(self.spacer)

        self.right_widget.setLayout(self.right_layout)
        self.pane_layout.addWidget(self.right_widget)
        # End right pane


        self.pane_container.setLayout(self.pane_layout)
        self.main_layout.addWidget(self.pane_container)

        self.setLayout(self.main_layout)

    def display_new_task_dialog(self):
        new_task_dialog = NewTaskDialog(self.user)

        new_task_dialog.exec_()
        self.update_task_list()

    def update_task_list(self):

        # Make it so that when the item is clicked, and the check box is 

        print("[INFO] Updating task list... ")
        # Add some data from the database
        data = QStandardItemModel()

        #Database fetch example
        ids = TasksInfo().get_ids_by_owner(self.user.id)
        print("[INFO] {0} Tasks found for user id: {0}".format(len(ids), self.user.id))
        self.tasks = []
        for taskID in ids:
            self.tasks.append(Task(databaseid=taskID))

            tmp = QStandardItem(self.tasks[-1].text)
            tmp.setCheckable(True)
            data.appendRow(tmp)
        self.task_list_view.setModel(data)
        print("[INFO] Task view update successful")
