"""
Barebone module that contains all prompts made to the user
by the plugin.
"""

import P4UI

PLUGIN_NAME = "P4Houdini"


def warn_user_file_not_under_depot():
    """
    Utility to show the user the error message stating the file lives
    outside of the repository root.
    """
    message = "This file lives outside of the repository root!"
    P4UI.P4Message(message)


def warn_user_dependencies_missing():
    """
    Utility to show the user the error message stating the P4Houdini required dependencies are not installed.
    """
    message = (
        "Perforce API has not been found. Please install the P4Houdini dependencies!"
    )
    P4UI.P4Message(message)


def warn_user_no_dependencies_found():
    """
    Utility to show the user an information dialog stating no
    unresolved dependencies have been found.
    """
    message = "No untracked file dependencies found!"
    P4UI.P4Message(message)


def warn_user_to_login():
    """
    Utility to show the user an information dialog stating
    the user needs to open P4V and login manually.
    """
    message = "Your P4V session has expired. Please open P4V and login manually"
    P4UI.P4Message(message)


def warn_user_workspace_not_valid():
    """
    Utility to show the user an information dialog stating
    the configured workspace is not valid.
    """
    message = "The configured P4Houdini Server and User combination is not correct!"
    P4UI.P4Message(message)


def warn_user_file_already_checked_out():
    """
    Utility to show the user that the file they are trying to
    check out has already been checked out.
    """
    message = "File has already been checked out!"
    P4UI.P4Message(message)


def warn_user_file_not_checked_out():
    """
    Utility to warn the user that the file they are trying to perform
    an action with has not been checked out on Perforce.
    """
    message = "File has not been checked out!"
    P4UI.P4Message(message)


def warn_user_plugin_state_changed(state):
    """
    Utility to warn the user that the file they are trying to perform
    an action with has not been checked out on Perforce.
    """
    message = "The plugin is now disabled and will not auto-prompt anymore!"
    if state:
        message = "The plugin is now enabled and will auto-prompt again!"
    P4UI.P4Message(message)


def confirm_user_revert_file():
    """
    Utility to prompt the user with a confirmation dialog about
    whether or not they really want to revert this file.
    """
    message = "This action will revert the file to the latest version found on the repository. This action CANNOT be undone. Continue?"
    return P4UI.P4Prompt(message)


def warn_user_file_doesnt_exist():
    """
    Utility to warn the user that the file they they are trying to use
    does not exist. For example when trying to add an unsaved hip file.
    """
    message = "The file you're trying to use with the plugin does not exist on disk. Did you save?"
    return P4UI.P4Prompt(message)
