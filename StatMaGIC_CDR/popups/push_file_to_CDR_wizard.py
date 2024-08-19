from PyQt5.QtWidgets import QWizard, QWizardPage, QLabel, QLineEdit, QGridLayout, QComboBox
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

        self.button(QWizard.FinishButton).clicked.connect(self.parent.push_to_CDR)

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
        self.LayerNameLineEdit = QLineEdit()
        self.DataTypeSpinBox = QComboBox()
        self.DataTypeSpinBox.addItems(['Continuous', 'Binary', 'Categorical'])
        self.CategorySpinBox = QComboBox()
        self.CategorySpinBox.addItems(['Geophysics', 'Geology', 'Geochemistry'])
        self.AuthorNameLineEdit = QLineEdit()
        self.ReferenceURLLineEdit = QLineEdit()

        # set the page layout
        layout = QGridLayout()
        layout.addWidget(QLabel('Layer Name'), 0, 0)
        layout.addWidget(self.LayerNameLineEdit, 0, 1)
        layout.addWidget(QLabel('Data Type'), 1, 0)
        layout.addWidget(self.DataTypeSpinBox, 1, 1)
        layout.addWidget(QLabel('Category'), 2, 0)
        layout.addWidget(self.CategorySpinBox, 2, 1)
        layout.addWidget(QLabel('Author Name'), 3, 0)
        layout.addWidget(self.AuthorNameLineEdit, 3, 1)
        layout.addWidget(QLabel('Reference URL (Optional)'), 4, 0)
        layout.addWidget(self.ReferenceURLLineEdit, 4, 1)

        self.setLayout(layout)

        self.registerField('layer_name*', self.LayerNameLineEdit)
        self.registerField('author_name*', self.AuthorNameLineEdit)
        self.registerField('ref_url', self.ReferenceURLLineEdit)
        # self.registerField('data_type', self.DataTypeSpinBox.currentText())
        # self.registerField('category', self.CategorySpinBox.currentText())



        # self.CommentsText.textChanged.connect(self.commentsTyped)

        # Delete this when done testing
        # self.registerField('user_name', self.LayerNameLineEdit)
        # self.registerField('cma_name', self.CMA_NameLineEdit)
        # self.registerField('cma_mineral', self.CMA_MineralLineEdit)
        # self.registerField('comments', self.CommentsText)

    # def commentsTyped(self):
    #     self.setField("comments", self.CommentsText.toPlainText())

    def reject(self):
        pass
