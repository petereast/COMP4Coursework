from PyQt4.QtCore import *
from PyQt4.QtGui import *

from LoginAction import User
from GlobalResources import *

from ChangePasswordDialog import *

class UserOverview(QGroupBox):
    def __init__(self, user):
        self.user = user
        super().__init__()

        self.layout = QVBoxLayout()

        self.username_label = QLabel(user.info["Name"])
        self.username_label.setFont(GTitleFont)
        self.layout.addWidget(self.username_label)
        # Maybe add an image to represent the user's privelleges

        self.priv_label = QLabel("Standard User")
        self.priv_label.setFont(GSmallText)
        self.layout.addWidget(self.priv_label)

        self.control_bar = QWidget()
        self.controls_layout = QHBoxLayout()

        #Controls:
        self.rename_button = QPushButton("Change Name")
        self.controls_layout.addWidget(self.rename_button)
        self.rename_button.setDisabled(not self.user.permissions["ChangeOwnData"])

        self.change_password_button = QPushButton("Change Password")
        self.controls_layout.addWidget(self.change_password_button)
        self.change_password_button.clicked.connect(self._show_change_password_window)
        self.change_password_button.setDisabled(not self.user.permissions["ChangeOwnData"])
        print(not self.user.permissions["ChangeOwnData"])
        print(self.user.permissions)

        self.control_bar.setLayout(self.controls_layout)
        self.control_bar.setFixedWidth(300)
        self.control_bar.setFont(GSmallText)
        self.layout.addWidget(self.control_bar)

        self.setLayout(self.layout)
        self.setFixedHeight(160)
        self.setTitle("Me")

    def _show_change_password_window(self):
        pwdwindow = ChangePasswordDialog(self.user)

        pwdwindow.show()
        pwdwindow.exec_()

class UserAdminView(QWidget):
    def __init__(self, user):
        self.user = user
        super().__init__()

        print("[INFO] Created MainScreenGuiUserAdminView")


        self.master_layout = QVBoxLayout()

        self.this_user_header =  UserOverview(self.user)
        self.master_layout.addWidget(self.this_user_header)

        # Add the admin controls - which will either be hidden or disabled for the users without
        # the proper privellages

        self.admin_tools = QGroupBox()
        self.admin_tools.setTitle("Administrative Tools") #Set this to change depending on if the thing is locked or not
        self.admin_tools_layout = QVBoxLayout()

        # Show a scrollable list of the UserOverview(s) for all the registered users, and add management
        # tools, eg "Delete User", "Add new user"

        # It miggh be a good idea to wait until the card updating system is sorted.
        self.admin_tools.setLayout(self.admin_tools_layout)

        self.master_layout.addWidget(self.admin_tools)

        self.admin_tools.setFont(GBodyFont)

        self.setLayout(self.master_layout)
