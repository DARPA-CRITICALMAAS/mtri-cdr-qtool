

from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer
from PyQt5.QtWidgets import QPushButton, QTableWidget, QGridLayout, QFrame, QMessageBox

from .TabBase import TabBase
from pathlib import Path
from ..popups.push_file_to_CDR_wizard import PushCDR_Wizard

class cdrTab(TabBase):
    def __init__(self, parent, tabWidget, isEnabled=True):
        super().__init__(parent, tabWidget, "CDR", isEnabled)

        self.parent = parent

        self.home_button_frame = QFrame()
        home_buttons_Layout = QGridLayout()

        self.pushCDRButton = QPushButton()
        self.pushCDRButton.setText('Publish Layer to CDR')
        self.pushCDRButton.clicked.connect(self.launch_CMA_wizard)

        self.pullCDRButton = QPushButton()
        self.pullCDRButton.setText('Pull Layer From CDR')
        self.pullCDRButton.setEnabled(False)

        home_buttons_Layout.addWidget(self.pushCDRButton, 0, 0)
        home_buttons_Layout.addWidget(self.pullCDRButton, 0, 1)

        self.home_button_frame.setLayout(home_buttons_Layout)
        self.tabLayout.addWidget(self.home_button_frame)

        # initialize lists to hold stuff later
        # self.sourcelist = []
        # self.pathlist = []
        # self.methodlist = []
        # self.desclist = []
        # self.refreshTable()

    def launch_CMA_wizard(self):
        self.wizard = PushCDR_Wizard(self)
        self.wizard.show()

    def push_to_CDR(self):
        # Lu here is where you can test. Just use this for now and I'll debug getting it back from the qt wizard
        layer_name = 'TEST LAYER'
        author_name = 'TEST AUTHOR'
        ref_url = None
        input_path = '/ws1/idata/CriticalMAAS/example_data/test_push_file_to_CDR.tif'
        data_type = 'Continuous'
        category = 'TEST Geophysical'


        # Retrieve inputs
        layer_name = self.wizard.field("layer_name")
        author_name = self.wizard.field("author_name")
        ref_url = self.wizard.field("ref_url")
        input_path = self.wizard.field("input_path")
        data_type = self.wizard.field("data_type")
        category = self.wizard.field("category")


        # with open(Path(proj_path, 'project_metadata.json'), 'w') as f:
        #     json.dump(meta_dict, f)


        msgBox = QMessageBox()
        msgBox.setText(f"Layer Name: {layer_name}     \n"
                       f"Author Name {author_name} \n"
                       f"Data Type: {data_type} \n"
                       f"Category: {category} \n"
                       f"Input Path: {input_path}  \n"
                       f"Ref URL: {ref_url}")
        msgBox.exec()
        return