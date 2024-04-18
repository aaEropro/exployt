from PyQt6.QtCore import *
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys


class LineEdit(QLineEdit):
    dir_path = ''

    def mousePressEvent(self, a0: QMouseEvent) -> None:

        self.dir_path = QFileDialog.getExistingDirectory(self, "Input Directory")
        self.setText(self.dir_path)

        return super().mousePressEvent(a0)


class Widget(QWidget):
    signal = None 

    def __init__(self, parent):
        super().__init__(parent)

        self.setLayout(QVBoxLayout())

        # MASTER CONTAINTER
        self.master_cont = QWidget()
        self.master_cont.setLayout(QVBoxLayout())
        self.master_cont.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # self.master_cont.layout().setAlignment(self.master_cont, Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.master_cont)

        # INDIVIDUAL CONTAINERS
        self.cont1 = QWidget()
        self.cont1.setLayout(QHBoxLayout())
        self.master_cont.layout().addWidget(self.cont1)
        # self.master_cont.layout().setAlignment(self.cont1, Qt.AlignmentFlag.AlignCenter)
        self.cont2 = QWidget()
        self.cont2.setLayout(QHBoxLayout())
        self.master_cont.layout().addWidget(self.cont2)
        # self.master_cont.layout().setAlignment(self.cont2, Qt.AlignmentFlag.AlignCenter)

        # LABELS
        input_folder_label = QLabel('FOLDER IN')
        input_folder_label.setMinimumWidth(120)
        self.cont1.layout().addWidget(input_folder_label)
        output_folder_label = QLabel('FOLDER OUT')
        output_folder_label.setMinimumWidth(120)
        self.cont2.layout().addWidget(output_folder_label)

        # INPUTS
        self.input_folder_input = LineEdit()
        self.input_folder_input.setMinimumWidth(400)
        self.input_folder_input.setReadOnly(True)
        self.cont1.layout().addWidget(self.input_folder_input)
        self.output_folder_input = LineEdit()
        self.output_folder_input.setMinimumWidth(400)
        self.output_folder_input.setReadOnly(True)
        self.cont2.layout().addWidget(self.output_folder_input)

        #CONFIRM
        self.confirm_button = QPushButton()
        self.confirm_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.confirm_button.setText("Confirm")
        self.confirm_button.clicked.connect(self.callback)
        self.master_cont.layout().addWidget(self.confirm_button)


    def callback(self):
        self.signal()


    def data(self):
        return self.input_folder_input.dir_path, self.output_folder_input.dir_path



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.resize(800, 800)

        self.widget_instance = Widget(self)
        self.widget_instance.signal = self.close
        self.setCentralWidget(self.widget_instance)

    def data(self):
        return self.widget_instance.data()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    instance = MainWindow()
    instance.show()

    sys.exit(app.exec())