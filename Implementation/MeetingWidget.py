# Meeting overview widget

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from GlobalResources import *
from Meetings import Meeting
from DatabaseInit import UsersInfo, MeetingsInfo
#from Meetings import *

class MeetingOverview(QFrame):
    def __init__(self, meeting):
        """
        Should take a Meeting object as a parameter rather than passing all of the individual parameters in.
        """
        super().__init__()
        self.meeting = meeting
        self.layout = QVBoxLayout()

        self.setFrameStyle(QFrame.StyledPanel + QFrame.Sunken)

        # Define the widgets

        self.title = QLabel(meeting.title)
        self.title.setFont(GTitleFont)
        self.layout.addWidget(self.title)

        self.place_title = QLabel("At: "+meeting.place)
        self.layout.addWidget(self.place_title)

        self.when_title = QLabel(meeting.when)
        self.layout.addWidget(self.when_title)

        self.owner_label = QLabel()
        self.layout.addWidget(self.owner_label)

        self.attendees_title = QLabel("Attendees:")
        self.layout.addWidget(self.attendees_title)

        self.attendees_list = []
        for index, person in enumerate(meeting.attendees):
            self.attendees_title.setText(self.attendees_title.text()+"\n"+person)

        #self.setMinimumHeight(100)
        self.buttons_widget = QWidget()
        self.buttons_layout = QHBoxLayout()

        self.delete_button = QPushButton("Delete")
        self.buttons_layout.addWidget(self.delete_button)

        self.edit_button = QPushButton("Edit")
        self.edit_button.setFixedWidth(150)
        self.buttons_layout.addWidget(self.edit_button)

        self.buttons_widget.setLayout(self.buttons_layout)
        self.layout.addWidget(self.buttons_widget)
        self.setLayout(self.layout)
        self.setMinimumSize(400, 200)
    
    def _edit_button_action(self):
        #Create a NewMeetingDialog with the information from this meeting
        pass
        

class PendingMeetingOverview(MeetingOverview):
    def __init__(self, meeting, user):
        super().__init__(meeting)
        self.meeting = meeting
        self.user = user
        # Get the owner's name
        owner_name = UsersInfo().get_username_by_uid(meeting.info["OwnerID"])
        self.owner_label.setText("From: {0}".format(owner_name))

        self.edit_button.setText("Respond - Confirm")
        self.edit_button.clicked.connect(self._accept_meeting)

        self.deny_button = QPushButton("Respond - Deny")
        self.deny_button.clicked.connect(self._reject_meeting)
        self.deny_button.setFixedWidth(150)
        self.buttons_layout.addWidget(self.deny_button)

    def _accept_meeting(self):
        MeetingsInfo().respond_to_attendance_request(True, self.meeting.meeting_id, self.user.id)
        print("[INFO] Meeting accepted")

    def _reject_meeting(self):
        MeetingsInfo().respond_to_attendance_request(False, self.meeting.meeting_id, self.user.id)
        print("[INFO] Meeting Rejected")

class PleaseSelectMeetingPlaceholder(QFrame):
    def __init__(self, empty = False):
        super().__init__()
        self.layout = QHBoxLayout()
        
        if not empty:
            self.label = QLabel("Please select\na meeting")
        else:
            self.label = QLabel("You have no\nnew meetings")
        self.label.setFont(GTitleFont)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setFixedWidth(300)
        
