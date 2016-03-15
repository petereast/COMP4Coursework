import sys

# import Qt depenencies
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from MainScreenGui import *
from GlobalResources import *

from LoginAction import *
from DatabaseInit import *

class PasswordWarningDialog(QDialog):
    def __init__(self, errormsg="", buttonmsg="Dismiss"):
        super().__init__()
        self.setModal(True)
        print("[INFO] Created Password Warning Dialog")

        self.setWindowTitle("Access Denied")

        self.main_layout = QVBoxLayout()

        self.title = QLabel("Access Denied")
        self.title.setFont(GTitleFont)
        self.main_layout.addWidget(self.title)

        self.text = QLabel(errormsg)
        self.text.setFont(GBodyFont)
        self.main_layout.addWidget(self.text)

        self.dismiss_button = QPushButton(buttonmsg)
        self.dismiss_button.clicked.connect(lambda: self.close())
        self.main_layout.addWidget(self.dismiss_button)

        self.subtext = QLabel("If the problem persists, please contact the system administrator.")
        self.subtext.setFont(GSmallText)
        self.main_layout.addWidget(self.subtext)

        self.setLayout(self.main_layout)

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        print("[INFO] Created Login window")

        self.setWindowTitle("[CMS] Login")

        self.main_title = QLabel("Welcome.")


        self.main_title.setFont(GTitleFont)

        # Create a labeled username feild:

        self.username_item = QWidget()

        self.username_layout = QHBoxLayout()


        self.username_label = QLabel("Username:")
        self.username_label.setFont(GBodyFont)
        self.username_label.setFixedWidth(150)

        self.username_input = QLineEdit()

        self.username_input.setWhatsThis("Enter your username here:")

        self.username_layout.addWidget(self.username_label)
        self.username_layout.addWidget(self.username_input)

        self.username_item.setLayout(self.username_layout)


        # Create a password feild

        self.password_item = QWidget()

        self.password_layout = QHBoxLayout()

        self.password_label = QLabel("Password:")
        self.password_label.setFont(GBodyFont)
        self.password_label.setFixedWidth(150)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self._enter_submit)

        self.password_input.setWhatsThis("Enter your password here")

        self.password_layout.addWidget(self.password_label)
        self.password_layout.addWidget(self.password_input)

        self.password_item.setLayout(self.password_layout)

        self.button_layout = QHBoxLayout()

        self.submit_button = QPushButton("Login")
        self.submit_button.clicked.connect(self.login_action)
        self.submit_button.setDefault(True)

        self.help_button = QPushButton("?")
        self.help_button.setFixedWidth(30)

        self.quit_button = QPushButton("Quit")

        self.button_layout.addWidget(self.submit_button)

        self.button_layout.addWidget(self.help_button)
        self.button_layout.addWidget(self.quit_button)

        # Add actions to the buttons within buttons_widget

        self.quit_button.clicked.connect(lambda: sys.exit(1))

        self.buttons_widget = QWidget()
        self.buttons_widget.setFixedWidth(300)
        self.buttons_widget.setLayout(self.button_layout)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.main_title)
        self.layout.addWidget(self.username_item)
        self.layout.addWidget(self.password_item)
        self.layout.addWidget(self.buttons_widget)

        self.setLayout(self.layout)
        self.setFont(GBodyFont)

        self.setFixedWidth(600)

    def _show_error_dialog(self, text="", button="Dismiss"):
        er = PasswordWarningDialog(text, button)
        er.show()
        er.raise_()
        er.exec_()

    def login_action(self, e = None):
        try:
            # Get  the user's id
            userid = UsersInfo().get_uid_by_username(self.username_input.text())

            # Create a User object with data related to the current userid
            user = User(userid) # User - class defined in LoginAction.py

            # If the hash of the input password does not match the stored hash
            if not user.password_hash_cmp(self.password_input.text()):

                # Show the warning dialog
                self._show_error_dialog("Password not recognised")
                # End the execution of the function.
                return 0

            else:

                # Create and run an instance of the MainScreen GUI.
                self.main_screen = MainScreen(user, self)
                self.main_screen.show()
                self.main_screen.raise_()

                # Hide this window.
                self.hide()

        # If the search for the useername does not return any results:
        except IndexError:
            self._show_error_dialog("Username not recognised")


    def reset(self):

        # Set both the input fields to ""
        self.password_input.setText("")
        self.username_input.setText("")


    # Event handler for pressing enter key.
    def _enter_submit(self, e = None):

        self.login_action(self)
