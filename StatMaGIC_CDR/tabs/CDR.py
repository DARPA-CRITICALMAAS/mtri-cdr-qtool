

from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer, QgsMessageLog
from PyQt5.QtWidgets import QPushButton, QTableWidget, QGridLayout, QFrame, QMessageBox
from pathlib import Path
import os, urllib3, json
from osgeo import gdal


from .TabBase import TabBase
from pathlib import Path
from ..popups.push_file_to_CDR_wizard import PushCDR_Wizard
from ..popups.CDR_token_config_dialog import CDR_PopUp_Menu

class cdrTab(TabBase):
    def __init__(self, parent, tabWidget, isEnabled=True):
        super().__init__(parent, tabWidget, "CDR", isEnabled)

        self.parent = parent

        self.home_button_frame = QFrame()
        home_buttons_Layout = QGridLayout()

        self.get_cred_button = QPushButton()
        self.get_cred_button.setText('Set CDR Token')
        self.get_cred_button.clicked.connect(self.launch_CDR_popup)

        self.pushCDRButton = QPushButton()
        self.pushCDRButton.setText('Publish Layer to CDR')
        self.pushCDRButton.clicked.connect(self.launch_CMA_wizard)

        self.pullCDRButton = QPushButton()
        self.pullCDRButton.setText('Pull Layer From CDR')
        self.pullCDRButton.setEnabled(False)

        home_buttons_Layout.addWidget(self.get_cred_button, 0, 0)
        home_buttons_Layout.addWidget(self.pushCDRButton, 0, 1)
        home_buttons_Layout.addWidget(self.pullCDRButton, 0, 2)

        self.home_button_frame.setLayout(home_buttons_Layout)
        self.tabLayout.addWidget(self.home_button_frame)

        # initialize lists to hold stuff later
        self.metadata_dict = {}
        # self.sourcelist = []
        # self.pathlist = []
        # self.methodlist = []
        # self.desclist = []
        # self.refreshTable()

    def launch_CMA_wizard(self):
        self.wizard = PushCDR_Wizard(self)
        self.wizard.show()

    def launch_CDR_popup(self):
        popup = CDR_PopUp_Menu(self.parent)
        self.cfg_menu = popup.show()

    def noCredentialsMessage(self):
        msgBox = QMessageBox()
        msgBox.setText("Unable to find CDR credentials")
        msgBox.exec()

    def assemble_metadata(self):
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
        data_type = self.wizard.field("data_type")
        category = self.wizard.field("category")
        subcategory = self.wizard.field("subcategory")
        ops = self.wizard.field("ops")
        date = self.wizard.field("date")
        doi = self.wizard.field("doi")
        input_path = self.wizard.field('input_path')
        QgsMessageLog.logMessage(f'input path: {input_path}')


        # with open(Path(proj_path, 'project_metadata.json'), 'w') as f:
        #     json.dump(meta_dict, f)

        _, xres, _, _, _, yres = gdal.Open(input_path).GetGeoTransform()
        resolution = [xres, yres]
        sid = f'{layer_name}_res0_{xres}_res1_{yres}_cat_LayerCategory{category.upper()}'

        msgBox = QMessageBox()
        msgBox.setText(f"Layer Name: {layer_name}     \n"
                       f"Author Names: {author_name} \n"
                       f"Publication Date: {date} \n"
                       f"Category: {category} \n"
                       f"Subcategory: {subcategory} \n"
                       f"Derivative Ops: {ops}  \n"
                       f"Input Path: {input_path}  \n"
                       f"Resolution: {resolution}  \n"
                       f"Data Source ID: {sid}  \n"
                       f"Data Type: {data_type} \n"
                       f"DOI: {doi} \n"
                       f"Ref URL: {ref_url}")
        msgBox.exec()


        #'''
        # UPDATE THIS TO TAKE IN INPUTS
        self.metadata_dict = {'authors': [author_name],
                         'publication_date': date,
                         'subcategory': subcategory,
                         'derivative_ops': ops,
                         'resolution': resolution,
                         'download_url': 'https://s3.amazonaws.com/public.cdr.land/prospectivity/inputs/0159507f9a7a4f7abd751af287a907c0.tif',
                         'evidence_layer_raster_prefix': layer_name,
                         'data_source_id': sid,
                         'DOI': doi,
                         'category': category,
                         'description': 'description',
                         'type': data_type,
                         'format': 'tif',
                         'reference_url': 'http'} # None is not accepted, empty string is also not accepted for 'reference_url'
        #'''




    def push_to_CDR(self):
        # Lu here is where you can test. Just use this for now and I'll debug getting it back from the qt wizard
        # layer_name = 'TEST LAYER'
        # author_name = 'TEST AUTHOR'
        # ref_url = None
        # input_path = '/ws1/idata/CriticalMAAS/example_data/test_push_file_to_CDR.tif'
        # data_type = 'Continuous'
        # category = 'TEST Geophysical'
        #
        input_path = self.wizard.field("input_path")


        with open(input_path, 'rb') as f:
            fread = f.read()
        cdr_host = "https://api.cdr.land"
        cdr_version = 'v1'
        token = os.environ['CDR_API_TOKEN']
        headers = {"Authorization": f"Bearer {token}"}
        http = urllib3.PoolManager()
        push_query = f'prospectivity/datasource'
        push_url = f'{cdr_host}/{cdr_version}/{push_query}'
        filename = Path(input_path).name
        payload = {
            'metadata': json.dumps(self.metadata_dict),
            'input_file': (filename, fread)
        }
        resp = http.request("POST", push_url, headers=headers, fields=payload)

