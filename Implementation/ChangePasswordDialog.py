# The dialog for changing a user's password

from PyQt4 import QtCore
from PyQt4 import QtGui

from DatabaseInit import UsersInfo
from GlobalResources import *

class _PWErrorDialog(QDialog): #Blank error dialog
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Error")
        self.layout = QVBoxLayout()
        self.title = QLabel("Password Error")
        self.title.setFont(GTitleFont)
        self.layout.addWidget(self.title)
        self.label = QLabel("")
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

class _PWMismatchErrorDialog(_PWErrorDialog):
    def __init__(self):
        super().__init__()
        self.label.setText("New passwords do not match, try again")

class _PWCurrentIncorrectError(_PWErrorDialog):
    def __init__(self):
        super().__init__()
        self.label.setText("You password is incorrect")


class ChangePasswordDialog(QDialog):
    def __init__(self, user):
        super().__init__()

        INPUT_WIDTH = 400
        LABEL_WIDTH = 200

        self.user = user

        self.setWindowTitle("Change your password")

        self.layout = QVBoxLayout()

        self.title = QLabel("Change your password")
        self.title.setFont(GTitleFont)
        self.layout.addWidget(self.title)

        self.pw_current_container = QWidget()
        self.pw_current_entry = QLineEdit()
        self.pw_current_entry.setFixedWidth(INPUT_WIDTH)
        self.pw_current_entry_label = QLabel("Enter your current password:")
        self.pw_current_entry_label.setFixedWidth(LABEL_WIDTH)
        self.pw_current_entry.setEchoMode(QLineEdit.Password)

        self.pw_container_layout = QHBoxLayout()
        self.pw_container_layout.addWidget(self.pw_current_entry_label)
        self.pw_container_layout.addWidget(self.pw_current_entry)

        self.pw_current_container.setLayout(self.pw_container_layout)
        self.layout.addWidget(self.pw_current_container)

        self.new_pw_container = QWidget()
        self.new_pw_label = QLabel("Enter your new password:")
        self.new_pw_label.setFixedWidth(LABEL_WIDTH)
        self.new_pw_entry = QLineEdit()
        self.new_pw_entry.setFixedWidth(INPUT_WIDTH)
        self.new_pw_entry.setEchoMode(QLineEdit.Password)

        self.new_pw_layout = QHBoxLayout()
        self.new_pw_layout.addWidget(self.new_pw_label)
        self.new_pw_layout.addWidget(self.new_pw_entry)

        self.new_pw_container.setLayout(self.new_pw_layout)
        self.layout.addWidget(self.new_pw_container)

        self.confirm_pw_container = QWidget()
        self.confirm_pw_label = QLabel("Confirm your new password:")
        self.confirm_pw_label.setFixedWidth(LABEL_WIDTH)
        self.confirm_pw_entry = QLineEdit()
        self.confirm_pw_entry.setFixedWidth(INPUT_WIDTH)
        self.confirm_pw_entry.setEchoMode(QLineEdit.Password)
        self.confirm_pw_entry.returnPressed.connect(self._pwchange_action)

        self.confirm_pw_layout = QHBoxLayout()
        self.confirm_pw_layout.addWidget(self.confirm_pw_label)
        self.confirm_pw_layout.addWidget(self.confirm_pw_entry)

        self.confirm_pw_container.setLayout(self.confirm_pw_layout)
        self.layout.addWidget(self.confirm_pw_container)

        self.button_container = QWidget()
        self.button_container_layout = QHBoxLayout()
        self.accept_button = QPushButton("Accept")
        self.accept_button.clicked.connect(self._pwchange_action)
        self.button_container_layout.addWidget(self.accept_button)

        self.reject_button = QPushButton("Cancel")
        self.reject_button.clicked.connect(lambda: self.close())
        self.button_container_layout.addWidget(self.reject_button)

        self.button_container.setLayout(self.button_container_layout)
        self.layout.addWidget(self.button_container)

        self.setFont(GBodyFont)

        self.setLayout(self.layout)

    def _pwchange_action(self):
        # Generate passwrod hash
        # Get password hash from the database
        # Compare the two
        # if correct, update the database entry for the password
        # should be easy

        # Check that the pw entry and the pwconfirm are equal

        passwords_the_same = self.confirm_pw_entry.text() == self.new_pw_entry.text()
        current_pw_correct = self.user.password_hash_cmp(self.pw_current_entry.text())

        if passwords_the_same and current_pw_correct:
            UsersInfo().update_user_password(User.gen_pw_hash(None, self.new_pw_entry.text()), self.user.id)
            self.close()
            # Proceed to change the password
            print("[DEBUG] Passwords changed successfully (ChangePasswordDialog.py:126)")
        elif not passwords_the_same and current_pw_correct:
            e = _PWMismatchErrorDialog()
            e.show()
            e.exec_()
            # Display a messagebox explaining wtf is wrong.
        else:
            e = _PWCurrentIncorrectError()
            e.show()
            e.exec_()
