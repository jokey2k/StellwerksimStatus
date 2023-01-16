# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'statusdialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QLabel,
    QLineEdit, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(428, 449)
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout_3 = QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.South)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.currentRailwayControlCenterLabel = QLabel(self.tab)
        self.currentRailwayControlCenterLabel.setObjectName(u"currentRailwayControlCenterLabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.currentRailwayControlCenterLabel)

        self.currentRailwayControlCenterLineEdit = QLineEdit(self.tab)
        self.currentRailwayControlCenterLineEdit.setObjectName(u"currentRailwayControlCenterLineEdit")
        self.currentRailwayControlCenterLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.currentRailwayControlCenterLineEdit)

        self.currentRailwayControlCenterRegionLabel = QLabel(self.tab)
        self.currentRailwayControlCenterRegionLabel.setObjectName(u"currentRailwayControlCenterRegionLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.currentRailwayControlCenterRegionLabel)

        self.currentRailwayControlCenterRegionLineEdit = QLineEdit(self.tab)
        self.currentRailwayControlCenterRegionLineEdit.setObjectName(u"currentRailwayControlCenterRegionLineEdit")
        self.currentRailwayControlCenterRegionLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.currentRailwayControlCenterRegionLineEdit)

        self.inGameClockLabel = QLabel(self.tab)
        self.inGameClockLabel.setObjectName(u"inGameClockLabel")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.inGameClockLabel)

        self.inGameClockLineEdit = QLineEdit(self.tab)
        self.inGameClockLineEdit.setObjectName(u"inGameClockLineEdit")
        self.inGameClockLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.inGameClockLineEdit)

        self.playDurationLabel = QLabel(self.tab)
        self.playDurationLabel.setObjectName(u"playDurationLabel")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.playDurationLabel)

        self.playDurationLineEdit = QLineEdit(self.tab)
        self.playDurationLineEdit.setObjectName(u"playDurationLineEdit")
        self.playDurationLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.playDurationLineEdit)

        self.instanceLabel = QLabel(self.tab)
        self.instanceLabel.setObjectName(u"instanceLabel")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.instanceLabel)

        self.instanceLineEdit = QLineEdit(self.tab)
        self.instanceLineEdit.setObjectName(u"instanceLineEdit")
        self.instanceLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.instanceLineEdit)

        self.onlineLabel = QLabel(self.tab)
        self.onlineLabel.setObjectName(u"onlineLabel")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.onlineLabel)

        self.onlineLineEdit = QLineEdit(self.tab)
        self.onlineLineEdit.setObjectName(u"onlineLineEdit")
        self.onlineLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.onlineLineEdit)

        self.currentTrainCountLabel = QLabel(self.tab)
        self.currentTrainCountLabel.setObjectName(u"currentTrainCountLabel")

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.currentTrainCountLabel)

        self.currentTrainCountLineEdit = QLineEdit(self.tab)
        self.currentTrainCountLineEdit.setObjectName(u"currentTrainCountLineEdit")
        self.currentTrainCountLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.currentTrainCountLineEdit)

        self.amountOfIncreasedDelayLabel = QLabel(self.tab)
        self.amountOfIncreasedDelayLabel.setObjectName(u"amountOfIncreasedDelayLabel")

        self.formLayout_2.setWidget(7, QFormLayout.LabelRole, self.amountOfIncreasedDelayLabel)

        self.amountOfIncreasedDelayLineEdit = QLineEdit(self.tab)
        self.amountOfIncreasedDelayLineEdit.setObjectName(u"amountOfIncreasedDelayLineEdit")
        self.amountOfIncreasedDelayLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(7, QFormLayout.FieldRole, self.amountOfIncreasedDelayLineEdit)

        self.amountOfDecreasedDelayLabel = QLabel(self.tab)
        self.amountOfDecreasedDelayLabel.setObjectName(u"amountOfDecreasedDelayLabel")

        self.formLayout_2.setWidget(8, QFormLayout.LabelRole, self.amountOfDecreasedDelayLabel)

        self.amountOfDecreasedDelayLineEdit = QLineEdit(self.tab)
        self.amountOfDecreasedDelayLineEdit.setObjectName(u"amountOfDecreasedDelayLineEdit")
        self.amountOfDecreasedDelayLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(8, QFormLayout.FieldRole, self.amountOfDecreasedDelayLineEdit)

        self.trainCountInSessionLabel = QLabel(self.tab)
        self.trainCountInSessionLabel.setObjectName(u"trainCountInSessionLabel")

        self.formLayout_2.setWidget(9, QFormLayout.LabelRole, self.trainCountInSessionLabel)

        self.trainCountInSessionLineEdit = QLineEdit(self.tab)
        self.trainCountInSessionLineEdit.setObjectName(u"trainCountInSessionLineEdit")
        self.trainCountInSessionLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(9, QFormLayout.FieldRole, self.trainCountInSessionLineEdit)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_2 = QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.communicatorAddressLabel = QLabel(self.tab_3)
        self.communicatorAddressLabel.setObjectName(u"communicatorAddressLabel")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.communicatorAddressLabel)

        self.communicatorAddressLineEdit = QLineEdit(self.tab_3)
        self.communicatorAddressLineEdit.setObjectName(u"communicatorAddressLineEdit")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.communicatorAddressLineEdit)

        self.homepageLabel = QLabel(self.tab_3)
        self.homepageLabel.setObjectName(u"homepageLabel")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.homepageLabel)

        self.homepageLineEdit = QLineEdit(self.tab_3)
        self.homepageLineEdit.setObjectName(u"homepageLineEdit")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.homepageLineEdit)


        self.verticalLayout_4.addLayout(self.formLayout_3)

        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_3.addWidget(self.tabWidget)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Stellwerksim Status Tool", None))
        self.currentRailwayControlCenterLabel.setText(QCoreApplication.translate("Dialog", u"Current railway control center", None))
        self.currentRailwayControlCenterRegionLabel.setText(QCoreApplication.translate("Dialog", u"Control center region", None))
        self.inGameClockLabel.setText(QCoreApplication.translate("Dialog", u"In game clock", None))
        self.playDurationLabel.setText(QCoreApplication.translate("Dialog", u"Play duration", None))
        self.instanceLabel.setText(QCoreApplication.translate("Dialog", u"Instance", None))
        self.onlineLabel.setText(QCoreApplication.translate("Dialog", u"Online", None))
        self.currentTrainCountLabel.setText(QCoreApplication.translate("Dialog", u"Current train count", None))
        self.amountOfIncreasedDelayLabel.setText(QCoreApplication.translate("Dialog", u"Amount of increased delay", None))
        self.amountOfDecreasedDelayLabel.setText(QCoreApplication.translate("Dialog", u"Amount of decreased delay", None))
        self.trainCountInSessionLabel.setText(QCoreApplication.translate("Dialog", u"Train count in session", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Stellwerkstate", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"stellwerksim.de", None))
        self.communicatorAddressLabel.setText(QCoreApplication.translate("Dialog", u"Communicator Address", None))
        self.homepageLabel.setText(QCoreApplication.translate("Dialog", u"Homepage", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Dialog", u"Settings", None))
    # retranslateUi

