# Indicator Badge -  a PyQt widget to display a numerical indicator Badge

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from GlobalResources import *

class Indicator(QFrame):
    def __init__(self, value = 0):
        super().__init__()
        self.value = value

        self.main_layout = QVBoxLayout()

        self.value_display = QLabel(str(self.value))

        self.main_layout.addWidget(self.value_display)

        self.setFixedHeight(30)
        #self.setFixedWidth(30)
        self.colour = QColor(255, 61, 0)

        self.setStyleSheet("QFrame {background-color: %s;  border-radius: 15; background-clip: margin;}" % self.colour.name())

        self.text_colour = QColor(0xFF, 0xFF, 0xFF)

        self.value_display.setStyleSheet("QLabel {color: %s }" % self.text_colour.name())

        self.setFrameStyle(QFrame.StyledPanel + QFrame.Plain)
        self.setLayout(self.main_layout)

    def update(self, new_value):

        self.value = new_value

        self.value_display.setText(str(self.value))

        # do some cool stuff here :-)
    def getValue(self):
        return int(self.value)
