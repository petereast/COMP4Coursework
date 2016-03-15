from PyQt4.QtCore import *
from PyQt4.QtGui import *

from GlobalResources import *
from DatabaseInit import ResourcesInfo
from NewResourceDialog import *


class ResourcesView(QWidget):
    def __init__(self, user):

        # `user` - reference to instance created in 
        self.user = user
        super().__init__()

        print("[INFO] Created ResourcesView")

        self.main_layout = QVBoxLayout()

        self.title =  QLabel("Resources")
        self.title.setFont(GTitleFont)
        self.main_layout.addWidget(self.title)

        self.pane_container = QWidget()
        self.pane_container_layout = QHBoxLayout()

        self.left_pane_container = QWidget()
        self.left_pane_layout = QVBoxLayout()


        self.table = QTableWidget(3, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Cost", "Quantity", "Quantity Needed"])
        for col in range(4):
            self.table.setColumnWidth(col, 580/4)
        self.table.setFixedSize(601, 400)
        self.left_pane_layout.addWidget(self.table)
        self.update_table()
        # This is where I'll define the tabular view.
        # there also needs to be some code for getting sections of information
        # from the database - otherwise it won't work.

        self.left_pane_container.setLayout(self.left_pane_layout)
        self.pane_container_layout.addWidget(self.left_pane_container)
        self.right_pane_container = QWidget()
        self.right_pane_layout = QVBoxLayout()

        self.add_items_button = QPushButton("Add Resource")
        self.right_pane_layout.addWidget(self.add_items_button)
        self.add_items_button.clicked.connect(self._open_new_resource_dialog)
        self.view_urgent_requirements_button = QPushButton("View urgent requirements")
        self.right_pane_layout.addWidget(self.view_urgent_requirements_button)

        self.right_pane_container.setLayout(self.right_pane_layout)
        self.pane_container_layout.addWidget(self.right_pane_container)

        self.pane_container.setLayout(self.pane_container_layout)
        self.main_layout.addWidget(self.pane_container)


        self.setLayout(self.main_layout)

    def _open_new_resource_dialog(self):
        dg = NewResourceDialog(self.user)
        dg.show()
        dg.exec_()

    def update_table(self):
        self.table.clear()

        # Get information from database

        raw_data = ResourcesInfo().get_all_resources()

        # Table dimentions
        x_total = self.table.columnCount()
        y_total = len(raw_data)
        self.table.setRowCount(y_total)
        self.table.setHorizontalHeaderLabels(["Name", "Cost", "Quantity", "Quantity Needed"])
        for x in range(x_total):
            for y in range(y_total):
                self.table.setItem(y, x, QTableWidgetItem(str(raw_data[y][x+1])))
