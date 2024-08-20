import os
from qgis.PyQt.QtWidgets import QDialog, QLineEdit, QGridLayout, QLabel, QPushButton


class CDR_PopUp_Menu(QDialog):

    def __init__(self, parent):
        self.parent = parent
        self.iface = parent.iface
        super(CDR_PopUp_Menu, self).__init__(parent)
        QDialog.setWindowTitle(self, "CDR Token Input")

        self.enter_layout = QGridLayout()
        self.token = QLineEdit()
        self.updateButton = QPushButton()
        self.updateButton.setText('Update Credentials')
        self.updateButton.clicked.connect(self.set_vars)

        self.enter_layout.addWidget(QLabel('Enter CDR Token: '), 0, 0)
        self.enter_layout.addWidget(self.token, 0, 1)
        self.enter_layout.addWidget(self.updateButton, 1, 1)
        self.setLayout(self.enter_layout)


    def set_vars(self):
        token = self.token.text()
        os.environ['CDR_API_TOKEN'] = token
        self.reject()
        pass