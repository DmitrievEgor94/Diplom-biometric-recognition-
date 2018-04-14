from PyQt5 import QtCore, QtGui, QtWidgets

import sys
import os
from face_extractor import get_faces_from_camera
import cv2

FACES_FOLDER = 'faces'


def get_right_word(number):
    if number // 10 % 10 == 1:
        return 'пользователей'
    else:
        if number % 10 == 1:
            return 'пользователь'
        if 1 < number % 10 < 5:
            return 'пользователя'
        return 'пользователей'


class UiMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(490, 491)
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)


        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("_v-minskom-aeroportu-zapuschena-b.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("treeView")
        self.listWidget.addItems(os.listdir(FACES_FOLDER))
        self.listWidget.installEventFilter(self.listWidget)
        self.listWidget.doubleClicked.connect(self.click_on_list)


        self.gridLayout_2.addWidget(self.listWidget, 0, 0, 7, 1)
        spacerItem = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 6, 1, 1, 1)

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)

        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)

        self.groupBox.setFont(font)
        self.groupBox.setTabletTracking(False)
        self.groupBox.setAutoFillBackground(True)
        self.groupBox.setObjectName("groupBox")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setObjectName("pushButton_4")

        self.verticalLayout_2.addWidget(self.pushButton_4)

        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.push_button_1)

        self.verticalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.push_button_2)

        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)
        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 2, 1)

        font_browser = QtGui.QFont()
        font_browser.setBold(True)
        font_browser.setWeight(90)

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setFont(font_browser)

        self.textBrowser.setObjectName("textBrowser")
        # self.textBrowser.setCursor(450)

        # print(self.textBrowser.cursorWidth())
        self.textBrowser.setText(
            ' ' * 10 + 'В данный момент в системе\n ' + ' ' * 20 + str(len(os.listdir(FACES_FOLDER)))
            + ' ' + get_right_word(len(os.listdir(FACES_FOLDER))))
        self.gridLayout_2.addWidget(self.textBrowser, 3, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 5, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 2, 1, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 490, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Биометрическая идентификация"))
        self.groupBox.setTitle(_translate("MainWindow", "Меню"))
        self.pushButton_4.setText(_translate("MainWindow", "Произвести идентификацию"))
        self.pushButton.setText(_translate("MainWindow", "Добавить пользователя"))
        self.pushButton_2.setText(_translate("MainWindow", "Добавить изображений"))
        self.pushButton_3.setText(_translate("MainWindow", "Построить базис"))
        self.menu.setTitle(_translate("MainWindow", "Помощь"))

    def push_button_1(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Ввод имени',
                             'Введите имя пользователя:')
        if ok:
            name = text
            get_faces_from_camera(5, 'faces/' + name)
            self.listWidget.addItem(name)
            self.textBrowser.setText(
                ' ' * 10 + 'В данный момент в системе\n ' + ' ' * 20 + str(len(os.listdir(FACES_FOLDER)))
                + ' ' + get_right_word(len(os.listdir(FACES_FOLDER))))

    def key_press_enter_top_list(self):
        print(2)

    def click_on_list(self):
        list_widget.clear()
        self.name_to_show = self.listWidget.selectedItems()[0].text()
        list_widget.addItems(os.listdir(FACES_FOLDER + '/' + self.name_to_show))
        list_widget.doubleClicked.connect(self.click_for_image_to_show)
        list_widget.show()

    def click_for_image_to_show(self):
        image = cv2.imread(FACES_FOLDER + '/' + self.name_to_show + '/' + list_widget.selectedItems()[0].text())
        cv2.imshow('face', image)

    def push_button_2(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Ввод имени',
                                                  'Введите имя пользователя:')
        if ok:
            name = text
            if name not in os.listdir(FACES_FOLDER):
                QtWidgets.QMessageBox.critical(self,'Ошибка', 'Пользователя нет в системе')
                return

            text, ok = QtWidgets.QInputDialog.getInt(self, 'Ввод количества изображений',
                                                      'Введите количество добавляемых изображений:')
            if ok:
                get_faces_from_camera(5, 'faces/' + name)
                self.listWidget.addItem(name)



# if __name__ == "__main__":
app = QtWidgets.QApplication(sys.argv)
interface_main_window = UiMainWindow()
interface_main_window.show()
list_widget = QtWidgets.QListWidget()
list_widget.setWindowTitle('Лица')

sys.exit(app.exec_())
