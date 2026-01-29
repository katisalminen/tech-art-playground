

import maya.cmds as cmds
import re



pf_dict = {
    "Default": "bn_",
    "Hair": "hbn_",
    "Eye": "ebn_",
    "Face": "fbn_",

    "End bone": "be_",
    "Hair end bone": "hbe_",
    "Eye end bone": "ebe_",
    "Face end bone": "fbn_"
    }

pf_all_joints = tuple(pf_dict.values())

pf_end_swap = {
    pf_dict["Default"]: pf_dict["End bone"],
    pf_dict["Hair"]: pf_dict["Hair end bone"],
    pf_dict["Eye"]: pf_dict["Eye end bone"],
    pf_dict["Face"]: pf_dict["Face end bone"]
    }

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

# for mode_one ONLY: the session uses this state to traverse through the joint chain
state = {
        "chain": [],            # authoritative traversal list that shall not be strayed from
        "position": 0,          # current position in the chain, +1 when moving to next joint
        "last_basename": "",    # the basename used on the previous step
        "run_index": 0          # the current count for that basename run
    } 



def short_name(dag_path: str) -> str: # currently obsolete, but retained in case i go back to using DAG paths
    if not dag_path:
        return "" # this shouldn't happen
    return dag_path.split("|")[-1]

def is_named(name: str) -> bool:
    return short_name(name).startswith(pf_all_joints)
    
def check_children(joint: str) -> list[str]:
    children = cmds.listRelatives(joint, type="joint") or []
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


# FUNCTION 2: rename just ONE joint

def rename_one(
        chain: list,
        joint: str,
        prefix: str,
        side: str,
        region: str,
        basename: str,
        should_skip: bool,
        use_index: bool,
        keep_basename: bool,
        end_joint_naming: bool,
        index: int,
        ) -> dict:

    clean_name = basename.strip()

    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", clean_name):
        raise RuntimeError("Name must start with a letter or underscore and contain only A-Z, digits, or underscores.")

    index_padding = 2
    index_str = ""

    end_prefix = pf_end_swap.get(prefix, pf_dict["End bone"])
    
    already_named = is_named(joint)
    will_rename = not (already_named and should_skip)
    end_joint = chain[-1]
    is_end_joint = (joint == end_joint)
    prefix = prefix if not is_end_joint or not end_joint_naming else end_prefix

    joint_dict = {
        "og_name": joint, 
        "already_named": already_named,
        "is_end": is_end_joint,
        "will_rename": will_rename,
        "side": side,
        "region": region,
        "prefix": prefix if will_rename else None,
        "basename": clean_name if will_rename else None,
        "index": None,
        "new_name": None
        }
    
    if joint_dict["will_rename"]:
    
        if use_index:
            joint_dict["index"] = index
            index_str = str(joint_dict["index"]).zfill(index_padding)

        joint_dict["new_name"] = f"{joint_dict['prefix']}{joint_dict['side']}{joint_dict['region']}{joint_dict['basename']}{index_str}"

    return joint_dict


# FUNCTION 3: rename ALL joints in one, calling rename_one

def rename_all(
        chain: list,
        prefix: str,
        side: str,
        region: str,
        basename: str,
        should_skip: bool,
        use_index: bool,
        preserve_name: bool,
        end_joint: bool
        ) -> str:
    
    if not chain:
        raise RuntimeError("Internal error: joint chain is empty.")

    name_plan = [] 
    index = 1

    for joint in chain:
        # create a list of dictionaries for all joints using rename_one
        entry = rename_one(chain, joint, prefix, side, region, basename, should_skip, use_index, True, end_joint, index)
        if entry["will_rename"]:
            index += 1
        name_plan.append(entry)

    return name_plan

# FUNCTION 4: rename_all in one go

def apply_rename_all(plan: list[dict]):        

    for joint in reversed(plan): # reversed in case i go back to using DAG paths
        if joint["new_name"]:
            cmds.rename(joint["og_name"], joint["new_name"])


