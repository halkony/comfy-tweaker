# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tweaker.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QSpinBox, QStatusBar,
    QTableView, QTextEdit, QToolButton, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1090, 859)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionPreferences = QAction(MainWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.actionSupporters = QAction(MainWindow)
        self.actionSupporters.setObjectName(u"actionSupporters")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.widget_2.setStyleSheet(u"QToolTip { \n"
"                           background-color: black; \n"
"                           color: white; \n"
"                           border: black solid 1px\n"
"                           }")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(self.widget_2)
        self.frame.setObjectName(u"frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setMinimumSize(QSize(250, 300))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.imagePreview = QLabel(self.frame)
        self.imagePreview.setObjectName(u"imagePreview")
        sizePolicy2.setHeightForWidth(self.imagePreview.sizePolicy().hasHeightForWidth())
        self.imagePreview.setSizePolicy(sizePolicy2)
        self.imagePreview.setMinimumSize(QSize(250, 250))
        self.imagePreview.setBaseSize(QSize(250, 250))

        self.verticalLayout_7.addWidget(self.imagePreview)

        self.imageGenerationPreview = QLabel(self.frame)
        self.imageGenerationPreview.setObjectName(u"imageGenerationPreview")
        sizePolicy2.setHeightForWidth(self.imageGenerationPreview.sizePolicy().hasHeightForWidth())
        self.imageGenerationPreview.setSizePolicy(sizePolicy2)
        self.imageGenerationPreview.setMinimumSize(QSize(250, 250))
        self.imageGenerationPreview.setBaseSize(QSize(250, 250))
        self.imageGenerationPreview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.imageGenerationPreview)


        self.horizontalLayout.addWidget(self.frame)

        self.widget = QWidget(self.widget_2)
        self.widget.setObjectName(u"widget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy3)
        self.widget.setMinimumSize(QSize(200, 0))
        self.verticalLayout_6 = QVBoxLayout(self.widget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setScaledContents(False)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.workflowLineEdit = QLineEdit(self.widget)
        self.workflowLineEdit.setObjectName(u"workflowLineEdit")
        self.workflowLineEdit.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.workflowLineEdit)

        self.workflowBrowseButton = QToolButton(self.widget)
        self.workflowBrowseButton.setObjectName(u"workflowBrowseButton")

        self.horizontalLayout_5.addWidget(self.workflowBrowseButton)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_5)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setScaledContents(False)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tweaksFileLineEdit = QLineEdit(self.widget)
        self.tweaksFileLineEdit.setObjectName(u"tweaksFileLineEdit")
        self.tweaksFileLineEdit.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.tweaksFileLineEdit)

        self.tweaksClearButton = QPushButton(self.widget)
        self.tweaksClearButton.setObjectName(u"tweaksClearButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.tweaksClearButton.sizePolicy().hasHeightForWidth())
        self.tweaksClearButton.setSizePolicy(sizePolicy4)
        self.tweaksClearButton.setFont(font)

        self.horizontalLayout_2.addWidget(self.tweaksClearButton)

        self.tweaksFileBrowseButton = QToolButton(self.widget)
        self.tweaksFileBrowseButton.setObjectName(u"tweaksFileBrowseButton")

        self.horizontalLayout_2.addWidget(self.tweaksFileBrowseButton)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_2)


        self.verticalLayout_6.addLayout(self.formLayout)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.validateButton = QPushButton(self.widget)
        self.validateButton.setObjectName(u"validateButton")

        self.horizontalLayout_7.addWidget(self.validateButton)

        self.saveAsButton = QPushButton(self.widget)
        self.saveAsButton.setObjectName(u"saveAsButton")

        self.horizontalLayout_7.addWidget(self.saveAsButton)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.jobTable = QTableView(self.widget)
        self.jobTable.setObjectName(u"jobTable")
        self.jobTable.setSortingEnabled(False)
        self.jobTable.horizontalHeader().setHighlightSections(False)
        self.jobTable.horizontalHeader().setStretchLastSection(True)
        self.jobTable.verticalHeader().setVisible(False)

        self.verticalLayout_5.addWidget(self.jobTable)

        self.progressBar = QProgressBar(self.widget)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy5)
        self.progressBar.setValue(0)

        self.verticalLayout_5.addWidget(self.progressBar)


        self.horizontalLayout_6.addLayout(self.verticalLayout_5)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.jobFilter = QLineEdit(self.widget)
        self.jobFilter.setObjectName(u"jobFilter")
        sizePolicy5.setHeightForWidth(self.jobFilter.sizePolicy().hasHeightForWidth())
        self.jobFilter.setSizePolicy(sizePolicy5)
        self.jobFilter.setMinimumSize(QSize(80, 0))

        self.verticalLayout_4.addWidget(self.jobFilter)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.amountLabel_2 = QLabel(self.widget)
        self.amountLabel_2.setObjectName(u"amountLabel_2")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.amountLabel_2.sizePolicy().hasHeightForWidth())
        self.amountLabel_2.setSizePolicy(sizePolicy6)
        self.amountLabel_2.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_4.addWidget(self.amountLabel_2)

        self.amountSpinBox = QSpinBox(self.widget)
        self.amountSpinBox.setObjectName(u"amountSpinBox")
        sizePolicy2.setHeightForWidth(self.amountSpinBox.sizePolicy().hasHeightForWidth())
        self.amountSpinBox.setSizePolicy(sizePolicy2)
        self.amountSpinBox.setMinimumSize(QSize(80, 0))
        self.amountSpinBox.setMinimum(1)
        self.amountSpinBox.setMaximum(9999)

        self.horizontalLayout_4.addWidget(self.amountSpinBox)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.addJobButton = QPushButton(self.widget)
        self.addJobButton.setObjectName(u"addJobButton")
        sizePolicy5.setHeightForWidth(self.addJobButton.sizePolicy().hasHeightForWidth())
        self.addJobButton.setSizePolicy(sizePolicy5)
        self.addJobButton.setMinimumSize(QSize(80, 0))

        self.verticalLayout_4.addWidget(self.addJobButton)

        self.comfyUIConnectedLabel = QLabel(self.widget)
        self.comfyUIConnectedLabel.setObjectName(u"comfyUIConnectedLabel")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.comfyUIConnectedLabel.sizePolicy().hasHeightForWidth())
        self.comfyUIConnectedLabel.setSizePolicy(sizePolicy7)
        self.comfyUIConnectedLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.comfyUIConnectedLabel)

        self.queueStartButton = QPushButton(self.widget)
        self.queueStartButton.setObjectName(u"queueStartButton")
        self.queueStartButton.setEnabled(False)
        sizePolicy5.setHeightForWidth(self.queueStartButton.sizePolicy().hasHeightForWidth())
        self.queueStartButton.setSizePolicy(sizePolicy5)
        self.queueStartButton.setMinimumSize(QSize(80, 0))

        self.verticalLayout_4.addWidget(self.queueStartButton)

        self.queueStopButton = QPushButton(self.widget)
        self.queueStopButton.setObjectName(u"queueStopButton")
        sizePolicy5.setHeightForWidth(self.queueStopButton.sizePolicy().hasHeightForWidth())
        self.queueStopButton.setSizePolicy(sizePolicy5)
        self.queueStopButton.setMinimumSize(QSize(80, 0))

        self.verticalLayout_4.addWidget(self.queueStopButton)


        self.horizontalLayout_6.addLayout(self.verticalLayout_4)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)


        self.horizontalLayout.addWidget(self.widget)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.logTextEdit = QTextEdit(self.widget_2)
        self.logTextEdit.setObjectName(u"logTextEdit")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.logTextEdit.sizePolicy().hasHeightForWidth())
        self.logTextEdit.setSizePolicy(sizePolicy8)
        self.logTextEdit.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.logTextEdit)


        self.verticalLayout.addWidget(self.widget_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1090, 21))
        self.menubar.setStyleSheet(u"QMenuBar {\n"
"        spacing: 10px;\n"
"    }")
        self.menubar.setDefaultUp(False)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionPreferences)
        self.menuEdit.addSeparator()
        self.menuAbout.addAction(self.actionSupporters)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ComfyTweaker", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionPreferences.setText(QCoreApplication.translate("MainWindow", u"Preferences", None))
        self.actionSupporters.setText(QCoreApplication.translate("MainWindow", u"Supporters", None))
