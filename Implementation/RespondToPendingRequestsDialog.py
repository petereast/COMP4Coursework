# Respond to meeting requests

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from GlobalResources import *
from Meetings import Meeting
from MeetingWidget import *
from DatabaseInit import MeetingsInfo


class RespondToPendingMeetingDialog(QDialog):
    def __init__(self, user):
        self.user = user
        super().__init__()

        #Respond to meeting request,
        # two panes, one for a list of pending meetings,
        # another for a tools and controls to deal with those
        # pending meetings
        self.setWindowTitle("Respond to Pending Requests")
        self.main_layout = QVBoxLayout()

        self.title = QLabel("Respond to Pending Requests")
        self.title.setFont(GTitleFont)
        self.main_layout.addWidget(self.title)

        self.pane_container = QWidget()
        self.pane_container_layout = QHBoxLayout()
        self.left_pane = QWidget()
        self.left_pane_layout = QVBoxLayout()

        self.meetings_list_view = QListView()
        self.meetings_list_view.clicked.connect(self._switch_right_stack)

        # End of 'following code'
        self.left_pane_layout.addWidget(self.meetings_list_view)


        self.left_pane.setLayout(self.left_pane_layout)

        self.right_pane = QWidget()
        self.right_pane_layout = QStackedLayout()

        self.meeting_view = PleaseSelectMeetingPlaceholder(len(MeetingsInfo({}).get_meetings_by_owner(self.user.id))==0)
        self.right_pane_layout.addWidget(self.meeting_view)
        self.update_pending_meeting_list()

        self.right_pane.setLayout(self.right_pane_layout)
        self.pane_container_layout.addWidget(self.left_pane)
        self.pane_container_layout.addWidget(self.right_pane)
        self.pane_container.setLayout(self.pane_container_layout)
        self.main_layout.addWidget(self.pane_container)


        self.setLayout(self.main_layout)

    def update_pending_meeting_list(self):
        print("[INFO] Updating list of pending appointments")

        self.data = QStandardItemModel()

        ids = MeetingsInfo().get_outstanding_meetings(self.user.id)
        print("[INFO] {0} meetings found for user id: {1}".format(len(ids), self.user.id))

        self.meetings = []
        for meetingID in ids:
            self.meetings.append(Meeting(meeting_id=meetingID[0]))
            meeting = self.meetings[-1]
            self.right_pane_layout.addWidget(PendingMeetingOverview(meeting, self.user))
            tmp = QStandardItem(meeting.title+"\n"+meeting.place+"\n"+meeting.when+"\n")
            tmp.setCheckable(False)
            self.data.appendRow(tmp)
        self.meetings_list_view.setModel(self.data)

        # Use a QStackedLayout to have the stack of meeting widgets

    def _switch_right_stack(self):
        index = self.meetings_list_view.selectedIndexes()[0].row()
        self.right_pane_layout.setCurrentIndex(index+1)