# FUNCTION 5 rename_one by one

def apply_rename_one(entry: dict) -> bool:

    if entry["new_name"]:
        cmds.rename(entry["og_name"], entry["new_name"])
        return True
    else:
        cmds.warning("Skipped joint.")
        return False



# WINDOW

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
            cmds.button(skip_button, edit=True, enable=False)

    def read_ui_for_rename() -> tuple:
        prefix_token = pf_dict[cmds.optionMenuGrp(joint_type_menu, query=True, value=True)]
        side_token = side_dict[cmds.optionMenuGrp(side_menu, query=True, value=True)]
        region_token = region_dict[cmds.optionMenuGrp(region_menu, query=True, value=True)]
        basename_token = cmds.textFieldGrp(basename_field, query = True, text = True)
        skip_token = cmds.checkBox(skip_cb, query=True, value=True)
        index_token = cmds.checkBox(index_cb, query=True, value=True)
        preserve_basename_token = cmds.checkBox(keep_basename_cb, query=True, value=True)
        end_joint_token = cmds.checkBox(endjoint_cb, query=True, value=True)
        return (prefix_token, side_token, region_token, basename_token, skip_token, index_token, preserve_basename_token, end_joint_token)
        

    def onClose(*args):
        cmds.deleteUI(window_id)

    def onSkip(*args): 
        state["position"] +=1
        cmds.select(state["chain"][state["position"]], replace=True)

    def onRename(*args):

        mode_type = cmds.optionMenu(mode_menu, query=True, value=True)
        rename_info = read_ui_for_rename()

        if mode_type == mode_all:

            rename_chain = validate()
            rename_chain_dict = rename_all(rename_chain, *rename_info)
            apply_rename_all(rename_chain_dict)


        elif mode_type == mode_one:

            current_basename = rename_info[3].strip()

            if not state["chain"]:                  # initiate one by one renaming state

                state["chain"] = validate()
                state["position"] = 0
                state["last_basename"] = current_basename
                state["run_index"] = 1
                index = 1
                cmds.button(skip_button, edit=True, enable=True)
                            

            else:                                   # continue renaming within the state

                sel = cmds.ls(selection=True, type="joint")
                expected = state["chain"][state["position"]]

                if len(sel) != 1 or sel[0] != expected:
                    cmds.select(expected, replace=True)
                    cmds.warning("Automatically re-selected next joint.")

                
                if not rename_info[5]:
                    index = 1
                else:
                    if state["last_basename"] != current_basename:
                        state["last_basename"] = current_basename
                        state["run_index"] = 1
                    else:
                        state["run_index"] += 1
                    index = state["run_index"]

            rename_dict = rename_one(state["chain"], state["chain"][state["position"]], *rename_info, index)
            apply_rename_one(rename_dict)
            state["position"] += 1

            if state["position"] >= len(state["chain"]):    # finish and exit state

                state["chain"].clear()
                state["position"] = 0
                cmds.button(skip_button, edit=True, enable=False)
                cmds.warning("Reached end of joint chain, tool reset.")
            else:                                           # select next joint
                cmds.select(state["chain"][state["position"]], replace=True)

            if not rename_info[6]:                          # clear user basename input
                cmds.textFieldGrp(basename_field, edit=True, text="")

        else: 
            raise RuntimeError("Internal error: no mode set.")


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

    mode_menu = cmds.optionMenu(
        label="Mode",
        width=half,
        changeCommand=update_mode_status)
    cmds.menuItem(label=mode_one)
    cmds.menuItem(label=mode_all)

    cmds.separator(height=separator_padding, style="none")

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
    
    endjoint_cb = cmds.checkBox(
        label="End Joint Naming",
        width=half,
        value=True,
        ann="Auto-name last joint in the chain with be_ etc."
    )
        
    cmds.setParent("..")
    cmds.setParent("..")

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

