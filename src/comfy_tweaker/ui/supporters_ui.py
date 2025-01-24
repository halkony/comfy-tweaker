# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'supporters.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Supporters(object):
    def setupUi(self, Supporters):
        if not Supporters.objectName():
            Supporters.setObjectName(u"Supporters")
        Supporters.resize(688, 430)
        self.verticalLayout = QVBoxLayout(Supporters)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.patreonLogo = QLabel(Supporters)
        self.patreonLogo.setObjectName(u"patreonLogo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.patreonLogo.sizePolicy().hasHeightForWidth())
        self.patreonLogo.setSizePolicy(sizePolicy)
        self.patreonLogo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.patreonLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.patreonLogo)

        self.label = QLabel(Supporters)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.supportersLabel1 = QLabel(Supporters)
        self.supportersLabel1.setObjectName(u"supportersLabel1")
        self.supportersLabel1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.supportersLabel1)

        self.supportersLabel2 = QLabel(Supporters)
        self.supportersLabel2.setObjectName(u"supportersLabel2")
        self.supportersLabel2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.supportersLabel2)

        self.supportersLabel3 = QLabel(Supporters)
        self.supportersLabel3.setObjectName(u"supportersLabel3")
        self.supportersLabel3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.supportersLabel3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.supportersCloseButton = QPushButton(Supporters)
        self.supportersCloseButton.setObjectName(u"supportersCloseButton")

        self.verticalLayout.addWidget(self.supportersCloseButton)


        self.retranslateUi(Supporters)

        QMetaObject.connectSlotsByName(Supporters)
    # setupUi

    def retranslateUi(self, Supporters):
        Supporters.setWindowTitle(QCoreApplication.translate("Supporters", u"Supporters", None))
        self.patreonLogo.setText("")
        self.label.setText(QCoreApplication.translate("Supporters", u"Thanks to all our Patreon supporters!", None))
        self.supportersLabel1.setText("")
        self.supportersLabel2.setText("")
        self.supportersLabel3.setText("")
        self.supportersCloseButton.setText(QCoreApplication.translate("Supporters", u"Nice", None))
    # retranslateUi

