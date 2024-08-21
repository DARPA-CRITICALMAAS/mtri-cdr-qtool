from PyQt5.QtWidgets import QWizard, QWizardPage, QLabel, QLineEdit, QGridLayout, QComboBox, QFormLayout, QSpinBox, QDateTimeEdit
from qgis.gui import QgsFileWidget, QgsMapLayerComboBox
from qgis.core import QgsMapLayerProxyModel

class PushCDR_Wizard(QWizard):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.iface = self.parent.iface

        self.setWindowTitle("Publish to the CDR")

        self.extent_gdf = None
        self.bounds = None

        self.addPage(Page1(self))
        self.addPage(Page2(self))

        self.button(QWizard.FinishButton).clicked.connect(self.parent.assemble_metadata)

    def reject(self):
        # we need to call QWizard's reject method to actually close the window
        super().reject()

class Page1(QWizardPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setTitle('Select which data you want to publish')

        self.comboBox = QgsMapLayerComboBox(self)
        self.comboBox.setFilters(QgsMapLayerProxyModel.RasterLayer)
        self.comboBox.allowEmptyLayer()
        self.comboBox.setCurrentIndex(-1)

        self.fileInput = QgsFileWidget(self)

        label1 = QLabel('Choose From Current Map Layers:')
        label2 = QLabel('Choose From File Path:')

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.comboBox, 0, 1)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.fileInput, 1, 1)

        self.comboBox.layerChanged.connect(self.layer_changed)
        self.fileInput.fileChanged.connect(self.file_changed)
        self.registerField('input_path', self.fileInput)

        self.setLayout(layout)

    def file_changed(self):
        self.setField('input_path', self.fileInput.filePath())

    def layer_changed(self):
        selectedLayer = self.comboBox.currentLayer()
        self.setField('input_path', selectedLayer.source())


class Page2(QWizardPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setTitle('Fill out the required metadata')

        # create some widgets
        self.LayerName_LineEdit = QLineEdit()
        self.DataType_SpinBox = QComboBox()
        self.DataType_SpinBox.addItems(['continuous', 'binary', 'categorical'])
        self.Category_SpinBox = QComboBox()
        self.Category_SpinBox.addItems(['geophysics', 'geology', 'geochemistry'])
        self.subCategory_LineEdit = QLineEdit()
        self.AuthorName_LineEdit = QLineEdit()
        self.ReferenceURL_LineEdit = QLineEdit()
        self.doi_LineEdit = QLineEdit()
        self.publicationDate = QDateTimeEdit()
        self.deriveOps_LineEdit = QLineEdit()
        self.description_LineEdit = QLineEdit()

        layout = QFormLayout()
        layout.addRow('Layer Name: ', self.LayerName_LineEdit)
        layout.addRow('Author(s): ', self.AuthorName_LineEdit)
        layout.addRow('Data Type: ', self.DataType_SpinBox)
        layout.addRow('Category: ', self.Category_SpinBox)
        layout.addRow('Subcategory: ', self.subCategory_LineEdit)
        layout.addRow('Derivative Ops: ', self.deriveOps_LineEdit)
        layout.addRow('Publication Date: ', self.publicationDate)
        layout.addRow('Reference URL: ', self.ReferenceURL_LineEdit)
        layout.addRow('DOI: ', self.doi_LineEdit)
        layout.addRow('Description: ', self.description_LineEdit)

        self.setLayout(layout)

        self.registerField('layer_name', self.LayerName_LineEdit)
        self.registerField('author_name', self.AuthorName_LineEdit)
        self.registerField('data_type', self.DataType_SpinBox, property='currentText')
        self.registerField('category', self.Category_SpinBox, property='currentText')
        self.registerField('subcategory', self.subCategory_LineEdit)
        self.registerField('ops', self.deriveOps_LineEdit)
        self.registerField('date', self.publicationDate)
        self.registerField('ref_url', self.ReferenceURL_LineEdit)
        self.registerField('doi', self.doi_LineEdit)
        self.registerField('description', self.description_LineEdit)


        # self.CommentsText.textChanged.connect(self.commentsTyped)

        # Delete this when done testing
        # self.registerField('user_name', self.LayerName_LineEdit)
        # self.registerField('cma_name', self.CMA_NameLineEdit)
        # self.registerField('cma_mineral', self.CMA_MineralLineEdit)
        # self.registerField('comments', self.CommentsText)

    # def commentsTyped(self):
    #     self.setField("comments", self.CommentsText.toPlainText())

    def reject(self):
        pass
