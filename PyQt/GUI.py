import fnmatch
import os
import shutil
from zipfile import ZipFile

import fitz
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QCheckBox, QPlainTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QMainWindow

from handlers.pdf_compressor import compress


# os.startfile(r'указывайте здесь путь к файлу')
# os.system('python путь_к_файлу.py')
# пример os.startfile(r'C:\Program Files\Notepad++\notepad++.exe')
def unz(my_dir, my_zip):
    pass


# def sub_in_str(def_str1, def_str2, def_text):
#     if def_str1 in def_text:
#         start_pos = def_text.find(def_str1) + len(def_str1)
#         end_pos = def_text.find(def_str2, start_pos)
#
#         return def_text[start_pos:end_pos]


def sub_in_str(name_pdf: str, name_find: str) -> str:
    name_pdf_unicode = name_pdf.encode('cp437').decode('cp866')

    if name_find in name_pdf_unicode:
        start_pos = name_pdf_unicode.find('/') + len('/')
        end_pos = len(name_pdf_unicode)

        return name_pdf_unicode[start_pos:end_pos]
    else:
        return ''


def save_pdf(name_zip: ZipFile, name_pdf: str, path_save: str) -> None:
    with name_zip.open(name_pdf) as fpr, open(path_save, "wb") as fpw:
        # копирование файлового объекта
        # без чтения и записи данных
        shutil.copyfileobj(fpr, fpw)


def merge_pdf(pdf_list: list, path_folder: str) -> None:
    result = fitz.open()

    for pdf in pdf_list:
        with fitz.open(path_folder + '/' + pdf) as mfile:
            result.insert_pdf(mfile)

    name_file = pdf_list[0].find('Акт')
    end_pos = pdf_list[0].find('.pdf')
    find_name = pdf_list[0][name_file:end_pos] + '.pdf'

    result.save(path_folder + '/' + find_name)
    # compress(path_folder + '/' + find_name, path_folder + '/compress/' + find_name, power=4)


def pars_zip(zip_file: ZipFile, path_folder: str) -> None:
    pdf_list = list()
    for name_pdf in zip_file.namelist():
        find_name = sub_in_str(name_pdf, 'Печатная форма')

        if 'Печатная форма' in find_name and ('Отчёт' in find_name or 'Акт' in find_name or 'итог' in find_name):

            if find_name in pdf_list:
                find_name = '2' + find_name
                pdf_list.append(find_name)
            else:
                pdf_list.append(find_name)

            path_save = os.path.join(path_folder, find_name)
            save_pdf(zip_file, name_pdf, path_save)

    if len(pdf_list) > 1:
        merge_pdf(pdf_list, path_folder)

        for name in pdf_list:
            myfile = path_folder + '/' + name
            # If file exists, delete it.
            if os.path.isfile(myfile):
                os.remove(myfile)
            else:
                # If it fails, inform the user.
                print("Error: %s file not found" % myfile)


class Form(QMainWindow):
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
