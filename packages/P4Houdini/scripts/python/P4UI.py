"""
This is UI code only.
"""

import re

import hou  # pylint: disable=E0401
import P4Messages
import P4Utils
from hutil.Qt import QtCore  # type: ignore pylint: disable=E0401,E0611
from hutil.Qt import QtGui  # type: ignore pylint: disable=E0401,E0611
from hutil.Qt import QtWidgets  # type: ignore pylint: disable=E0401,E0611

PLUGIN_NAME = "P4Houdini"


def P4Prompt(message):
    messagebox = QtWidgets.QMessageBox()
    messagebox.setIconPixmap(
        QtGui.QPixmap(
            hou.text.expandString(str="$P4HOUDINI/help/icons/perforce-icon.svg")  # type: ignore
        )
    )
    messagebox.setText(message)
    messagebox.setWindowTitle(PLUGIN_NAME)
    messagebox.setStandardButtons(
        QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
    )

    value = messagebox.exec()
    if value == QtWidgets.QMessageBox.Ok:
        return True
    return False


def P4ChooseYesNo(message):
    messagebox = QtWidgets.QMessageBox()
    messagebox.setIconPixmap(
        QtGui.QPixmap(
            hou.text.expandString(str="$P4HOUDINI/help/icons/perforce-icon.svg")  # type: ignore
        )
    )
    messagebox.setText(message)
    messagebox.setWindowTitle(PLUGIN_NAME)
    messagebox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

    value = messagebox.exec()
    if value == QtWidgets.QMessageBox.Yes:
        return True
    return False


def P4Message(message):
    messagebox = QtWidgets.QMessageBox()
    messagebox.setIconPixmap(
        QtGui.QPixmap(
            hou.text.expandString(str="$P4HOUDINI/help/icons/perforce-icon.svg")  # type: ignore
        )
    )
    messagebox.setText(message)
    messagebox.setWindowTitle(PLUGIN_NAME)
    messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    messagebox.exec()


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    """
    return [atoi(c) for c in re.split(r"(\d+)", text)]


def natural_keys_2nd_element(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    """
    return [atoi(c) for c in re.split(r"(\d+)", text[1])]


