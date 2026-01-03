""""
JOINT RENAMING TOOL

This is the V1 version of the Joint Renaming Tool.

V1:

    - Validate selection: one joint selected, is a joint, chain is single-branch
    - Store joint information in a list of dictionaries
    - Rename joint chain with default names
    - Add and increment numerical index to renamed joints
    - Skip already named joints: starts with bn_, hbn_, ebn_, be_
    - bn_basename<index>

V2:

    - UI
    - User inputs base name
    - Buttons for rename, skip, close
    - bn_<basename><index>

V3:

    - Dropdowns for joint type, side, region
    - Checkboxes for indexing, skipping already named joints
    - <prefix>_<side>_<region>_<basename><index>

Future improvements:
    - Use Classes instead of Dictionaries to store joint information

"""

import maya.cmds as cmds

# validate selection
    # nothing -> inform user to select a joint
    # multiple -> inform user to select one joint
    # check type:
        # not a joint -> inform user to select a joint
        # joint -> proceed
    # check if any joint in the chain has multiple joint children
        # yes -> inform the user the joint hierarchy cannot have multiple branches
        # no -> run the program



# store selected joints in a list of dictionaries in order of root -> leaf
    # joint name
    # does it look named True/False

# build new joint names
    # <prefix>_<side>_<region>_<basename><index>

# rename each joint
    # skip joints that are already named
    # if renaming fails e.g. due to a locked joint, stop and report








## UI
# show current name
# joint type: regular, hair, eyelid
# joint side: none, left, right
# joint region: none, upper, middle, lower
# numerical indexing on/off
# skip joints that look named on/off
# base name input field
# rename button
# skip joint button
# close button