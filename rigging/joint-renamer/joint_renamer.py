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

# VARIABLES

sel = cmds.ls(selection=True) # selection

prefixes = {
    "Default": "bn_",
    "Hair": "hbn_",
    "Eyelid": "ebn_",
    "End bone": "be_"
    }

prefix_values = tuple(prefixes.values())

base_name = "temp" # default base name for V1, later user input
skip_already_named = True # later user-controlled

use_index = True # later user-controlled
index = 1 # index start number
index_padding = 2 # 01, 02 etc.

joint_chain = [] # list of joint hierarchy
joint_chain_info = [] # joint names and whether they are named in a list of dictionaries

# HELPER FUNCTIONS

def is_named(name: str):
    if name.startswith(prefix_values):
        return True
    else:
        return False
    
def check_children(joint: str):
    children = cmds.listRelatives(joint, type="joint")
    if not children:
        children = []
    return children


# VALIDATE SELECTION

if not sel:
    raise RuntimeError("Please select the start of the joint chain.")
elif len(sel) == 1:
    if cmds.nodeType(sel[0]) != "joint":
        raise RuntimeError("Selection is not a joint.")
    else:
        current_joint = sel[0]
else:
    raise RuntimeError("Please select only one joint.")

# CHECK FOR BRANCHING

while True:
    joint_children = check_children(current_joint)
    if len(joint_children) > 1:
        raise RuntimeError(f"Joint {current_joint} has multiple joint children. Select a single chain.")
    else:
        joint_chain.append(current_joint)
        if not joint_children:
            break
        else:
            current_joint = joint_children[0]

# CHECK WHICH JOINTS ARE ALREADY NAMED
for joint in joint_chain:
    joint_dict = {
        "og_name": joint, 
        "already_named": is_named(joint)
        }
    joint_chain_info.append(joint_dict)

# RENAMING YES/NO
for joint in joint_chain_info:
    if joint.get("already_named"):
        if not skip_already_named:
            joint["will_rename"] = True
        else:
            joint["will_rename"] = False
    else:
        joint["will_rename"] = True


# BASENAME
for joint in joint_chain_info:

    if joint.get("will_rename"):
        joint["base_name"] = base_name


#INDEXING
for joint in joint_chain_info:

    if use_index and joint.get("will_rename"):
        joint["index"] = index
        index += 1


# RENAME JOINTS
for joint in joint_chain_info:

    if joint.get("will_rename"):

        if joint.get("index"):
            index_str = str(joint.get("index")).zfill(index_padding)
        else:
            index_str = ""

        new_name = f"bn_{joint.get('base_name')}{index_str}"

        cmds.rename(joint["og_name"], new_name)








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