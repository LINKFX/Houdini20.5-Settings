"""
Utility functions for P4Houdini and UI
"""

import dataclasses
import hashlib
import json
import os
import ssl
import subprocess
from urllib import request

import hou  # pylint: disable=E0401
import P4Houdini
import P4Messages
import P4UI

PIP_FOLDER = os.path.normpath(hou.text.expandString(str="$P4HOUDINI_PIP_FOLDER"))  # type: ignore


def check_perforce_installed():
    """
    Returns whether or not P4 dependencies are installed.
    """
    try:
        from P4 import P4  # pylint: disable=E0401,C0415,W0621,W0611

        return True
    except:  # pylint: disable=W0702
        return False


def set_workspace():
    """
    Util for opening the UI to configure the workspace.
    """
    if check_perforce_installed():
        plugin = P4Houdini.P4HoudiniPlugin(skip_login=True)
        dialog = P4UI.P4HoudiniWorkspaceChooser(hou.qt.mainWindow(), plugin)  # type: ignore
        dialog.exec()
    else:
        P4Messages.warn_user_dependencies_missing()


def get_default_preferences_file_path():
    """
    Gets the default preferences filepath.
    """
    return os.path.join(
        hou.text.expandString(str="$HOUDINI_USER_PREF_DIR"), "P4Preferences.json"  # type: ignore
    )  # type: ignore


def generate_prefs_file():
    """
    Generates the default preferences file.
    """
    default_path = get_default_preferences_file_path()
    with open(default_path, "w", encoding="utf-8") as file:
        json.dump(dataclasses.asdict(P4Houdini.P4HoudiniPreferences()), file, indent=4)

    return default_path


def get_preferences_file():
    """
    Finds or creates the preferences file in HOUDINI_PATH.
    """
    # findFiles() throws an error if no file is found
    try:
        return list(hou.findFiles("P4Preferences.json"))[0]
    except:  # pylint: disable=W0702
        pass

    # This is so we don't accidentally overwrite the newly generated prefs file with a new one
    # if Houdini hasnt been restarted yet.
    # This because it wont be in the HOUDINI_PATH yet.
    if os.path.isfile(get_default_preferences_file_path()):
        return get_default_preferences_file_path()

    return generate_prefs_file()