#if QT_CONFIG(tooltip)
        self.imagePreview.setToolTip(QCoreApplication.translate("MainWindow", u"The directory containings your ComfyUI models", None))
#endif // QT_CONFIG(tooltip)
        self.imagePreview.setText("")
        self.imageGenerationPreview.setText(QCoreApplication.translate("MainWindow", u"Start a job to see an image preview.", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("MainWindow", u"An image containing a workflow", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Workflow Image", None))
#if QT_CONFIG(tooltip)
        self.workflowBrowseButton.setToolTip(QCoreApplication.translate("MainWindow", u"Browse for an image containing your workflow", None))
#endif // QT_CONFIG(tooltip)
        self.workflowBrowseButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("MainWindow", u"A yaml file containing tweaks", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Tweaks File", None))
        self.tweaksClearButton.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
#if QT_CONFIG(tooltip)
        self.tweaksFileBrowseButton.setToolTip(QCoreApplication.translate("MainWindow", u"Browse for Tweaks yaml file", None))
#endif // QT_CONFIG(tooltip)
        self.tweaksFileBrowseButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.validateButton.setToolTip(QCoreApplication.translate("MainWindow", u"Validate that the tweaks files can be applied to the workflow", None))
#endif // QT_CONFIG(tooltip)
        self.validateButton.setText(QCoreApplication.translate("MainWindow", u"Validate", None))
#if QT_CONFIG(tooltip)
        self.saveAsButton.setToolTip(QCoreApplication.translate("MainWindow", u"Save the tweaked workflow as a JSON", None))
#endif // QT_CONFIG(tooltip)
        self.saveAsButton.setText(QCoreApplication.translate("MainWindow", u"Save As...", None))
#if QT_CONFIG(tooltip)
        self.jobFilter.setToolTip(QCoreApplication.translate("MainWindow", u"Filter the current jobs", None))
#endif // QT_CONFIG(tooltip)
        self.jobFilter.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Filter...", None))
        self.amountLabel_2.setText(QCoreApplication.translate("MainWindow", u"Amount", None))
#if QT_CONFIG(tooltip)
        self.amountSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"How many images to generate with a tweaked workflow", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.addJobButton.setToolTip(QCoreApplication.translate("MainWindow", u"Add a job to the queue", None))
#endif // QT_CONFIG(tooltip)
        self.addJobButton.setText(QCoreApplication.translate("MainWindow", u"Add Job", None))
        self.comfyUIConnectedLabel.setText(QCoreApplication.translate("MainWindow", u"Connecting...", None))
#if QT_CONFIG(tooltip)
        self.queueStartButton.setToolTip(QCoreApplication.translate("MainWindow", u"Start the queue", None))
#endif // QT_CONFIG(tooltip)
        self.queueStartButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
#if QT_CONFIG(tooltip)
        self.queueStopButton.setToolTip(QCoreApplication.translate("MainWindow", u"Stop the queue after the current image is finished generating", None))
#endif // QT_CONFIG(tooltip)
        self.queueStopButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi

