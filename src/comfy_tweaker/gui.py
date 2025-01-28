import asyncio
import functools
import itertools
import logging
import os
import platform
import subprocess
import sys
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor
from copy import copy

# this code must be disabled when compiling with pyinstaller
# import faulthandler
# faulthandler.enable()

from loguru import logger

import qdarktheme
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QAbstractTableModel, Qt, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QInputDialog
from qasync import QEventLoop, asyncSlot, QApplication

import comfy_tweaker
from comfy_tweaker import JobQueue, JobStatus, Tweaks, Workflow
from comfy_tweaker.settings import load_settings, save_settings
from comfy_tweaker.ui.main_ui import Ui_MainWindow
from comfy_tweaker.ui.preferences_ui import Ui_PreferencesDialog
from comfy_tweaker.ui.supporters_ui import Ui_Supporters

executor = ThreadPoolExecutor()

from comfy_tweaker.comfyui import check_if_connected

class JobQueueTask(QtCore.QRunnable):
    def __init__(self, job_queue):
        super().__init__()
        self.job_queue = job_queue

    def run(self):
        if self.job_queue.mid_job:
            self.job_queue.restart()
        else:
            asyncio.run(self.job_queue.start())

class QTextEditLogger(logging.Handler):
    """Custom logging handler to redirect logs to a QTextEdit."""

    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def emit(self, record):
        # msg = self.format(record)
        msg = record.getMessage()
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(msg + "\n")
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()


SUPPORTERS = ["tohoco", "sourjck"]


class SupportersDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Supporters()
        self.ui.setupUi(self)

        label_cycle = itertools.cycle(
            [
                self.ui.supportersLabel1,
                self.ui.supportersLabel2,
                self.ui.supportersLabel3,
            ]
        )
        for supporter in SUPPORTERS:
            label = next(label_cycle)
            new_text = label.text() + f"{supporter}\n"
            label.setText(new_text)

        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "icons", "patreon.png")
        pixmap = QtGui.QPixmap(icon_path)
        pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        self.ui.patreonLogo.setPixmap(pixmap)
        clickable_elements = [
            self.ui.patreonLogo,
            self.ui.label,
            self.ui.supportersLabel1,
            self.ui.supportersLabel2,
            self.ui.supportersLabel3,
        ]
        for element in clickable_elements:
            element.setCursor(QtCore.Qt.PointingHandCursor)
            element.mousePressEvent = lambda event: QtGui.QDesktopServices.openUrl(
                QtCore.QUrl("https://www.patreon.com/comfytweaker")
            )

        self.ui.supportersCloseButton.clicked.connect(self.accept)


class PreferencesDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)

        self.ui = Ui_PreferencesDialog()
        self.ui.setupUi(self)
        self.settings = settings

        self.ui.modelsDirectoryLineEdit.setText(
            self.settings.get("models_directory", "")
        )
        self.ui.wildcardsDirectoryLineEdit.setText(
            self.settings.get("wildcards_directory", "")
        )
        self.ui.comfyUIFolderLineEdit.setText(self.settings.get("comfy_ui_folder", ""))
        self.ui.comfyUIServerAddressLineEdit.setText(
            self.settings.get("comfy_ui_server_address", "")
        )

        models_browse_handler = functools.partial(
            self.browse_for_folder, self.ui.modelsDirectoryLineEdit, "models_directory"
        )
        wildcards_browse_handler = functools.partial(
            self.browse_for_folder,
            self.ui.wildcardsDirectoryLineEdit,
            "wildcards_directory",
        )
        comfy_ui_output_browse_handler = functools.partial(
            self.browse_for_folder, self.ui.comfyUIFolderLineEdit, "comfy_ui_folder"
        )
        comfy_ui_server_address_handler = lambda: self.settings.update(
            {"comfy_ui_server_address": self.ui.comfyUIServerAddressLineEdit.text()}
        )

        self.ui.modelsDirectoryBrowseButton.clicked.connect(models_browse_handler)
        self.ui.comfyUIFolderBrowseButton.clicked.connect(
            comfy_ui_output_browse_handler
        )
        self.ui.wildcardsDirectoryBrowseButton.clicked.connect(wildcards_browse_handler)
        self.ui.comfyUIServerAddressLineEdit.textChanged.connect(
            comfy_ui_server_address_handler
        )

        self.ui.closeButton.clicked.connect(self.reject)

    def browse_for_folder(self, line_edit, settings_key):
        logger.info(f"Browsing for f{settings_key} folder..")
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Folder", dir=self.settings.get(settings_key, "")
        )
        if folder_path:
            self.settings[settings_key] = folder_path
            line_edit.setText(folder_path)
            save_settings(self.settings)


