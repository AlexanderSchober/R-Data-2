# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RData(object):
    def setupUi(self, RData):
        RData.setObjectName("RData")
        RData.resize(1234, 892)
        RData.setStyleSheet("")
        self.main_widget = QtWidgets.QWidget(RData)
        self.main_widget.setStyleSheet("#main_widget{\n"
"background-color: rgb(64, 66, 68);}")
        self.main_widget.setObjectName("main_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.main_widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.main_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(100, 0))
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(35)
        self.verticalLayout.setObjectName("verticalLayout")
        self.env_button = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.env_button.sizePolicy().hasHeightForWidth())
        self.env_button.setSizePolicy(sizePolicy)
        self.env_button.setMinimumSize(QtCore.QSize(64, 40))
        self.env_button.setMaximumSize(QtCore.QSize(16777215, 30))
        self.env_button.setAutoFillBackground(False)
        self.env_button.setStyleSheet("#env_button { \n"
"background-color: transparent; \n"
"qproperty-icon: url(:/Ressources/env_raw.ico); \n"
"background: none; \n"
"border: none; \n"
"background-repeat: none; \n"
"} \n"
"#env_button:checked { \n"
"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.50033, fy:0.505682,stop:0 rgba(94, 0, 255, 255), stop:1 rgb(64, 66, 68) );\n"
"}\n"
"\n"
"")
        self.env_button.setText("")
        self.env_button.setIconSize(QtCore.QSize(45, 64))
        self.env_button.setCheckable(True)
        self.env_button.setChecked(True)
        self.env_button.setAutoRepeat(False)
        self.env_button.setAutoExclusive(False)
        self.env_button.setAutoDefault(False)
        self.env_button.setFlat(False)
        self.env_button.setObjectName("env_button")
        self.verticalLayout.addWidget(self.env_button)
        self.data_button = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_button.sizePolicy().hasHeightForWidth())
        self.data_button.setSizePolicy(sizePolicy)
        self.data_button.setMinimumSize(QtCore.QSize(64, 40))
        self.data_button.setMaximumSize(QtCore.QSize(16777215, 40))
        self.data_button.setAutoFillBackground(False)
        self.data_button.setStyleSheet("#data_button { \n"
"background-color: transparent; \n"
"qproperty-icon: url(:/Ressources/data.ico); \n"
"background: none; \n"
"border: none; \n"
"background-repeat: none; \n"
"} \n"
"#data_button:checked { \n"
"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.50033, fy:0.505682,stop:0 rgba(94, 0, 255, 255), stop:1 rgb(64, 66, 68) );\n"
"}")
        self.data_button.setText("")
        self.data_button.setIconSize(QtCore.QSize(45, 64))
        self.data_button.setCheckable(True)
        self.data_button.setChecked(True)
        self.data_button.setAutoRepeat(False)
        self.data_button.setAutoExclusive(False)
        self.data_button.setAutoDefault(False)
        self.data_button.setFlat(False)
        self.data_button.setObjectName("data_button")
        self.verticalLayout.addWidget(self.data_button)
        self.script_button = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.script_button.sizePolicy().hasHeightForWidth())
        self.script_button.setSizePolicy(sizePolicy)
        self.script_button.setMinimumSize(QtCore.QSize(64, 40))
        self.script_button.setMaximumSize(QtCore.QSize(16777215, 40))
        self.script_button.setAutoFillBackground(False)
        self.script_button.setStyleSheet("#script_button { \n"
"background-color: transparent; \n"
"qproperty-icon: url(:/Ressources/script.ico); \n"
"background: none; \n"
"border: none; \n"
"background-repeat: none; \n"
"} \n"
"#script_button:checked { \n"
"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.50033, fy:0.505682,stop:0 rgba(94, 0, 255, 255), stop:1 rgb(64, 66, 68) );\n"
"}\n"
"")
        self.script_button.setText("")
        self.script_button.setIconSize(QtCore.QSize(45, 64))
        self.script_button.setCheckable(True)
        self.script_button.setChecked(True)
        self.script_button.setAutoRepeat(False)
        self.script_button.setAutoExclusive(False)
        self.script_button.setAutoDefault(False)
        self.script_button.setFlat(False)
        self.script_button.setObjectName("script_button")
        self.verticalLayout.addWidget(self.script_button)
        self.save_button = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_button.sizePolicy().hasHeightForWidth())
        self.save_button.setSizePolicy(sizePolicy)
        self.save_button.setMinimumSize(QtCore.QSize(64, 40))
        self.save_button.setMaximumSize(QtCore.QSize(16777215, 40))
        self.save_button.setAutoFillBackground(False)
        self.save_button.setStyleSheet("#save_button { \n"
"background-color: transparent; \n"
"qproperty-icon: url(:/Ressources/save.ico); \n"
"background: none; \n"
"border: none; \n"
"background-repeat: none; \n"
"} \n"
"#save_button:checked { \n"
"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.50033, fy:0.505682,stop:0 rgba(94, 0, 255, 255), stop:1 rgb(64, 66, 68) );\n"
"}\n"
"")
        self.save_button.setText("")
        self.save_button.setIconSize(QtCore.QSize(45, 64))
        self.save_button.setCheckable(True)
        self.save_button.setChecked(True)
        self.save_button.setAutoRepeat(False)
        self.save_button.setAutoExclusive(False)
        self.save_button.setAutoDefault(False)
        self.save_button.setFlat(False)
        self.save_button.setObjectName("save_button")
        self.verticalLayout.addWidget(self.save_button)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.main_line_progress_0 = QtWidgets.QFrame(self.widget)
        self.main_line_progress_0.setFrameShape(QtWidgets.QFrame.HLine)
        self.main_line_progress_0.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.main_line_progress_0.setObjectName("main_line_progress_0")
        self.verticalLayout_3.addWidget(self.main_line_progress_0)
        self.main_label_progress_0 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_label_progress_0.sizePolicy().hasHeightForWidth())
        self.main_label_progress_0.setSizePolicy(sizePolicy)
        self.main_label_progress_0.setMinimumSize(QtCore.QSize(75, 0))
        self.main_label_progress_0.setMaximumSize(QtCore.QSize(64, 16777215))
        self.main_label_progress_0.setStyleSheet("#main_label_progress_0{color: rgb(179, 179, 179);}")
        self.main_label_progress_0.setAlignment(QtCore.Qt.AlignCenter)
        self.main_label_progress_0.setWordWrap(True)
        self.main_label_progress_0.setObjectName("main_label_progress_0")
        self.verticalLayout_3.addWidget(self.main_label_progress_0)
        self.main_bar_progress = QtWidgets.QProgressBar(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_bar_progress.sizePolicy().hasHeightForWidth())
        self.main_bar_progress.setSizePolicy(sizePolicy)
        self.main_bar_progress.setMinimumSize(QtCore.QSize(75, 0))
        self.main_bar_progress.setMaximumSize(QtCore.QSize(75, 16777215))
        self.main_bar_progress.setStyleSheet("")
        self.main_bar_progress.setProperty("value", 24)
        self.main_bar_progress.setAlignment(QtCore.Qt.AlignCenter)
        self.main_bar_progress.setObjectName("main_bar_progress")
        self.verticalLayout_3.addWidget(self.main_bar_progress)
        self.main_label_progress_1 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_label_progress_1.sizePolicy().hasHeightForWidth())
        self.main_label_progress_1.setSizePolicy(sizePolicy)
        self.main_label_progress_1.setMinimumSize(QtCore.QSize(75, 0))
        self.main_label_progress_1.setMaximumSize(QtCore.QSize(75, 16777215))
        self.main_label_progress_1.setStyleSheet("#main_label_progress_1{color: rgb(179, 179, 179);}")
        self.main_label_progress_1.setAlignment(QtCore.Qt.AlignCenter)
        self.main_label_progress_1.setWordWrap(True)
        self.main_label_progress_1.setObjectName("main_label_progress_1")
        self.verticalLayout_3.addWidget(self.main_label_progress_1)
        self.main_line_progress_1 = QtWidgets.QFrame(self.widget)
        self.main_line_progress_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.main_line_progress_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.main_line_progress_1.setObjectName("main_line_progress_1")
        self.verticalLayout_3.addWidget(self.main_line_progress_1)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setStyleSheet("#label{color: \"grey\";}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.widget)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setObjectName("main_layout")
        self.horizontalLayout.addLayout(self.main_layout)
        RData.setCentralWidget(self.main_widget)
        self.menubar = QtWidgets.QMenuBar(RData)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1234, 22))
        self.menubar.setObjectName("menubar")
        RData.setMenuBar(self.menubar)

        self.retranslateUi(RData)
        QtCore.QMetaObject.connectSlotsByName(RData)

    def retranslateUi(self, RData):
        _translate = QtCore.QCoreApplication.translate
        RData.setWindowTitle(_translate("RData", "MIEZE Tool"))
        self.main_label_progress_0.setText(_translate("RData", "TextLabel"))
        self.main_label_progress_1.setText(_translate("RData", "TextLabel"))
        self.label.setText(_translate("RData", "v 0.0.1"))

