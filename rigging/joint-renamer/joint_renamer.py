""""
JOINT RENAMING TOOL

V3:
    
    - <prefix_><side_><region_><basename><index>
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

pf = {
    "Default": "bn_",
    "Hair": "hbn_",
    "Eyelid": "ebn_",
    "End bone": "be_"
    }

all_pf = tuple(pf.values())
default_pf = pf["Default"]
hair_pf = pf["Hair"]
eyelid_pf = pf["Eyelid"]
end_pf = pf["End bone"]

side = {
    "None": "",
    "Left": "l_",
    "Right": "r_"
    }

region = {
    "None": "",
    "Upper": "upper_",
    "Middle": "middle_",
    "Lower:": "lower_"
    }


def short_name(dag_path: str) -> str:
    if not dag_path:
        return "" # this shouldn't happen
    return dag_path.split("|")[-1]

def is_named(name: str) -> bool:
    return short_name(name).startswith(all_pf)
    
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

def define_name(
        chain: list[str],
        prefix: str,
        side: str,
        region: str,
        basename: str,
        should_skip: bool,
        use_index: bool
        ) -> list:

    if not chain:
        raise RuntimeError("Internal error: joint chain is empty.")
    
    clean_name = basename.strip()
    index_padding = 2
    index = 1
    name_plan = [] 
    end_joint = chain[-1]

    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", clean_name):
        raise RuntimeError("Name must start with a letter or underscore and contain only A-Z, digits, or underscores.")
    
    for joint in chain:
        already_named = is_named(joint)
        will_rename = not (already_named and should_skip)
        is_end_joint = (joint == end_joint)
        prefix = prefix if not is_end_joint else end_pf

        joint_dict = {
            "og_name": joint, 
            "already_named": already_named,
            "is_end": is_end_joint,
            "will_rename": will_rename,
            "side": side,
            "region": region,
            "prefix": prefix if will_rename else None,
            "basename": clean_name if will_rename else None,
            "index": None
            }
        
        if use_index and will_rename:
            joint_dict["index"] = index
            index += 1

        name_plan.append(joint_dict)

    for joint in name_plan:

        if joint["will_rename"]:
            
            if joint["index"] is not None:
                index_str = str(joint["index"]).zfill(index_padding)
            else:
                index_str = ""
            
            joint["new_name"] = f"{joint['prefix']}{joint['side']}{joint['region']}{joint['basename']}{index_str}"
        
        else:
            joint["new_name"] = None


    return name_plan

# FUNCTION 3: Rename!!

def apply_rename(plan: list[dict]):

    for joint in reversed(plan):
        if joint["new_name"]:
            cmds.rename(joint["og_name"], joint["new_name"])





def show_ui():

    window_id = "joint_renamer_v3"
    window_title = "Joint Renamer V3"
    basename_label = "Basename:"

    window_width = 350
    half = window_width//2
    third = window_width//3
    label_w = window_width//5

    mode_all = "Rename All"
    mode_one = "Rename One By One"

    can_use_index = True

    def update_index_status():
        if cmds.optionMenu(mode_menu, query=True, value=True) == mode_all:
            can_use_index = False

    def onClose(*args):
        cmds.deleteUI(window_id)

    def onSkip(*args):
        pass

    def onRename(*args):
        mode_type = cmds.optionMenu(mode_menu, query=True, value=True)
        if mode_type == mode_all:
            user_input = cmds.textFieldGrp(
                basename_field,
                query = True,
                text = True)
            use_index = True
            should_skip = cmds.checkBox(skip_cb, query=True, value=True)
            prefix_label = pf[cmds.optionMenu(joint_type_menu, query=True, value=True)]
            side_label = side[cmds.optionMenu(side_menu, query=True, value=True)]
            region_label = region[cmds.optionMenu(region_menu, query=True, value=True)]
            rename_chain = validate()
            rename_chain_dict = define_name(
                rename_chain,
                prefix_label,
                side_label,
                region_label,
                user_input,
                should_skip,
                use_index)
            apply_rename(rename_chain_dict)

        elif mode_type == mode_one:
            use_index = cmds.checkBox(index_cb, query=True, value=True)

    if cmds.window(window_id, exists=True):
        cmds.deleteUI(window_id)

#######

    cmds.window(
        window_id, 
        title=window_title, 
        widthHeight=(window_width, 185),
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
    
    cmds.separator(height=10, style="none")

    cmds.rowLayout(numberOfColumns=2)
    cmds.columnLayout(adjustableColumn=True)

    joint_type_menu = cmds.optionMenu(label="Joint Type")
    cmds.menuItem(label="Default")
    cmds.menuItem(label="Hair")
    cmds.menuItem(label="Eyelid")

    side_menu = cmds.optionMenu(label="Side")
    cmds.menuItem(label="None")
    cmds.menuItem(label="Left")
    cmds.menuItem(label="Right")

    region_menu = cmds.optionMenu(label="Region")
    cmds.menuItem(label="None")
    cmds.menuItem(label="Upper")
    cmds.menuItem(label="Middle")
    cmds.menuItem(label="Lower")

    cmds.setParent("..")
   
    cmds.columnLayout(adjustableColumn=True)
   
    index_cb = cmds.checkBox(
        label="Numerical Indexing",
        width=half,
        value=True,
        enable=can_use_index
        )
    
    skip_cb = cmds.checkBox(
        label="Skip Named Joints",
        width=half,
        value=True
        )
    
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.separator(height=10, style="none")
    
    mode_menu = cmds.optionMenu(label="Mode",width=half)
    cmds.menuItem(label=mode_one,changeCommand=update_index_status)
    cmds.menuItem(label=mode_all,changeCommand=update_index_status)


    cmds.separator(height=10, style="none")

    cmds.rowLayout(numberOfColumns=3)
    
    cmds.button(
        label="Rename",
        width=third,
        command=onRename
        )
    
    cmds.button(
        label="Skip",
        width=third,
        command=onSkip
        )
    
    cmds.button(
        label="Close",
        width=third,
        command=onClose
        )
    
    cmds.setParent("..")
    cmds.showWindow(window_id)
    


show_ui()



# UI PLAN
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