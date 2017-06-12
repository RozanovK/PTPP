from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTextEdit, QDesktopWidget, QMessageBox, QApplication, QLineEdit
import sys
from serwer import Socket

class Gui(QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(1000, 500)
        self.move(300, 300)
        self.setWindowTitle('PTPP 1.0')

        self.request = QLineEdit(self)
        self.request.setFixedWidth(960)
        self.request.move(20, 30)

        self.button = QPushButton("Send", self)
        self.button.move(430, 80)
        self.button.clicked.connect(self.button_click)

        self.response = QTextEdit(self)
        self.response.setFixedWidth(960)
        self.response.setFixedHeight(330)
        self.response.setReadOnly(True)
        self.response.move(20, 150)

        self.setWindowIcon(QIcon('static/101.jpg'))
        self.center()
        self.show()

    def button_click(self):
        request = self.request.text()
        file = serwer.serve_file(request=request)
        self.response.setText(str(file))

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Stop connection?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui()
    serwer = Socket('5005', '../../serwer/')
    sys.exit(app.exec_())