# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTabWidget, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(887, 729)
        icon = QIcon()
        icon.addFile(u"1643312787esp32.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBoxPorts = QComboBox(self.groupBox_2)
        self.comboBoxPorts.setObjectName(u"comboBoxPorts")

        self.horizontalLayout_2.addWidget(self.comboBoxPorts)

        self.pushButtonStartSerialMonitor = QPushButton(self.groupBox_2)
        self.pushButtonStartSerialMonitor.setObjectName(u"pushButtonStartSerialMonitor")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonStartSerialMonitor.sizePolicy().hasHeightForWidth())
        self.pushButtonStartSerialMonitor.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.pushButtonStartSerialMonitor)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 2, 1, 1)

        self.lineEditServerPortNumber = QLineEdit(self.groupBox_2)
        self.lineEditServerPortNumber.setObjectName(u"lineEditServerPortNumber")

        self.gridLayout.addWidget(self.lineEditServerPortNumber, 4, 2, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.lineEditServerAddress = QLineEdit(self.groupBox_2)
        self.lineEditServerAddress.setObjectName(u"lineEditServerAddress")

        self.gridLayout.addWidget(self.lineEditServerAddress, 3, 2, 1, 1)

        self.lineEditSSID = QLineEdit(self.groupBox_2)
        self.lineEditSSID.setObjectName(u"lineEditSSID")

        self.gridLayout.addWidget(self.lineEditSSID, 1, 2, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.lineEditPassword = QLineEdit(self.groupBox_2)
        self.lineEditPassword.setObjectName(u"lineEditPassword")

        self.gridLayout.addWidget(self.lineEditPassword, 2, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.gridLayout)

        self.tabWidget = QTabWidget(self.groupBox_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabTempHumid = QWidget()
        self.tabTempHumid.setObjectName(u"tabTempHumid")
        self.verticalLayout_3 = QVBoxLayout(self.tabTempHumid)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButtonUpload_DHT = QPushButton(self.tabTempHumid)
        self.pushButtonUpload_DHT.setObjectName(u"pushButtonUpload_DHT")

        self.gridLayout_2.addWidget(self.pushButtonUpload_DHT, 2, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditDeviceID_DHT = QLineEdit(self.tabTempHumid)
        self.lineEditDeviceID_DHT.setObjectName(u"lineEditDeviceID_DHT")

        self.horizontalLayout.addWidget(self.lineEditDeviceID_DHT)

        self.pushButtonAutoID_DHT = QPushButton(self.tabTempHumid)
        self.pushButtonAutoID_DHT.setObjectName(u"pushButtonAutoID_DHT")

        self.horizontalLayout.addWidget(self.pushButtonAutoID_DHT)


        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 1, 1, 1)

        self.label_7 = QLabel(self.tabTempHumid)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)

        self.comboBoxDHTType = QComboBox(self.tabTempHumid)
        self.comboBoxDHTType.addItem("")
        self.comboBoxDHTType.addItem("")
        self.comboBoxDHTType.addItem("")
        self.comboBoxDHTType.addItem("")
        self.comboBoxDHTType.setObjectName(u"comboBoxDHTType")

        self.gridLayout_2.addWidget(self.comboBoxDHTType, 0, 1, 1, 1)

        self.label_9 = QLabel(self.tabTempHumid)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 0, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tabTempHumid, "")
        self.tabVibration = QWidget()
        self.tabVibration.setObjectName(u"tabVibration")
        self.verticalLayout_4 = QVBoxLayout(self.tabVibration)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_10 = QLabel(self.tabVibration)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 1, 0, 1, 1)

        self.pushButtonUpload_VIB = QPushButton(self.tabVibration)
        self.pushButtonUpload_VIB.setObjectName(u"pushButtonUpload_VIB")

        self.gridLayout_3.addWidget(self.pushButtonUpload_VIB, 2, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEditDeviceID_VIB = QLineEdit(self.tabVibration)
        self.lineEditDeviceID_VIB.setObjectName(u"lineEditDeviceID_VIB")

        self.horizontalLayout_3.addWidget(self.lineEditDeviceID_VIB)

        self.pushButtonAutoID_VIB = QPushButton(self.tabVibration)
        self.pushButtonAutoID_VIB.setObjectName(u"pushButtonAutoID_VIB")

        self.horizontalLayout_3.addWidget(self.pushButtonAutoID_VIB)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)

        self.label_13 = QLabel(self.tabVibration)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_3.addWidget(self.label_13, 0, 0, 1, 1)

        self.comboBoxVIBType = QComboBox(self.tabVibration)
        self.comboBoxVIBType.addItem("")
        self.comboBoxVIBType.setObjectName(u"comboBoxVIBType")

        self.gridLayout_3.addWidget(self.comboBoxVIBType, 0, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tabVibration, "")
        self.tabNoise = QWidget()
        self.tabNoise.setObjectName(u"tabNoise")
        self.tabWidget.addTab(self.tabNoise, "")
        self.tabWeight = QWidget()
        self.tabWeight.setObjectName(u"tabWeight")
        self.verticalLayout_6 = QVBoxLayout(self.tabWeight)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_12 = QLabel(self.tabWeight)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_5.addWidget(self.label_12, 1, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lineEditDeviceID_WT = QLineEdit(self.tabWeight)
        self.lineEditDeviceID_WT.setObjectName(u"lineEditDeviceID_WT")

        self.horizontalLayout_5.addWidget(self.lineEditDeviceID_WT)

        self.pushButtonAutoID_WT = QPushButton(self.tabWeight)
        self.pushButtonAutoID_WT.setObjectName(u"pushButtonAutoID_WT")

        self.horizontalLayout_5.addWidget(self.pushButtonAutoID_WT)


        self.gridLayout_5.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)

        self.pushButtonUpload_WT = QPushButton(self.tabWeight)
        self.pushButtonUpload_WT.setObjectName(u"pushButtonUpload_WT")

        self.gridLayout_5.addWidget(self.pushButtonUpload_WT, 2, 1, 1, 1)

        self.label_14 = QLabel(self.tabWeight)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_5.addWidget(self.label_14, 0, 0, 1, 1)

        self.comboBoxWTType = QComboBox(self.tabWeight)
        self.comboBoxWTType.addItem("")
        self.comboBoxWTType.setObjectName(u"comboBoxWTType")

        self.gridLayout_5.addWidget(self.comboBoxWTType, 0, 1, 1, 1)


        self.verticalLayout_6.addLayout(self.gridLayout_5)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)

        self.tabWidget.addTab(self.tabWeight, "")

        self.verticalLayout_5.addWidget(self.tabWidget)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout_5.addWidget(self.label_2)

        self.textBrowserLogOutput = QTextBrowser(self.groupBox_2)
        self.textBrowserLogOutput.setObjectName(u"textBrowserLogOutput")

        self.verticalLayout_5.addWidget(self.textBrowserLogOutput)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout.addWidget(self.label_8)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lineEditSerialSend = QLineEdit(self.centralwidget)
        self.lineEditSerialSend.setObjectName(u"lineEditSerialSend")

        self.verticalLayout_2.addWidget(self.lineEditSerialSend)

        self.textBrowserSerialMonitor = QTextBrowser(self.centralwidget)
        self.textBrowserSerialMonitor.setObjectName(u"textBrowserSerialMonitor")

        self.verticalLayout_2.addWidget(self.textBrowserSerialMonitor)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 887, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"\uc885\ub8cc", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\ud504\ub85c\uadf8\ub7a8 \uc5c5\ub85c\ub4dc", None))
        self.pushButtonStartSerialMonitor.setText(QCoreApplication.translate("MainWindow", u"\ubaa8\ub2c8\ud130 \uc804\ud658", None))
        self.lineEditServerPortNumber.setText(QCoreApplication.translate("MainWindow", u"1883", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\uc640\uc774\ud30c\uc774 \ube44\ubc00\ubc88\ud638", None))
        self.lineEditServerAddress.setText(QCoreApplication.translate("MainWindow", u"kiotech.gonetis.com", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\uc640\uc774\ud30c\uc774 SSID", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\ub9ac\uc5bc \ud3ec\ud2b8", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\uc11c\ubc84\ud3ec\ud2b8", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\uc11c\ubc84\uc8fc\uc18c (MQTT)", None))
        self.pushButtonUpload_DHT.setText(QCoreApplication.translate("MainWindow", u"\uc5c5\ub85c\ub4dc\uc2dc\uc791", None))
        self.lineEditDeviceID_DHT.setText(QCoreApplication.translate("MainWindow", u"KITECH/ESP32/dht11/202510-001", None))
        self.pushButtonAutoID_DHT.setText(QCoreApplication.translate("MainWindow", u"\uc544\uc774\ub514 \uc790\ub3d9\uc0dd\uc131", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\ub514\ubc14\uc774\uc2a4 ID", None))
        self.comboBoxDHTType.setItemText(0, QCoreApplication.translate("MainWindow", u"DHT11", None))
        self.comboBoxDHTType.setItemText(1, QCoreApplication.translate("MainWindow", u"DHT22", None))
        self.comboBoxDHTType.setItemText(2, QCoreApplication.translate("MainWindow", u"RHT05", None))
        self.comboBoxDHTType.setItemText(3, QCoreApplication.translate("MainWindow", u"BME280", None))

        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\ub514\ubc14\uc774\uc2a4 \uc885\ub958", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTempHumid), QCoreApplication.translate("MainWindow", u"\uc628\uc2b5\ub3c4\uc13c\uc11c", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\ub514\ubc14\uc774\uc2a4 ID", None))
        self.pushButtonUpload_VIB.setText(QCoreApplication.translate("MainWindow", u"\uc5c5\ub85c\ub4dc\uc2dc\uc791", None))
        self.lineEditDeviceID_VIB.setText(QCoreApplication.translate("MainWindow", u"KITECH/ESP32/VIB01/202510-001", None))
        self.pushButtonAutoID_VIB.setText(QCoreApplication.translate("MainWindow", u"\uc544\uc774\ub514 \uc790\ub3d9\uc0dd\uc131", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\ub514\ubc14\uc774\uc2a4 \uc885\ub958", None))
        self.comboBoxVIBType.setItemText(0, QCoreApplication.translate("MainWindow", u"MPU6050", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabVibration), QCoreApplication.translate("MainWindow", u"\uc9c4\ub3d9\uc13c\uc11c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabNoise), QCoreApplication.translate("MainWindow", u"\uc18c\uc74c\uc13c\uc11c", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\ub514\ubc14\uc774\uc2a4 ID", None))
        self.lineEditDeviceID_WT.setText(QCoreApplication.translate("MainWindow", u"KITECH/ESP32/WT01/202510-001", None))
        self.pushButtonAutoID_WT.setText(QCoreApplication.translate("MainWindow", u"\uc544\uc774\ub514 \uc790\ub3d9\uc0dd\uc131", None))
        self.pushButtonUpload_WT.setText(QCoreApplication.translate("MainWindow", u"\uc5c5\ub85c\ub4dc\uc2dc\uc791", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\ub514\ubc14\uc774\uc2a4 \uc885\ub958", None))
        self.comboBoxWTType.setItemText(0, QCoreApplication.translate("MainWindow", u"HX711", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWeight), QCoreApplication.translate("MainWindow", u"\ubb34\uac8c\uc13c\uc11c", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\uc5c5\ub85c\ub4dc \uc9c4\ud589\uc0c1\ud669", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\ub9ac\uc5bc \ubaa8\ub2c8\ud130", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c", None))
    # retranslateUi

