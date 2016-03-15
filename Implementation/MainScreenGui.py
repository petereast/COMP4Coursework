# Copyright (c) 2015 Peter East All Rights Reserved.

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Import custom classes for this project

try:
    from MainScreenGui_DiaryView import *
    from MainScreenGui_TaskView import *
    from MainScreenGui_ResourcesView import *
    from MainScreenGui_UserAdminView import *
    from GlobalResources import *
except ImportError:
    print("[ERROR] Error loading modules")
    sys.exit(-1)



# Requires seperate widgets for each view in the tabbed layout
class MainScreen(QMainWindow):
    def __init__(self, user=None, parent=None):
        self.user = user
        self.parent = parent
        super().__init__()
        print("[INFO] Created MainScreenGui")

        self.setWindowTitle("[CMS] Main View")

        self.main_layout = QVBoxLayout()

        self.central_widget = QWidget()
        # Define the topbar
        self.topbar = QWidget()

        self.topbar_layout = QHBoxLayout()

        self.tb_help_button = QPushButton("?")
        self.tb_help_button.setFixedWidth(30)


        # Create a spacer to keep the thing spaced out
        self.tb_spacer = QLabel("  ")
        self.tb_spacer.setFixedWidth(600)

        self.tb_logout_button = QPushButton("Logout")
        self.tb_logout_button.setFixedWidth(100)
        self.tb_logout_button.clicked.connect(self._logout)

        self.topbar_layout.addWidget(self.tb_help_button)
        self.topbar_layout.addWidget(self.tb_spacer)
        self.topbar_layout.addWidget(self.tb_logout_button)

        self.topbar.setLayout(self.topbar_layout)

        # End of the topobar widget
        self.main_layout.addWidget(self.topbar)

        # Finish defining the topbar
        self.view_switcher = QTabWidget()

        # Define the views for the view_switcher
        # Diary View
        if self.user.permissions["Meetings"]:
            self.diary_view = DiaryView(self.user)
            self.view_switcher.addTab(self.diary_view, "Planner")
        # Task View
        if self.user.permissions["Tasks"]:
            self.task_view = TaskView(self.user)
            self.view_switcher.addTab(self.task_view, "Tasks")

        # Resources view
        if self.user.permissions["Resources"]:
            self.resources_view = ResourcesView(self.user)
            self.view_switcher.addTab(self.resources_view, "Resources")


        # User Admin View
        if self.user.permissions["ChangeOwnData"] or self.user.permissions["Admin"]:
            self.user_admin_view = UserAdminView(self.user)
            self.view_switcher.addTab(self.user_admin_view, "User Admin")


        # finish defining the view switcher


        self.view_switcher.setFont(GBodyFont)

        # End the definitions for the view swtich
        # Add the task view to the window
        self.main_layout.addWidget(self.view_switcher)


        # Fill in the window
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def _logout(self):
        self.user = None
        self.close()
        self.parent.show()
        self.parent.reset()
