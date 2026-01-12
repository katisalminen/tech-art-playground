""""
JOINT RENAMING TOOL

V3:

    - Refactor rename(), split into three functions:
        - Joint chain validation
        - Deciding new names
        - Renaming
    
    - Skip & index toggle, no UI yet
    - Joint type, side, region naming, no UI yet
    - <prefix_><side_><region_><basename><index>
    - Still name the entire chain in one go
    - Auto end bone prefixes be_, hbe_, ebe_
    - UI controls: index, skip, prefix dropdown


V4:

    - Traverse down the joint chain
    - Individually rename each joint
        - Preserve basename text between passes
        - User can input basename -> click -> click -> click: bn_name01, bn_name01, bn_name03
        - Or name individually: bn_firstjoint01 -> click -> bn_secondjoint01 -> click
    - "Current Name" field for name that is being overwritten
    - "New Name" preview

Future improvements:
    - Use Classes instead of Dictionaries to store joint information

"""

import maya.cmds as cmds
import re

prefixes = {
    "Default": "bn_",
    "Hair": "hbn_",
    "Eyelid": "ebn_",
    "End bone": "be_"
    }

prefix_values = tuple(prefixes.values())

def short_name(dag_path: str) -> str:
    if not dag_path:
        return "" # this shouldn't happen
    return dag_path.split("|")[-1]

def is_named(name: str) -> bool:
    return short_name(name).startswith(prefix_values)
    
def check_children(joint: str) -> list[str]:
    children = cmds.listRelatives(joint, type="joint", fullPath=True) or []
    return children # current joint's child(ren)



# FUNCTION 1: Validate user's selection

def validate() -> list[str]:

    sel = cmds.ls(selection=True, long=True) # list things in the current scene (selected ones)
    joint_chain = []

    if not sel:
        raise RuntimeError("Please select the start of the joint chain.")
    elif len(sel) == 1:
        if cmds.nodeType(sel[0]) != "joint":
            raise RuntimeError("Selection is not a joint.")
        else:
            current_joint = sel[0]
    else:
        raise RuntimeError("Please select only one joint.")
    
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
    
    return joint_chain



# FUNCTION 2: Decide the new names

def define_name(chain: list[str], basename: str, should_skip: bool, use_index: bool) -> list:

    clean_name = basename.strip()
    index_padding = 2
    index = 1
    name_plan = [] 
    end_joint = chain[-1]

    if not chain:
        raise RuntimeError("Internal error: joint chain is empty.")

    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", clean_name):
        raise RuntimeError("Name must start with a letter or underscore and contain only A-Z, digits, or underscores.")
    
    for joint in chain:
        already_named = is_named(joint)
        will_rename = not (already_named and should_skip)

        joint_dict = {
            "og_name": joint, 
            "already_named": already_named,
            "is_end": (joint == end_joint),
            "will_rename": will_rename,
            "prefix": prefix_values[0],
            "basename": clean_name if will_rename else None,
            "index": None,
            }
        
        if use_index and will_rename:
            joint_dict["index"] = index
            index += 1

        if joint_dict["is_end"]:
            joint_dict["prefix"] = prefix_values[3]

        name_plan.append(joint_dict)

    for joint in name_plan:

        if joint["will_rename"]:
            
            if joint["index"] is not None:
                index_str = str(joint["index"]).zfill(index_padding)
            else:
                index_str = ""

            if not joint["is_end"]:
                prefix = prefix_values[0]
            else:
                prefix = prefix_values[3]
            
            joint["new_name"] = f"{prefix}{joint['basename']}{index_str}"
        
        else:
            joint["new_name"] = None


    return name_plan

# FUNCTION 3: Rename!!

def apply_rename(plan: list[dict]):

    for joint in reversed(plan):
        if joint["new_name"]:
            cmds.rename(joint["og_name"], joint["new_name"])





def show_ui():

    window_id = "joint_renamer_v2"
    window_title = "Joint Renamer V2"
    basename_label = "Basename:"

    window_width = 350
    half = window_width//2
    label_w = window_width//5

    def onClose(*args):
        cmds.deleteUI(window_id)

    def onRename(*args):
        user_input = cmds.textFieldGrp(
            basename_field,
            query = True,
            text = True

        )

        apply_rename(user_input,True,True,1)


    if cmds.window(window_id, exists=True):
        cmds.deleteUI(window_id)

    cmds.window(
        window_id, 
        title=window_title, 
        widthHeight=(window_width, 125),
        sizeable=False
        )
    
    cmds.columnLayout(adjustableColumn=True)

    cmds.separator(height=20, style="none")

    basename_field = cmds.textFieldGrp(
        label=basename_label,
        text="",
        columnWidth=(1,label_w),
        ann="Type joint's base name here."
        )
    
    cmds.separator(
        height=50, 
        style="none"
        )

    cmds.rowLayout(numberOfColumns=2)
    
    cmds.button(
        label="Rename",
        width=half,
        command=onRename
        )
    
    cmds.button(
        label="Close",
        width=half,
        command=onClose
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