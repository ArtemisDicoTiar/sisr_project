# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
#
#
# class MyApp(QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         label1 = QLabel('Label1', self)
#         label1.move(20, 20)
#         label2 = QLabel('Label2', self)
#         label2.move(20, 60)
#
#         btn1 = QPushButton('Button1', self)
#         btn1.move(80, 13)
#         btn2 = QPushButton('Button2', self)
#         btn2.move(80, 53)
#
#         self.setWindowTitle('Absolute Positioning')
#         self.setGeometry(300, 300, 400, 200)
#         self.show()
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyApp()
#     sys.exit(app.exec_())
#

import sys
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog)


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.edit = QLineEdit("Write my name here")
        self.button = QPushButton("Show Greetings")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)

    # Greets the user
    def greetings(self):
        print ("Hello %s" % self.edit.text())


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())

