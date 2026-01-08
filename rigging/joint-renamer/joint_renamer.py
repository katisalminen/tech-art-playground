""""
JOINT RENAMING TOOL

V2:

    - UI
    - User inputs base name
    - Buttons for rename, close
    - bn_<basename><index>

V3:

    - Dropdowns for joint type, side, region
    - Checkboxes for indexing, skipping already named joints
    - <prefix>_<side>_<region>_<basename><index>

Future improvements:
    - Use Classes instead of Dictionaries to store joint information

"""

import maya.cmds as cmds

# CORE

prefixes = {
    "Default": "bn_",
    "Hair": "hbn_",
    "Eyelid": "ebn_",
    "End bone": "be_"
    }

prefix_values = tuple(prefixes.values())
index_padding = 2


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

def rename(user_name: str, skip: bool, use_index: bool, index: int):

    sel = cmds.ls(selection=True)
    joint_chain = []
    joint_chain_info = []


    # VALIDATE NAME

    clean_name = user_name.strip()

    if not clean_name:
        raise RuntimeError("Joint name cannot be empty.")
    elif clean_name[0].isdigit():
        raise RuntimeError("Name cannot start with a digit.")

    for c in clean_name:
        if not c.isalnum() and c != "_":
            raise RuntimeError("Name should only have letters A-Z, digits or underscores.")



    ## VALIDATE SELECTION
    if not sel:
        raise RuntimeError("Please select the start of the joint chain.")
    elif len(sel) == 1:
        if cmds.nodeType(sel[0]) != "joint":
            raise RuntimeError("Selection is not a joint.")
        else:
            current_joint = sel[0]
    else:
        raise RuntimeError("Please select only one joint.")

    ## CHECK FOR BRANCHING
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

    ## CHECK WHICH JOINTS ARE ALREADY NAMED
    for joint in joint_chain:
        joint_dict = {
            "og_name": joint, 
            "already_named": is_named(joint)
            }
        joint_chain_info.append(joint_dict)

    ## RENAMING YES/NO
    for joint in joint_chain_info:
        if joint.get("already_named"):
            if not skip:
                joint["will_rename"] = True
            else:
                joint["will_rename"] = False
        else:
            joint["will_rename"] = True


    ## BASENAME
    for joint in joint_chain_info:

        if joint.get("will_rename"):
            joint["basename"] = clean_name


    ## INDEXING
    for joint in joint_chain_info:

        if use_index and joint.get("will_rename"):
            joint["index"] = index
            index += 1


    ## RENAME JOINTS
    for joint in joint_chain_info:

        if joint.get("will_rename"):
            
            if joint.get("index"):
                index_str = str(joint.get("index")).zfill(index_padding)
            else:
                index_str = ""

            new_name = f"bn_{joint.get('basename')}{index_str}"
            
            cmds.rename(joint["og_name"], new_name)




def show_ui():

    window_id = "joint_renamer_v2"
    window_title = "Joint Renamer V2"
    basename_label = "Basename:"

    def closeWindow(*args):
        cmds.deleteUI(window_id)

    if cmds.window(window_id, exists=True):
        cmds.deleteUI(window_id)

    cmds.window(
        window_id, 
        title=window_title, 
        widthHeight=(350, 125),
        sizeable=False
        )
    
    cmds.columnLayout(adjustableColumn=True)

    cmds.separator(height=20, style="none")

    basename_field = cmds.textFieldGrp(
        label=basename_label,
        text="",
        columnWidth=(1,70),
        ann="Type joint's base name here."
        )
    
    cmds.separator(
        height=50, 
        style="none"
        )

    cmds.rowLayout(
        numberOfColumns=2,
        columnWidth2=[175,175],
        )
    
    cmds.button(label="Rename",width=175)
    cmds.button(
        label="Close",
        width=175,
        command=closeWindow
        )
    
    cmds.setParent("..")
    cmds.showWindow(window_id)
    


show_ui()




# UI
## show current name
## joint type: regular, hair, eyelid
## joint side: none, left, right
## joint region: none, upper, middle, lower
## numerical indexing on/off
## skip joints that look named on/off
## base name input field
## rename button
## skip joint button
## close button