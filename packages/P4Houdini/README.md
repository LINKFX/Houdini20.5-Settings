# P4Houdini
![P4Houdini Banner](https://github.com/AMTA-Consultancy/P4Houdini/blob/main/misc/images/P4Houdini_Plugin.jpg)

You can join the Discord to chat about the plugin: https://discord.gg/rKr5SNZJtM
Please note that the plugin is (officially) supports Houdini 20.0 on Windows and Linux. Mac may also work, but has not been tested.

## Important information about Houdini & Perforce!
Please make sure your hip and hda files that get submitted to perforce are marked as binary files and not text files!!
Hip and HDAs not marked as binary will not properly version on perforce, and will corrupt your files. (This has nothing to do with the plugin)
For more information on filetypes, see: https://www.perforce.com/manuals/p4sag/Content/P4SAG/defining-filetype-with-p4-typemap.html


## Installing for Houdini
To install the plugin for the first time, follow these steps:
1. Clone this repository and make note of the directory you have cloned it to.
2. Copy the `P4Houdini.json` file found in the repository root, and paste it in the $HOUDINI_USER_PREF_DIR/packages/ folder.
3. Edit the `P4Houdini.json` file you just pasted, and modify the `$P4HOUDINI` path found inside. Set the path to where you cloned the repository to in step one.
4. Configure your workspace by pressing the `Set Workspace` shelf button. Additionally you can also manually configure it in the `P4Preferences.json` file. The variable to set is `P4Settings`.

## Configuring a P4 Repository
The plugin makes use of P4TICKETS. This means that it wil make use of already validated and authenticated sessions from the Perforce Visual Client. These tickets are valid by default for 12 hours. If the plugin has authentication issues, try logging in on P4V again. 

## Using the Plugin

- (Automatic) checking out and adding of hip files. (Triggers when saving a file)
- (Automatic) checking out and adding of hda files. (RMB menu when clicking on HDA)
- Submitting (partial) changelists from inside Houdini. (See shelf tool)
- Editing pending Changelists.
- Reverting HIP and HDAs to the latest version found on the repository.
- Check out files specified in any string parm using RMB Click > P4Houdini > Add/Checkout.
- Scanning hip file for files that are being written to, and allowing users to add or 
  check them out automatically preventing any permission errors during cook. Now also supporting $F expressions.
- Modify or set the description of a new or existing changelist while adding/checking out files
  as well as during submit.
- Make files writeable by RMB clicking items in the dialog that shows up when saving / adding one or multiple files.
- You can also automatically add files on ROPs using post-render scripts. 
  Check out the `examples/manual_managing_files.hip` for an example. You will see that the pre-frame and post-write parms have python expression in it which will ensure all files get checked out pre-write, or get added to the changelist after creation.


**Enable the P4Houdini shelf!**

![P4Houdini Shelf](https://github.com/Bismuth-Consultancy-BV/P4Houdini-Private/blob/main/misc/images/P4Houdini_Shelf.jpg)

The plugin root has a file called `P4Preferences.json`, which contains some settings you can configure.
`P4Settings` - These are the typical P4 settings used to connect to a server through a user and workspace.
`P4CL_Default` - Allows you to set a default changelist name that will get added to the dropdown menu when selecting a changelist.
`P4Updates` - This dictionary contains booleans for automatic triggers that will happen when using Houdini. Setting these to false will no longer automatically
trigger the plugin to issue Perforce commands when for example saving a file. This allows you to for example have a purely manual workflow.


## Troubleshooting
Please contact SideFX Support

## DISCLAIMERS
Perforce, their API and any of their icons used by the plugin is owned and developed by Perforce Software, Inc. https://www.perforce.com/
Houdini is owned and developed by SideFX. https://www.sidefx.com/

## API

```
FUNCTIONS
    node_file_automatic(node)
        For the given node, check out or add all files found in the known
        parameters described in P4NodeCheckouts.json

    hda_save_automatic(file):
        Prompts the user to either check out or add the HDA definition
        after hitting save. It only does this if the plugin preferences
        have this enabled. This is used by event callbacks in pythonrc.py

    hda_revert(node)
        Reverts the specified node definition to what is found on the depot.
        Also matches the specified node instance to that.

    hip_before_save_automatic()
        Prompts the user to check out the HIP
        right before the file gets saved. This prevents any permission
        errors due to file locks. It only does this if the
        plugin preferences have this enabled.
        This is used by event callbacks in pythonrc.py

    hip_after_save_automatic()
        Prompts the user to either add the HIP
        after hitting save. It only does this if the plugin preferences
        have this enabled. This is used by event callbacks in pythonrc.py

    hip_checkout_dependencies()
        Crawl through all nodes found in the currently open HIP file,
        and check if its node type name is found in the P4NodeCheckouts.json file.
        If it is, it will look for files in the P4NodeCheckouts.json parameters marked as write.

    hip_before_load_automatic()
        Automatically check if the file that is to be loaded is the latest version.
        If not it will prompt for an update. This is used by event callbacks in pythonrc.py
        NOTE: CURRENTLY NOT USED BECAUSE OF A BUG IN HOUDINI CAUSING A FREEZE.

    hip_checkout_manual()
        Prompts the user to check out the currently open HIP file.

    hip_revert()
        Prompts the user to revert the currently open HIP file
        to the state it is on the depot. It will also
        reload the hip file automatically.

    file_revert(file)
        Reverts the specified file to the state found on the depot.

    file_checkout(file)
        Prompts the user to check out the specified file.

    file_edit_changelist(file)
        Prompts the user to edit the changelist belonging to the specified file.

    submit_dialog()
        Prompts the user with the P4Houdini submit dialog.

    toggle_plugin_active()
        Utility to toggle the P4Houdini plugin enabled or disable.
```
