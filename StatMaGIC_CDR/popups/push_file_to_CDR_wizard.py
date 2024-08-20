from PyQt5.QtWidgets import QWizard, QWizardPage, QLabel, QLineEdit, QGridLayout, QComboBox, QFormLayout
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

        selectedFile = self.comboBox.currentLayer()
        selectedPath = self.fileInput.filePath()

        if selectedFile:
            self.registerField("input_path", selectedFile.source())
        elif selectedPath:
            self.registerField("input_path", selectedPath)
        else:
            pass


        self.setLayout(layout)


class Page2(QWizardPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setTitle('Fill out the required metadata')

        # create some widgets
        self.LayerName_LineEdit = QLineEdit()
        self.DataType_SpinBox = QComboBox()
        self.DataType_SpinBox.addItems(['Continuous', 'Binary', 'Categorical'])
        self.Category_SpinBox = QComboBox()
        self.Category_SpinBox.addItems(['Geophysics', 'Geology', 'Geochemistry'])
        self.subCategory_LineEdit = QLineEdit()
        self.AuthorName_LineEdit = QLineEdit()
        self.ReferenceURL_LineEdit = QLineEdit()
        self.doi_LineEdit = QLineEdit()
        self.publicationDate_LineEdit = QLineEdit()
        self.deriveOps_LineEdit = QLineEdit()

        layout = QFormLayout()
        layout.addRow('Layer Name: ', self.LayerName_LineEdit)
        layout.addRow('Author(s): ', self.AuthorName_LineEdit)
        layout.addRow('Data Type: ', self.DataType_SpinBox)
        layout.addRow('Category: ', self.Category_SpinBox)
        layout.addRow('Subcategory: ', self.subCategory_LineEdit)
        layout.addRow('Derivative Ops: ', self.deriveOps_LineEdit)
        layout.addRow('Publication Date: ', self.publicationDate_LineEdit)
        layout.addRow('Reference URL: ', self.ReferenceURL_LineEdit)
        layout.addRow('DOI: ', self.doi_LineEdit)

        self.setLayout(layout)

        # self.registerField('layer_name*', self.LayerName_LineEdit)
        # self.registerField('author_name*', self.AuthorName_LineEdit)
        # self.registerField('ref_url', self.ReferenceURL_LineEdit)
        # self.registerField('data_type', self.DataType_SpinBox.currentText())
        # self.registerField('category', self.CategorySpinBox.currentText())



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
