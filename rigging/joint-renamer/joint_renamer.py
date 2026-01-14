""""
JOINT RENAMING TOOL

V4:

    - Keep Basename checkbox
    - Traverse down the joint chain
    - Individually rename each joint
        - Preserve basename text between passes or delete?
        - Core loop: write basename, select modifiers -> click Rename -> joint is named, automatically moves to the next joint -> write basename, select modifiers -> rename -> etc.
    - "New Name" preview?

Future improvements:
    - Use Classes instead of Dictionaries to store joint information
    - User can define joint prefix label and name, add as many as they like
    - User preferences are stored between Maya restarts

"""

import maya.cmds as cmds
import re



pf_dict = {
    "Default": "bn_",
    "Hair": "hbn_",
    "Eyelid": "ebn_",

    "End bone": "be_",
    "Hair end bone": "hbe_",
    "Eyelid end bone": "ebe_"
    }

all_joints_pf = tuple(pf_dict.values())
default_joint_pf = pf_dict["Default"]
hair_joint_pf = pf_dict["Hair"]
eyelid_joint_pf = pf_dict["Eyelid"]
end_joint_pf = pf_dict["End bone"]
hair_end_joint_pf = pf_dict["Hair end bone"]
eyelid_end_joint_pf = pf_dict["Eyelid end bone"]

side_dict = {
    "None": "",
    "Left": "l_",
    "Right": "r_"
    }

region_dict = {
    "None": "",
    "Upper": "upper_",
    "Middle": "middle_",
    "Lower": "lower_"
    }



def short_name(dag_path: str) -> str:
    if not dag_path:
        return "" # this shouldn't happen
    return dag_path.split("|")[-1]

def is_named(name: str) -> bool:
    return short_name(name).startswith(all_joints_pf)
    
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








# FUNCTION 3

def rename_all(
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

    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", clean_name):
        raise RuntimeError("Name must start with a letter or underscore and contain only A-Z, digits, or underscores.")

    index_padding = 2
    index = 1
    name_plan = [] 
    end_joint = chain[-1]

    end_swap = {
        default_joint_pf: end_joint_pf,
        hair_joint_pf: hair_end_joint_pf,
        eyelid_joint_pf: eyelid_end_joint_pf
    }

    end_prefix = end_swap.get(prefix, end_joint_pf)
    
    for joint in chain:
        already_named = is_named(joint)
        will_rename = not (already_named and should_skip)
        is_end_joint = (joint == end_joint)
        prefix = prefix if not is_end_joint else end_prefix

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

# FUNCTION 4: Rename!!

def apply_rename(plan: list[dict]):

    for joint in reversed(plan):
        if joint["new_name"]:
            cmds.rename(joint["og_name"], joint["new_name"])





def show_ui():

    window_id = "joint_renamer_v4"
    window_title = "Joint Renamer V4"
    basename_label = "Basename "
    mode_all = "Rename All"
    mode_one = "Rename One By One"

    window_width = 400
    window_height = 210
    window_padding = 10
    separator_padding = window_padding
    window_content_width = window_width-window_padding*2
    half = window_content_width//2
    third = window_content_width//3
    quarter = window_content_width//4


    def update_mode_status(*args):
        current_mode = cmds.optionMenu(mode_menu, query=True, value=True)
        if current_mode == mode_all:
            cmds.checkBox(index_cb, edit=True, value=True, enable=False)
            cmds.checkBox(keep_basename_cb, edit=True, enable=False)
            cmds.button(skip_button, edit=True, enable=False)
        else:
            cmds.checkBox(index_cb, edit=True, enable=True)
            cmds.checkBox(keep_basename_cb, edit=True, enable=True)
            cmds.button(skip_button, edit=True, enable=True)

    def read_ui_for_rename() -> tuple:
        prefix_token = pf_dict[cmds.optionMenuGrp(joint_type_menu, query=True, value=True)]
        side_token = side_dict[cmds.optionMenuGrp(side_menu, query=True, value=True)]
        region_token = region_dict[cmds.optionMenuGrp(region_menu, query=True, value=True)]
        basename_token = cmds.textFieldGrp(basename_field, query = True, text = True)
        skip_token = cmds.checkBox(skip_cb, query=True, value=True)
        index_token = cmds.checkBox(index_cb, query=True, value=True)
        return (prefix_token, side_token, region_token, basename_token, skip_token, index_token)
        

    def onClose(*args):
        cmds.deleteUI(window_id)

    def onSkip(*args): 
        pass

    def onRename(*args):
        mode_type = cmds.optionMenu(mode_menu, query=True, value=True)
        if mode_type == mode_all:
            rename_info = read_ui_for_rename()
            rename_chain = validate()
            rename_chain_dict = rename_all(rename_chain, *rename_info)
            apply_rename(rename_chain_dict)

        elif mode_type == mode_one:
            pass

    if cmds.window(window_id, exists=True):
        cmds.deleteUI(window_id)

#######

    cmds.window(
        window_id, 
        title=window_title, 
        widthHeight=(window_width, window_height),
        sizeable=False
        )
    
    cmds.columnLayout(adjustableColumn=True,columnOffset=["both", window_padding])
    cmds.separator(height=separator_padding*1.5, style="none")

    basename_field = cmds.textFieldGrp(
        label=basename_label,
        text="",
        columnWidth2=(quarter, half),
        ann="Type joint's base name here"
        )
    
    cmds.columnLayout(columnOffset=["both", window_padding*4])
    keep_basename_cb = cmds.checkBox(
        label="Preserve Basename",
        ann="Check to preserve typed Basename between Rename passes",
        value=True
        )
    cmds.setParent("..")
    cmds.separator(height=separator_padding, style="none")

    cmds.rowLayout(numberOfColumns=2, columnWidth2=(half,half))
    cmds.columnLayout()

    joint_type_menu = cmds.optionMenuGrp(
        label="Joint Type", 
        columnWidth=(1,quarter), 
        ann="Sets the joint prefix"
        )
    for name in pf_dict:
        if "end" in name.lower():
            continue
        cmds.menuItem(label=name)

    side_menu = cmds.optionMenuGrp(
        label="Side", 
        columnWidth=(1,quarter), 
        ann="Sets a Left or Right prefix, choose None for empty"
        )
    for name in side_dict:
        cmds.menuItem(label=name)

    region_menu = cmds.optionMenuGrp(
        label="Region", 
        columnWidth=(1,quarter), 
        ann="Choose joint region, e.g. upper and lower lip or eyelid"
        )
    for name in region_dict:
        cmds.menuItem(label=name)

    cmds.setParent("..")
   
    cmds.columnLayout(adjustableColumn=True)
   
    index_cb = cmds.checkBox(
        label="Numerical Indexing",
        width=half,
        value=True,
        ann="Enable/disable numerical indexing 01, 02, etc."
        )
    
    skip_cb = cmds.checkBox(
        label="Skip Named Joints",
        width=half,
        value=True,
        ann="Skip joints that appear already named"
        )
        
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.separator(height=10, style="none")
    
    mode_menu = cmds.optionMenu(
        label="Mode",
        width=half,
        changeCommand=update_mode_status)
    cmds.menuItem(label=mode_one)
    cmds.menuItem(label=mode_all)


    cmds.separator(height=separator_padding, style="none")

    cmds.rowLayout(numberOfColumns=3)
    
    cmds.button(
        label="Rename",
        width=third,
        command=onRename
        )
    
    skip_button = cmds.button(
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
    update_mode_status()
    cmds.showWindow(window_id)
    


show_ui()

