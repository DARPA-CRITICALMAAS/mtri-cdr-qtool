# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTabWidget, QDockWidget, QHBoxLayout
from qgis.PyQt.QtCore import pyqtSignal
from .tabs.CDR import cdrTab



class StatMaGICDockWidget(QDockWidget):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(StatMaGICDockWidget, self).__init__(parent)
        self.iface = parent.iface
        self.canvas = self.iface.mapCanvas()
        self.setObjectName("StatMaGICDockWidget")
        self.dockWidgetContents = QWidget(self)
        self.dockWidgetLayout = QVBoxLayout()
        self.dockWidgetContents.setLayout(self.dockWidgetLayout)

        my_widget = QWidget(self.dockWidgetContents)
        my_widget.setLayout(QHBoxLayout())
        my_widget.parent().layout().addWidget(my_widget)

        self.createTabs()
        self.setWidget(self.dockWidgetContents)


    def createTabs(self):
        # create tab container
        self.tabWidget = QTabWidget(self.dockWidgetContents)

        # populate tabs
        self.cdr_tab = cdrTab(self, self.tabWidget)
        self.tabWidget.parent().layout().addWidget(self.tabWidget)


    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
