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
named_prefixes = ("bn_", "hbn_", "ebn_", "be_")
basename = "newname" # default base name for V1
joint_chain = [] # list of joint hierarchy
joint_chain_info = [] # joint names and whether they are named in a list of dictionaries

# HELPER FUNCTIONS

def is_named(name: str):
    if name.startswith(named_prefixes):
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

# CHECK IF SOME JOINTS ARE ALREADY NAMED

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

for joint in joint_chain:
    joint_dict = {
        "name": joint, 
        "already_named": is_named(joint)
        }
    joint_chain_info.append(joint_dict)



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