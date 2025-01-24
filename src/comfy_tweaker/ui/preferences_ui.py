# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferences.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QFrame,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QToolButton, QVBoxLayout,
    QWidget)

class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        if not PreferencesDialog.objectName():
            PreferencesDialog.setObjectName(u"PreferencesDialog")
        PreferencesDialog.resize(836, 397)
        PreferencesDialog.setStyleSheet(u"QToolTip { \n"
"                           background-color: black; \n"
"                           color: white; \n"
"                           border: black solid 1px\n"
"                           }")
        self.horizontalLayout = QHBoxLayout(PreferencesDialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(PreferencesDialog)
        self.frame.setObjectName(u"frame")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(12)
        self.frame.setFont(font)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.modelsDirectoryLineEdit = QLineEdit(self.frame)
        self.modelsDirectoryLineEdit.setObjectName(u"modelsDirectoryLineEdit")
        self.modelsDirectoryLineEdit.setReadOnly(True)

        self.horizontalLayout_10.addWidget(self.modelsDirectoryLineEdit)

        self.modelsDirectoryBrowseButton = QToolButton(self.frame)
        self.modelsDirectoryBrowseButton.setObjectName(u"modelsDirectoryBrowseButton")

        self.horizontalLayout_10.addWidget(self.modelsDirectoryBrowseButton)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_10)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.comfyUIFolderLineEdit = QLineEdit(self.frame)
        self.comfyUIFolderLineEdit.setObjectName(u"comfyUIFolderLineEdit")
        self.comfyUIFolderLineEdit.setReadOnly(True)

        self.horizontalLayout_8.addWidget(self.comfyUIFolderLineEdit)

        self.comfyUIFolderBrowseButton = QToolButton(self.frame)
        self.comfyUIFolderBrowseButton.setObjectName(u"comfyUIFolderBrowseButton")

        self.horizontalLayout_8.addWidget(self.comfyUIFolderBrowseButton)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_8)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.wildcardsDirectoryLineEdit = QLineEdit(self.frame)
        self.wildcardsDirectoryLineEdit.setObjectName(u"wildcardsDirectoryLineEdit")
        self.wildcardsDirectoryLineEdit.setReadOnly(True)

        self.horizontalLayout_11.addWidget(self.wildcardsDirectoryLineEdit)

        self.wildcardsDirectoryBrowseButton = QToolButton(self.frame)
        self.wildcardsDirectoryBrowseButton.setObjectName(u"wildcardsDirectoryBrowseButton")

        self.horizontalLayout_11.addWidget(self.wildcardsDirectoryBrowseButton)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_11)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.comfyUIServerAddressLineEdit = QLineEdit(self.frame)
        self.comfyUIServerAddressLineEdit.setObjectName(u"comfyUIServerAddressLineEdit")
        self.comfyUIServerAddressLineEdit.setReadOnly(False)

        self.horizontalLayout_14.addWidget(self.comfyUIServerAddressLineEdit)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_14)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.closeButton = QPushButton(self.frame)
        self.closeButton.setObjectName(u"closeButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closeButton.sizePolicy().hasHeightForWidth())
        self.closeButton.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout)


        self.horizontalLayout.addWidget(self.frame)


        self.retranslateUi(PreferencesDialog)

        QMetaObject.connectSlotsByName(PreferencesDialog)
    # setupUi

    def retranslateUi(self, PreferencesDialog):
        PreferencesDialog.setWindowTitle(QCoreApplication.translate("PreferencesDialog", u"Preferences", None))
        self.label_2.setText(QCoreApplication.translate("PreferencesDialog", u"Models Directory", None))
        self.modelsDirectoryBrowseButton.setText(QCoreApplication.translate("PreferencesDialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("PreferencesDialog", u"The root directory of your comfyUI installation", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("PreferencesDialog", u"ComfyUI Directory", None))
        self.comfyUIFolderBrowseButton.setText(QCoreApplication.translate("PreferencesDialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("PreferencesDialog", u"The root directory containing wildcards in the form of new line separated text files", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("PreferencesDialog", u"Wildcards Directory", None))
        self.wildcardsDirectoryBrowseButton.setText(QCoreApplication.translate("PreferencesDialog", u"...", None))
        self.comfyUIServerAddressLineEdit.setPlaceholderText(QCoreApplication.translate("PreferencesDialog", u"ip:port", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("PreferencesDialog", u"The root directory containing wildcards in the form of new line separated text files", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("PreferencesDialog", u"ComfyUI Server Address", None))
        self.closeButton.setText(QCoreApplication.translate("PreferencesDialog", u"Close", None))
    # retranslateUi

