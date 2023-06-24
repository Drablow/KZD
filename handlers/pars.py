import os
from zipfile import ZipFile
import shutil
import fitz


def unz(my_dir, my_zip):
    pass


# def sub_in_str(def_str1, def_str2, def_text):
#     if def_str1 in def_text:
#         start_pos = def_text.find(def_str1) + len(def_str1)
#         end_pos = def_text.find(def_str2, start_pos)
#
#         return def_text[start_pos:end_pos]


def sub_in_str(name_pdf: str, name_find: str) -> str:
    """
    Ищем стартовую и конечную позицию для обработки файлов
    """
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
    """
    Мержим pdf
    """
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
    """
    Ищем по ключевым словам в zip файлах
    """
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
                print("Ошибка: %s файл не найден" % myfile)
