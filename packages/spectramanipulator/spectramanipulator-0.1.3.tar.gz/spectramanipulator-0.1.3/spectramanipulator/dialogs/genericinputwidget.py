from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import sys


class GenericInputWidget(QtWidgets.QWidget):

    instance = None

    def __init__(self, widget_list=None, label_text='Some shity descriptive text...', title='GenericInputDialog',
                 parent=None):
        super(GenericInputWidget, self).__init__(parent)

        GenericInputWidget.instance = self

        self.accepted = False

        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.VLayout = QVBoxLayout()
        # self.VLayout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(label_text)
        self.label.setWordWrap(True)

        self.VLayout.addWidget(self.label)

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSpacing(7)
        self.grid_layout.setContentsMargins(15, 0, 0, 0)

        if widget_list is None:
            widget_list = [("par1", QLineEdit("some fucking text")),
                           ("par2", QLineEdit("some another fucking text")),
                           ("fuck paramters", QCheckBox("more shity text"))]

        self.label_list = []
        self.widget_list = []

        i = 0
        for label, widget in widget_list:
            self.label_list.append(QLabel(label + ':'))
            self.widget_list.append(widget)

            self.grid_layout.addWidget(self.label_list[i], i, 0)
            self.grid_layout.addWidget(widget, i, 1)
            i += 1

        self.VLayout.addItem(self.grid_layout)
        self.VLayout.addWidget(self.button_box)

        self.setLayout(self.VLayout)

        self.widget_list[0].setFocus()
        if isinstance(self.widget_list[0], QLineEdit):
            self.widget_list[0].selectAll()


    # virtual method
    def set_result(self):
        pass

    def accept(self):
        self.set_result()
        self.accepted = True
        GenericInputWidget.instance = None

    def reject(self):
        GenericInputWidget.instance = None


# if __name__ == "__main__":
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     Dialog = GenericInputDialog()
#     Dialog.show()
#     sys.exit(app.exec_())
