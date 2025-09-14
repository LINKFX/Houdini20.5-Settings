"""
Simple script that registers some callbacks for the session.
"""

import hou  # pylint: disable=E0401
import P4Houdini
import P4Utils


def get_p4houdini_data():
    """
    Retrieve or initialize the P4Houdini data stored in the Houdini session.
    """
    if not hasattr(hou.session, "p4houdini"):  # type: ignore pylint: disable=E1101
        hou.session.p4houdini = P4Houdini.P4HoudiniData()  # type: ignore pylint: disable=E1101
    return hou.session.p4houdini  # type: ignore pylint: disable=E1101


def handle_before_save(p4houdini_data):
    """
    Actions to take before the HIP file is saved.
    """
    p4houdini_data.hip_pre_save = P4Houdini.hip_before_save_automatic()


def handle_after_save(p4houdini_data):
    """
    Actions to take after the HIP file is saved, conditional on prior actions before save.
    """
    if not p4houdini_data.hip_pre_save:
        P4Houdini.hip_after_save_automatic()
        p4houdini_data.hip_pre_save = False


def scene_event_callback(event_type):
    """
    Attaching P4Houdini plugin to Hip saving mechanism.
    """
    if not P4Utils.check_perforce_installed():
        return

    p4houdini_data = get_p4houdini_data()

    if event_type == hou.hipFileEventType.BeforeSave:  # type: ignore
        handle_before_save(p4houdini_data)
    elif event_type == hou.hipFileEventType.AfterSave:  # type: ignore
        handle_after_save(p4houdini_data)

    # # Check if file in sync with depot
    # elif event_type == hou.hipFileEventType.BeforeLoad:
    #     P4Houdini.hip_before_load_automatic()


def before_hda_saved_event_callback(
    event_type, asset_definition, **kwargs
):  # pylint: disable=W0613
    """
    Attach checking out HDA definitions on disk before saving.
    """
    if asset_definition:
        file = asset_definition.libraryFilePath()
        P4Houdini.hda_save_automatic(file)


def hda_saved_event_callback(
    event_type, asset_definition, **kwargs
):  # pylint: disable=W0613
    """
    Attach marking HDA definition on disk for add after saving.
    """
    if asset_definition:
        file = asset_definition.libraryFilePath()
        P4Houdini.hda_save_automatic(file)


hou.hda.addEventCallback(
    (hou.hdaEventType.BeforeAssetSaved,), before_hda_saved_event_callback  # type: ignore
)  # type: ignore
hou.hda.addEventCallback((hou.hdaEventType.AssetSaved,), hda_saved_event_callback)  # type: ignore
hou.hipFile.addEventCallback(scene_event_callback)  # type: ignore
