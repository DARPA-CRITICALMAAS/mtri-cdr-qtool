

from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer
from PyQt5.QtWidgets import QPushButton, QTableWidget, QGridLayout, QFrame, QMessageBox
from pathlib import Path
import os, urllib3, json

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

        '''
        # mostly copied this metadata from another test push
        metadata_dict = {'authors': [author_name],
                         'publication_date': '2024-08-19T15:25:34.155039',
                         'subcategory': 'subcategory',
                         'derivative_ops': 'derivative_ops',
                         'resolution': [3.0, 3.0], # this should be read from the file
                         'download_url': 'https://s3.amazonaws.com/public.cdr.land/prospectivity/inputs/0159507f9a7a4f7abd751af287a907c0.tif',
                         'evidence_layer_raster_prefix': 'evidence_layer_raster_prefix', # should this be layer_name?
                         'data_source_id': 'evidence_layer_raster_prefix_res0_3_res1_3_cat_LayerCategoryGEOPHYSICS',
                         # it looks like data_source_id is supposed to be constructed from the prefix, resolution, and category
                         'DOI': 'DOI',
                         'category': category,
                         'description': 'description',
                         'type': data_type,
                         'format': 'tif',
                         'reference_url': 'http'} # None is not accepted, empty string is also not accepted for 'reference_url'
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
            'metadata': json.dumps(metadata_dict),
            'input_file': (filename, fread)
        }
        resp = http.request("POST", push_url, headers=headers, fields=payload)
        #'''

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