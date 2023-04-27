import sys

from PyQt5.QtWidgets import QApplication

from PyQt.GUI import Form

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()

    sys.exit(app.exec_())