class P4HoudiniChangeListChooser(QtWidgets.QDialog):
    """
    UI for letting user pick the changelist they wish to use.
    """

    def __init__(self, parent, plugin, mode, *args):
        super().__init__(parent)
        self.plugin = plugin
        self.mode = mode
        self.proposed_files_to_add = [] if len(args) == 0 else args[0]
        self.start_checklist = None if len(args) < 2 else args[1]
        self.files_to_add = []
        self.state = False
        self.cl_description = ""
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.selected_changelist = None
        self.available_cl = []
        self.available_cl_id = []

        self.buildUI()
        self.resize(self.minimumSizeHint())

    def closeEvent(self, event):
        pass

    def on_accept(self):
        if self.mode == "submit":
            changelist = self.selected_changelist
            if changelist:
                left = self.listwidget.count()
                for i in range(self.listwidget.count()):
                    item = self.listwidget.item(i)
                    if item.checkState() != QtCore.Qt.Checked:
                        file = item.text().split(" - ")[-1]
                        left -= 1
                        self.plugin.move_file_to_changelist(file, "default")
                if left > 0:
                    self.plugin.set_changelist_description(
                        changelist, self.changelist_desc.toPlainText()
                    )
                    self.plugin.submit_changelist(changelist, left)
        elif self.mode == "add":
            to_add = []
            for i in range(self.addwidget.count()):
                item = self.addwidget.item(i)
                if item.checkState() == QtCore.Qt.Checked:
                    to_add.append(item.text())
            self.files_to_add = to_add
            self.cl_description = self.changelist_desc.toPlainText()
        elif self.mode == "edit":
            self.cl_description = self.changelist_desc.toPlainText()

        self.state = True
        self.close()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.ContextMenu and source is self.addwidget:
            menu = QtWidgets.QMenu()
            menu.addAction("Make Writeable")
            item = source.itemAt(event.pos())

            if item:
                if menu.exec_(event.globalPos()):
                    file = item.text()
                    self.plugin.make_file_writeable(file)
                    icon = QtGui.QIcon(
                        hou.text.expandString(
                            str="$P4HOUDINI/misc/p4icons/writeable.png"  # type: ignore
                        )
                    )
                    item.setIcon(icon)
                    item.setCheckState(QtCore.Qt.Unchecked)

            return True
        return super().eventFilter(source, event)

    def on_cancel(self):
        self.selected_changelist = None
        self.files_to_add = []
        self.state = False
        self.close()

    def construct_changelist_descriptions(self):
        existing = self.plugin.get_pending_changelists()
        added = []
        added_id = []

        if self.mode == "add":
            added.append(self.plugin.preferences.P4CL_Default)
            added_id.append(self.plugin.preferences.P4CL_Default)
            added.append("New Changelist...")
            added_id.append(-1)

        for change in existing:
            if change["change"] not in added:
                value = change["change"].strip()
                added_id.append(int(value))
                _desc = change["desc"].strip().split("\n")[0]
                value += " - " + _desc  # [:30]
                added.append(value)

        self.available_cl = added
        self.available_cl_id = added_id
        return

    def on_chosen_changelist_changed(self):
        _index = self.changelist_dropdown.currentIndex()
        if _index == -1:
            return
        self.selected_changelist = self.available_cl_id[_index]

        self.update_file_dropdown()
        self.update_cldesc_dropdown()

    def update_cldesc_dropdown(self):
        self.changelist_desc.clear()
        _description = self.plugin.get_description_of_changelist(
            self.selected_changelist
        )
        self.changelist_desc.insertPlainText(str(_description))

    def update_file_dropdown(self):
        self.listwidget.clear()
        if isinstance(self.selected_changelist, int):
            changelist = self.selected_changelist
        else:
            changelist = self.plugin.find_changelist_by_description(
                self.selected_changelist
            )

        if not changelist or changelist == -1:
            return

        modifications = self.plugin.get_files_in_changelist(changelist)
        modifications.sort(key=natural_keys_2nd_element)

        for action, file, _ in modifications:
            item = QtWidgets.QListWidgetItem()
            item.setText(f"{file}")

            formatting = self.detect_status_submit(action)
            item.setIcon(formatting[0])
            item.setToolTip(formatting[1])

            if self.mode == "submit":
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Checked)
            self.listwidget.addItem(item)

    def detect_status_add(self, file_status):
        """
        Determine the icon and tooltip based on pre-fetched status data.
        Adjust logic to accurately reflect file check-out needs.
        """
        # Default icon when no specific conditions are met
        icon = QtGui.QIcon(
            hou.text.expandString(str="$P4HOUDINI/misc/p4icons/empty.png")  # type: ignore
        )
        tooltip = ""

        if not file_status.get("tracked"):
            icon = QtGui.QIcon(
                hou.text.expandString(str="$P4HOUDINI/misc/p4icons/add_self_user.png")  # type: ignore
            )
            tooltip = "File not tracked or other error"
        elif file_status.get("status"):
            status_info = file_status.get("status")

            # File is in sync and not checked out at all (not opened)
            if not status_info.get("edited_by_self"):
                icon = QtGui.QIcon(
                    hou.text.expandString(
                        str="$P4HOUDINI/misc/p4icons/lock_self_user.png"  # type: ignore
                    )
                )
                tooltip = "File is not checked out"

            # Check if the file is out of sync
            if not file_status.get("is_in_sync"):
                icon = QtGui.QIcon(
                    hou.text.expandString(str="$P4HOUDINI/misc/p4icons/unsynced.png")  # type: ignore
                )
                tooltip = "File is out of sync"

            # Check if the file is checked out by another user
            if file_status.get("checked_out_by_others"):
                other_user = status_info["otherOpen"][0]
                icon = QtGui.QIcon(
                    hou.text.expandString(
                        str="$P4HOUDINI/misc/p4icons/lock_other_user.png"  # type: ignore
                    )
                )
                tooltip = f"Checked out by {other_user}"

        return [icon, tooltip]

    def detect_status_submit(self, action):
        icon = hou.text.expandString(str="$P4HOUDINI/misc/p4icons/empty.png")  # type: ignore
        tooltip = ""

        if not self.plugin.preferences.P4CL_Icons:
            return [QtGui.QIcon(icon), tooltip]

        if action == "add":
            icon = hou.text.expandString(
                str="$P4HOUDINI/misc/p4icons/add_self_user.png"  # type: ignore
            )
            tooltip = "File marked for add"
        elif action == "edit":
            icon = hou.text.expandString(
                str="$P4HOUDINI/misc/p4icons/lock_self_user.png"  # type: ignore
            )
            tooltip = "File edited"
        elif action == "delete":
            icon = hou.text.expandString(str="$P4HOUDINI/misc/p4icons/delete.png")  # type: ignore
            tooltip = "File marked for delete"
        else:
            print("MISSING ICON FOR", action)

        return [QtGui.QIcon(icon), tooltip]

    def populate_files_to_add_listview(self):
        """
        Populate the list view with files and their status, using batch status retrieval.
        Updates UI elements based on the status data fetched from Perforce.
        """
        self.addwidget.clear()
        file_paths = self.proposed_files_to_add
        file_statuses = self.plugin.get_file_statuses(file_paths)

        for file in file_paths:
            item = QtWidgets.QListWidgetItem(file)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)  # Default to checked

            # Fetch the status from the dictionary, use default if not present
            file_status = file_statuses.get(file, {"error": "status unknown"})

            # Determine the icon and tooltip based on the file status
            icon, tooltip = self.detect_status_add(file_status)

            # Set the icon and tooltip for the list item
            item.setIcon(icon)
            item.setToolTip(tooltip)

            # Add the item to the list widget
            self.addwidget.addItem(item)

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Window title and description
        _window_title = ""
        _window_message = ""
        if self.mode == "add":
            _window_title = PLUGIN_NAME + " - Add or Checkout"
            _window_message = "Select a changelist to add these files to"
        elif self.mode == "submit":
            _window_title = PLUGIN_NAME + " - Submit a Changelist"
            _window_message = "Select a changelist to submit"
        elif self.mode == "edit":
            _window_title = PLUGIN_NAME + " - Edit a Changelist"
            _window_message = "Select a changelist to edit"
        self.setWindowTitle(_window_title)
        message_widget = QtWidgets.QLabel(_window_message)

        if self.mode != "edit":
            layout.addWidget(message_widget)

        # List of files to be added / checked out
        if self.mode == "add":
            self.addwidget = QtWidgets.QListWidget()
            self.populate_files_to_add_listview()
            layout.addWidget(self.addwidget)
            self.addwidget.installEventFilter(self)

        # Changelist picker
        self.changelist_dropdown = QtWidgets.QComboBox(self)
        self.changelist_dropdown.setEditable(False)
        self.construct_changelist_descriptions()
        self.changelist_dropdown.addItems(self.available_cl)
        self.changelist_dropdown.currentIndexChanged.connect(
            self.on_chosen_changelist_changed
        )
        layout.addWidget(self.changelist_dropdown)

        # Changelist description
        self.changelist_desc = QtWidgets.QPlainTextEdit()
        layout.addWidget(self.changelist_desc)

        # Changelist overview
        self.listwidget = QtWidgets.QListWidget()
        self.update_file_dropdown()

        layout.addWidget(self.listwidget)

        # Button for the primary action of the dialog
        _main_action_description = ""
        buttonlayout = QtWidgets.QHBoxLayout()
        if self.mode == "add":
            _main_action_description = "Add"
        elif self.mode == "submit":
            _main_action_description = "Submit"
        elif self.mode == "edit":
            _main_action_description = "Apply"
        self.update_button = QtWidgets.QPushButton(_main_action_description)
        self.update_button.clicked.connect(self.on_accept)
        buttonlayout.addWidget(self.update_button)

        # Button for canceling
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        buttonlayout.addWidget(self.cancel_button)

        layout.addLayout(buttonlayout)

        if self.mode == "edit":
            _index = self.available_cl_id.index(int(self.start_checklist))  # type: ignore
            self.changelist_dropdown.setCurrentIndex(_index)

        self.on_chosen_changelist_changed()
        if self.mode == "add":
            self.setMinimumSize(
                hou.ui.scaledSize(size=700), hou.ui.scaledSize(size=400)  # type: ignore
            )
        else:
            self.setMinimumSize(
                hou.ui.scaledSize(size=700), hou.ui.scaledSize(size=400)  # type: ignore
            )