class JobTableModel(QAbstractTableModel):
    def __init__(self, job_queue=None):
        super(JobTableModel, self).__init__()
        self.job_queue = job_queue
        self.jobs = job_queue.all_jobs or []

    def rowCount(self, parent=None):
        return len(self.jobs)

    def columnCount(self, parent=None):
        return 6  # Updated to 6 columns: Icon, Position, Amount, Progress, Workflow Name, Tweaks Name

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "#"
                elif section == 1:
                    return ""
                elif section == 2:
                    return "Amount"
                elif section == 3:
                    return "Remaining"
                elif section == 4:
                    return "Workflow"
                elif section == 5:
                    return "Tweaks"
        return None

    def data(self, index, role):
        if not index.isValid():
            return None

        job = self.jobs[index.row()]

        if role == Qt.DisplayRole:
            if index.column() == 0:
                if self.job_queue.position_of(job.id):
                    return self.job_queue.position_of(
                        job.id
                    )  # Position in the job queue
                else:
                    return ""
            elif index.column() == 2:
                return job.amount  # Job amount
            elif index.column() == 3:
                return job.remaining  # Job progress
            elif index.column() == 4:
                return job.original_workflow.name
            elif index.column() == 5:
                return job.tweaks.name

        if role == Qt.DecorationRole and index.column() == 1:
            return self.create_job_icon(job)

        return None

    def create_job_icon(self, job):
        status = str(job.status.value).lower()
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "icons", f"{status}.png")
        icon = QtGui.QIcon(icon_path)
        return icon

    def setModel(self, model):
        super().setModel(model)

    def set_jobs(self, jobs):
        self.beginResetModel()
        self.jobs = jobs
        self.endResetModel()

    def updateData(self, updates):
        """
        Updates specific data cells without resetting the model.
        `updates` is a list of tuples: [(row, column, value), ...]
        """
        for row, col, value in updates:
            index = self.index(row, col)
            self.setData(index, value, Qt.EditRole)
        self.layoutChanged.emit()


class TweakerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.settings = load_settings()
        self.update_environment_variables()
        self.job_queue = JobQueue()
        self.setAcceptDrops(True)
        self.current_tweaks = Tweaks(name="No Tweaks")
        # self.ui.queueStopButton.setEnabled(False)
        self.drop_label = QtWidgets.QLabel(self)
        self.drop_label.setAlignment(Qt.AlignCenter)
        # self.drop_label.setPixmap(QtGui.QtPixmap(":/icons/plus_icon.png"))
        self.drop_label.setStyleSheet("background-color: gray;")
        self.drop_label.setGeometry(self.rect())
        self.drop_label.hide()
        # we have to start at 1 or the progress bar will be in an
        # indeterminate state on launch, which looks ugly
        self.starting_job_count = 1
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "icons", "window.png")
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.update_job_table_lock = threading.Lock()
        self.setWindowTitle(f"Comfy Tweaker {comfy_tweaker.__version__}")

        # Set up logging
        log_handler = QTextEditLogger(self.ui.logTextEdit)
        # Redirect stdout to logger and console
        # We'll change this back when we find a way to print to both console and our app
        # sys.stdout = StreamToLogger(logging.getLogger(), logging.INFO)
        log_format = "{time:MM/DD/YYYY HH:mm:ss} - {level} - {message}"
        logger.add(log_handler, format=log_format, level="INFO")
        self.ui.queueStartButton.clicked.connect(self.handle_start_queue)
        logger.info("Application successfully started")

        # Connect workflowBrowseButton to the file browse function
        self.ui.workflowBrowseButton.clicked.connect(self.browse_and_load_image)
        self.ui.tweaksFileBrowseButton.clicked.connect(self.browse_and_load_tweaks_file)
        self.ui.saveAsButton.clicked.connect(self.save_workflow_as)
        self.ui.validateButton.clicked.connect(self.validate_tweaks)
        self.ui.addJobButton.clicked.connect(self.add_job)
        self.ui.tweaksClearButton.clicked.connect(
            lambda: self.ui.tweaksFileLineEdit.setText("")
        )
        self.ui.tweaksFileLineEdit.textChanged.connect(self.set_current_tweaks)

        self.ui.jobFilter.textChanged.connect(self.update_job_table)

        self.ui.actionSupporters.triggered.connect(self.show_supporters)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionPreferences.triggered.connect(self.open_preferences)

        self.ui.jobTable.setEditTriggers(
            QtWidgets.QTableWidget.EditTrigger.NoEditTriggers
        )
        self.populate_defaults()

        self.ui.queueStopButton.clicked.connect(self.stop_queue)

        # Set up a QTimer to call update_job_table regularly
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_job_table)
        self.timer.start(1000)

        # # Set up a QTimer to call update_job_table regularly
        # self.comfyui_timer = QTimer(self)
        # self.comfyui_timer.timeout.connect(self.update_comfyui_connected)
        # self.comfyui_timer.start(2000)  # Update every 5 seconds
        # self.update_comfyui_connected()
        self.ui.comfyUIConnectedLabel.setText("")

        self.image_generation_preview_timer = QTimer(self)
        self.image_generation_preview_timer.timeout.connect(
            self.update_image_generation_preview
        )
        self.image_generation_preview_timer.start(1000)

        # Create and set the model
        self.jobTableModel = JobTableModel(job_queue=self.job_queue)
        self._last_length = 0
        self.ui.jobTable.setModel(self.jobTableModel)
        self.ui.jobTable.setColumnWidth(0, 25)
        self.ui.jobTable.setColumnWidth(1, 40)
        self.ui.jobTable.setColumnWidth(2, 60)  # Set column width for Amount
        self.ui.jobTable.setColumnWidth(3, 80)  # Set column width for Progress
        self.update_job_table()

        # Add context menu to jobTable
        self.ui.jobTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.jobTable.customContextMenuRequested.connect(
            self.show_job_table_context_menu
        )

        try:
            self.set_current_workflow()
        except Exception as e:
            self.clear_workflow_image()

        try:
            self.set_current_tweaks()
        except Exception as e:
            self.clear_tweaks_file()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.drop_label.show()

    def dragLeaveEvent(self, event):
        self.drop_label.hide()

    @asyncSlot()
    async def handle_start_queue(self):
        await self.start_queue()

    def dropEvent(self, event):
        self.drop_label.hide()
        yaml_files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(".png"):
                self.load_image(file_path)
                return
            if file_path.lower().endswith(".yaml"):
                yaml_files.append(file_path)
        
        if len(yaml_files) == 1:
            self.load_tweaks_file(yaml_files[0])
        elif len(yaml_files) > 1:
            self.load_yaml_batch(yaml_files)

    def load_yaml_batch(self, yaml_files):
        for yaml_file in yaml_files:
            self.load_tweaks_file(yaml_file)
            self.add_job()

    def clear_tweaks_file(self):
        self.ui.tweaksFileLineEdit.setText("")

    def clear_workflow_image(self):
        self.ui.workflowLineEdit.setText("")

    def show_job_table_context_menu(self, position):
        index = self.ui.jobTable.indexAt(position)
        menu = QtWidgets.QMenu()
        menu.setFixedWidth(250)
        if index.isValid():
            selected_indexes = self.ui.jobTable.selectionModel().selectedIndexes()
            if len(selected_indexes) == 1:
                job = self.jobTableModel.jobs[selected_indexes[0].row()]
                if job.output_location:
                    go_to_folder_action = menu.addAction("Go to Folder")
                    go_to_folder_action.triggered.connect(
                        functools.partial(
                            self.go_to_folder, os.path.dirname(job.output_location)
                        )
                    )
            remove_action = menu.addAction("Remove")
            remove_action.triggered.connect(self.remove_selected_jobs)
            duplicate_action = menu.addAction("Duplicate")
            duplicate_action.triggered.connect(self.duplicate_selected_jobs)
            move_to_front_action = menu.addAction("Move to Front")
            move_to_front_action.triggered.connect(self.move_selected_jobs_to_front)

        menu.addSeparator()

        refresh_action = menu.addAction("Refresh")
        refresh_action.triggered.connect(
            functools.partial(self.update_job_table, reset=True)
        )

        menu.addSeparator()

        clear_action = menu.addAction("Clear All")
        clear_action.triggered.connect(self.clear_job_queue)
        menu.exec(self.ui.jobTable.viewport().mapToGlobal(position))

    def go_to_folder(self, folder_path):
        if os.path.isdir(folder_path):
            if platform.system() == "Windows":
                os.startfile(folder_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", folder_path])
            else:  # Linux and other Unix-like systems
                subprocess.Popen(["xdg-open", folder_path])

    def move_selected_jobs_to_front(self):
        selected_indexes = self.ui.jobTable.selectionModel().selectedIndexes()
        rows = sorted(set(index.row() for index in selected_indexes), reverse=True)
        for row in rows:
            job = self.jobTableModel.jobs[row]
            self.job_queue.queue.remove(job)
            self.job_queue.queue.insert(0, job)
        self.update_job_table()

    def duplicate_selected_jobs(self):
        selected_indexes = self.ui.jobTable.selectionModel().selectedIndexes()
        rows = set(index.row() for index in selected_indexes)
        for row in sorted(rows):
            job = copy(self.jobTableModel.jobs[row])
            self.job_queue.add(job.workflow, job.tweaks, job.amount, validate=False)
        self.update_job_table(reset=True)

    def remove_selected_jobs(self):
        selected_indexes = self.ui.jobTable.selectionModel().selectedIndexes()
        rows = set(index.row() for index in selected_indexes)
        for row in sorted(rows, reverse=True):
            self.job_queue.remove(self.jobTableModel.jobs[row].id)
        logger.info(f"Removed {len(rows)} jobs.")
        self.update_job_table()

    def clear_job_queue(self):
        self.job_queue.clear()
        self.update_job_table()

    def stop_queue(self):
        logger.info("Stopping the job queue after finishing current job...")
        self.job_queue.stop()
        # self.ui.queueStopButton.setEnabled(False)

    # @asyncSlot()
    # async def update_comfyui_connected(self):
    #     """If we're connected, enable start button, otherwise disable."""
    #     try:
    #         connected = await check_if_connected()
    #     except RuntimeError as e:
    #         if "no running event loop" in str(e).lower():
    #             return
    #         else:
    #             raise e
    #     if connected:
    #         self.ui.comfyUIConnectedLabel.setText("ComfyUI Connected")
    #         self.ui.queueStartButton.setEnabled(True)
    #     else:
    #         self.ui.comfyUIConnectedLabel.setText("ComfyUI Not Connected")
    #         self.ui.queueStartButton.setEnabled(False)

    def validate_comfyui_folder(self):
        logger.debug("Validating comfyui folder...")
        comfyui_folder = self.settings.get("comfy_ui_folder")
        if not os.path.exists(os.path.join(comfyui_folder, "output")) or not os.path.exists(
            os.path.join(comfyui_folder, "input")
        ):
            QMessageBox.critical(
                self,
                "Invalid ComfyUI Folder",
                "The comfyui folder does not contain the expected 'output' and 'input' folders.",
            )
            raise ValueError(
                "The comfyui folder does not contain the output and input folders."
            )
        if not comfyui_folder:
            raise ValueError("ComfyUI folder is not set.")

    async def start_queue(self):
        logger.info("Starting the job queue...")
        logger.info("Checking for comfyui connection...")
        connected = await check_if_connected()
        if not connected:
            QMessageBox.critical(
                self,
                "ComfyUI Not Connected",
                "Could not connect to comfyui server. Please check your cormfyui server address in preferences.",
            )
            return
        self.update_environment_variables()
        self.validate_comfyui_folder()
        if not self.job_queue.queue:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("No jobs in the queue.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.show()
            return
        self.starting_job_count = len(self.job_queue.queue)
        self.update_progress_bar()
        # self.ui.queueStopButton.setEnabled(True)
        if not self.job_queue.mid_job:
            logger.debug("Starting job queue...")
            await self.job_queue.start()
        else:
            logger.debug("Restarting job queue...")
            self.job_queue.restart()

        # self.ui.queueStopButton.setEnabled(False)

    def update_progress_bar(self):
        if len(self.job_queue.all_jobs) == 0:
            self.ui.progressBar.setMaximum(1)
            self.ui.progressBar.setValue(0)
        else:
            progress = sum(job.progress for job in self.job_queue.all_jobs)
            amount = sum(job.amount for job in self.job_queue.all_jobs)
            self.ui.progressBar.setMaximum(amount)
            self.ui.progressBar.setValue(progress)

    def update_environment_variables(self):
        logger.debug("Updating environment variables with UI settings...")
        os.environ["MODELS_FOLDER"] = self.settings.get("models_directory", "")
        os.environ["WILDCARDS_DIRECTORY"] = self.settings.get("wildcards_directory", "")
        if self.settings.get("comfy_ui_folder"):
            os.environ["COMFYUI_OUTPUT_FOLDER"] = os.path.join(
                self.settings.get("comfy_ui_folder", ""), "output"
            )
            os.environ["COMFYUI_INPUT_FOLDER"] = os.path.join(
                self.settings.get("comfy_ui_folder", ""), "input"
            )
        os.environ["COMFYUI_SERVER_ADDRESS"] = self.settings.get(
            "comfy_ui_server_address", ""
        )

    def show_supporters(self):
        dialog = SupportersDialog(self)
        dialog.exec()

    def open_preferences(self):
        dialog = PreferencesDialog(self, self.settings)
        dialog.exec()

    def populate_defaults(self):
        self.ui.workflowLineEdit.setText(self.settings.get("workflow_image", ""))
        self.ui.tweaksFileLineEdit.setText(self.settings.get("tweaks_file", ""))
        self.update_image_preview()

    def update_image_generation_preview(self):
        if self.job_queue.running:
            try:
                image_bytes = self.job_queue.queue[0].preview_image
                if image_bytes:
                    pixmap = QtGui.QPixmap()
                    if pixmap.loadFromData(image_bytes):
                        pixmap = pixmap.scaled(250, 250, QtCore.Qt.KeepAspectRatio)
                        self.ui.imageGenerationPreview.setPixmap(pixmap)
                    else:
                        # Handle the case where pixmap loading fails
                        logger.info("Failed to load pixmap from image bytes")
            except IndexError:
                pass

    def update_image_preview(self):
        file_path = self.ui.workflowLineEdit.text()
        if file_path:
            pixmap = QtGui.QPixmap(file_path).scaled(
                250, 250, QtCore.Qt.KeepAspectRatio
            )
            self.ui.imagePreview.setPixmap(pixmap)

    def update_job_table(self, reset=False):
        jobs = self.job_queue.all_jobs
        filtered_jobs = sorted(
            [
                job
                for job in jobs
                if self.ui.jobFilter.text()
                in job.original_workflow.name + job.tweaks.name
            ],
            key=lambda job: self.job_queue.position_of(job.id) or float("inf"),
        )
        # Update the model data
        updates = []
        for row, job in enumerate(filtered_jobs):
            updates.append(
                (
                    row,
                    0,
                    (
                        self.job_queue.position_of(job.id)
                        if self.job_queue.position_of(job.id)
                        else ""
                    ),
                )
            )
            updates.append((row, 2, job.original_workflow.name))
            updates.append((row, 3, job.tweaks.name))
        self.jobTableModel.updateData(updates)

        if len(filtered_jobs) != self._last_length or reset:
            self.jobTableModel.set_jobs(filtered_jobs)
            self._last_length = len(filtered_jobs)
        self.update_progress_bar()

    def add_job(self):
        try:
            # we validate here once so adding a bunch of jobs is quick
            self.job_queue.add(
                self.current_workflow,
                self.current_tweaks,
                self.ui.amountSpinBox.value(),
            )
            self.update_job_table()
            logger.info(
                f"{self.job_queue.queue[-1].workflow.name} with {self.job_queue.queue[-1].tweaks.name} added to the queue."
            )
        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(self, "Tweaks Error", error_message)

    def set_current_workflow(self):
        path = self.ui.workflowLineEdit.text()
        self.current_workflow = Workflow.from_image(path, name=os.path.basename(path))
        self.update_image_preview()

    def set_current_tweaks(self):
        path = self.ui.tweaksFileLineEdit.text()
        if path:
            self.current_tweaks = Tweaks.from_file(path, name=os.path.basename(path))
        else:
            self.current_tweaks = Tweaks(name="No Tweaks")

    def validate_tweaks(self):
        if len(self.current_tweaks) == 0:
            QMessageBox.critical(self, "Tweaks Error", "Tweaks file seems to be empty. No tweaks to validate.")
            return
        try:
            self.set_current_tweaks()
            self.current_workflow.validate(self.current_tweaks)
            # TODO: We need a way to check how many changes were successfully validated
            QMessageBox.information(
                self, "Success", f"Successfully validated {len(self.current_tweaks)} tweaks in this workflow."
            )
        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(self, "Tweaks Error", error_message)

    def save_workflow_as(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Workflow As",
            self.settings.get("workflow_folder", ""),
            "JSON Files (*.json)",
        )
        if file_path:
            tweaked_workflow = self.current_workflow.apply_tweaks(self.current_tweaks)
            tweaked_workflow.save(file_path)
            self.settings["workflow_folder"] = file_path

    def browse_and_load_tweaks_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select YAML File",
            self.settings.get("tweaks_file", ""),
            "YAML Files (*.yaml)",
        )
        if file_path:
            self.load_tweaks_file(file_path)

    def load_tweaks_file(self, file_path):
        try:
            self.settings["tweaks_file"] = file_path
            self.ui.tweaksFileLineEdit.setText(file_path)
        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(self, "Error", error_message)

    def browse_and_load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select PNG File",
            self.settings.get("workflow_image", ""),
            "PNG Files (*.png)",
        )
        if file_path:
            self.load_image(file_path)

    def load_image(self, file_path):
        try:
            # we run this without using anything so it throws an error if the image is invalid
            Workflow.from_image(file_path)
            self.ui.workflowLineEdit.setText(file_path)
            self.settings["workflow_image"] = file_path
            self.set_current_workflow()
        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(self, "Error", error_message)

    def closeEvent(self, event):
        reply = QMessageBox.critical(
            self,
            "Confirm Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            # Save settings when the application is closed
            save_settings(self.settings)
            event.accept()
        else:
            event.ignore()


async def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    qdarktheme.setup_theme()

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    window = TweakerApp()
    window.show()

    with loop:
        loop.run_until_complete(app_close_event.wait())


def entry():
    data_dir = user_data_dir("ComfyTweaker", "ComfyTweaker", roaming=True)
    # File handler with DEBUG level
    log_file_path = os.path.join(data_dir, "logs/comfytweaker_{time}.log")
    logger.add(log_file_path, level="DEBUG")

    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Exception occurred: {e}")
        logger.critical(traceback.format_exc())


from appdirs import user_data_dir

if __name__ == "__main__":
    entry()
