import fnmatch
import os

from zipfile import ZipFile

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QCheckBox, QPlainTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QMainWindow

from handlers.pars import pars_zip
from handlers.pdf_compressor import compress


class Form(QMainWindow):
    """
    Форма нашего распаковщика
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setFont(QFont('Arial', 11))

        cb = QCheckBox('не в архиве', self)
        cb.move(20, 20)
        cb.toggle()
        cb.stateChanged.connect(self.change_title)

        open_dir_button = QPushButton("Открыть папку")
        open_dir_button.clicked.connect(self.get_directory)

        layout_v = QVBoxLayout()
        layout_v.addWidget(open_dir_button)

        layout_h = QHBoxLayout()
        layout_h.addLayout(layout_v)
        layout_h.addWidget(self.plainTextEdit)

        center_widget = QWidget()
        center_widget.setLayout(layout_h)
        self.setCentralWidget(center_widget)

        self.resize(740, 480)
        self.setWindowTitle("КС")

    def change_title(self, state):
        if state == Qt.Checked:
            self.setWindowTitle('QCheckBox')
        else:
            self.setWindowTitle('')

    def get_directory(self) -> None:
        """

        """
        path_folder = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.plainTextEdit.appendHtml("<br>Выбрали папку: <b>{}</b>".format(path_folder))

        for file in os.listdir(path_folder):
            if fnmatch.fnmatch(file, '*.zip'):  # ищем зипы
                zip_file = ZipFile(path_folder + "/" + file)
                self.plainTextEdit.appendHtml("<br>Имя zip файла: <b>{}</b>".format(file))

                pars_zip(zip_file, path_folder)

        for file in os.listdir(path_folder):
            if '.pdf' in file:
                compress(path_folder + '/' + file, path_folder + '/compress/' + file, power=4)