class P4HoudiniWorkspaceChooser(QtWidgets.QDialog):
    """
    UI for letting user pick the workspace they wish to use.
    """

    def __init__(self, parent, plugin):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.plugin = plugin
        self.original_client = self.plugin.preferences.P4Settings.P4CLIENT
        self.found_clients = [self.original_client]
        self.buildUI()
        self.resize(self.minimumSizeHint())

    def closeEvent(self, event):
        pass

    def update_login_prefs(self):
        self.plugin.preferences.P4Settings.P4PORT = self.port_edit.text()
        self.plugin.preferences.P4Settings.P4USER = self.username_edit.text()
        self.plugin.preferences.P4Settings.P4CLIENT = (
            self.workspace_dropdown.currentText()
        )

    def on_refresh_workspaces(self):
        self.update_login_prefs()
        self.workspace_dropdown.clear()
        self.found_clients = [self.original_client]
        success, _ = self.plugin.attempt_login()
        if success:
            local_workspaces = self.plugin.get_local_workspaces()
            for workspace in local_workspaces:
                if workspace not in self.found_clients:
                    self.found_clients.append(workspace)
        self.workspace_dropdown.addItems(self.found_clients)

    def on_accept(self):
        self.update_login_prefs()

        if not P4Utils.check_perforce_installed():
            return

        succesful_login, reason = self.plugin.attempt_login()
        if succesful_login:
            self.plugin.save_preferences()
            self.close()
        else:
            if reason != "expired_login":
                P4Messages.warn_user_workspace_not_valid()

    def on_cancel(self):
        self.close()

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Window title and description
        _window_title = PLUGIN_NAME + " - Workspace Chooser"
        self.setWindowTitle(_window_title)

        grid_layout = QtWidgets.QGridLayout()

        # Server Field
        port_label = QtWidgets.QLabel("Server:")
        self.port_edit = QtWidgets.QLineEdit(self.plugin.preferences.P4Settings.P4PORT)
        grid_layout.addWidget(port_label, 0, 0)
        grid_layout.addWidget(self.port_edit, 0, 1)

        # Username Field
        username_label = QtWidgets.QLabel("User:")
        self.username_edit = QtWidgets.QLineEdit(
            self.plugin.preferences.P4Settings.P4USER
        )
        grid_layout.addWidget(username_label, 1, 0)
        grid_layout.addWidget(self.username_edit, 1, 1)

        # Workspace Field
        client_label = QtWidgets.QLabel("Workspace:    ")
        grid_layout.addWidget(client_label, 2, 0)
        self.workspace_dropdown = QtWidgets.QComboBox(self)
        self.workspace_dropdown.setEditable(True)
        self.workspace_dropdown.addItems(self.found_clients)
        self.workspace_button = QtWidgets.QPushButton("\u21BB")
        font = QtGui.QFont("Arial", hou.ui.scaledSize(size=12))  # type: ignore
        font.setBold(True)
        self.workspace_button.setFont(font)
        self.workspace_button.clicked.connect(self.on_refresh_workspaces)
        grid_layout.addWidget(self.workspace_dropdown, 2, 1)
        grid_layout.addWidget(self.workspace_button, 2, 2)

        # Add the grid layout to the main layout
        layout.addLayout(grid_layout)
        layout.addStretch(1)

        # Button for the primary action of the dialog
        buttonlayout = QtWidgets.QHBoxLayout()
        self.update_button = QtWidgets.QPushButton("Apply")
        self.update_button.clicked.connect(self.on_accept)
        buttonlayout.addWidget(self.update_button)

        # Button for canceling
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        buttonlayout.addWidget(self.cancel_button)

        layout.addLayout(buttonlayout)

        self.setMinimumSize(hou.ui.scaledSize(size=500), hou.ui.scaledSize(size=120))  # type: ignore
