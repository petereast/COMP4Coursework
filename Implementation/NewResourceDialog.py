from DatabaseInit import ResourcesInfo
from PyQt4 import QtCore, QtGui
from GlobalResources import *

class NewResourceDialog(QDialog):
    def __init__(self, user):
        super().__init__()

        self.setWindowTitle("Add a Resource")
        self.layout = QVBoxLayout()

        self.title = QLabel("Add a resource")
        self.title.setFont(GTitleFont)
        self.layout.addWidget(self.title)

        self.name_label = QLabel("Resource Name:")
        self.layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)

        self.cost_input = QLineEdit()
        self.layout.addWidget(self.cost_input)

        self.current_quantity = QLineEdit()
        self.layout.addWidget(self.current_quantity)
        self.setLayout(self.layout)
