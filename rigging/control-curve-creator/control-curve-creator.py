
# CONTROL CIRCLE -- start of control creation tool

import re
import functools as ft
import maya.cmds as cmds
    




# create control curve

def create_control():

    # selection: 1 item, multiple, or none

    sel = cmds.ls(selection=True)
    joint = None

    if not sel:
        mode = "default"

    elif len(sel) == 1:
        joint = sel[0]

        if cmds.nodeType(joint) != "joint":
            raise RuntimeError("Please select exactly one joint, or nothing.")
        
        # check for default Maya joint naming
        short_name = joint.split(":")[-1]
        if re.match(r"^joint\d+$", short_name):
            raise RuntimeError("" \
            f"Joint '{joint}' uses Maya default naming - please rename."
            )
        
        mode = "snap"

    else:
        raise RuntimeError(f"Multiple items selected: {sel}")
    
    return mode

    # create control

    ctrl = cmds.circle(nr=(0, 1, 0), r=20, ch=False)[0]

    shapes = cmds.listRelatives(ctrl, shapes=True, fullPath=True) or []
    if not shapes:
        raise RuntimeError(f"No shape found under control: {ctrl}")

    shape = shapes[0]

    # rename control

    if mode == "default":
        new_name = increment_name("anim_control")
        ctrl = cmds.rename(ctrl, new_name)

    elif mode == "snap":
        if short_name.startswith("bn_"):
            ctrl = cmds.rename()

    else:
        raise RuntimeError("Invalid mode for renaming.")
    
    # create offset group


    # if joint selected, snap offset group to joint, lock offset group attributes

    
    

    # enable drawing overrides
    if not shape or not cmds.objExists(shape):
        raise RuntimeError(f"Shape node not found: {shape}")
    
    cmds.setAttr(f"{shape}.overrideEnabled", 1)
    cmds.setAttr(f"{shape}.overrideRGBColors", 0)
    cmds.setAttr(f"{shape}.overrideColor", 13) # red


# name control curve
# lock and hide scale and visibility

# create control group
# name control group

# if mode = snap, snap control group pivot to joint pivot
# lock control group transforms, don't freeze


###########################################


shape = ""
mode = ""
joint_name = ""


# mode definer
def validate():
    sel = cmds.ls(sl=True,type="joint")

    if len(sel) > 1:
        raise RuntimeError("Multiple joints selected.")
    
    elif len(sel) == 1:
        short_name = sel[0].split(":")[-1]

        if re.match(r"^joint\d+$", short_name):
            cmds.warning(
            f"Selection '{sel[0]}' uses Maya default naming - please rename."
            )
        
        mode = "snap"

    else:
        short_name = None
        mode = "default"


    return mode, short_name

### shape functions

def create_circle():
    return cmds.circle(nr=(0, 1, 0), r=20, ch=False)[0]
def create_square():
    pass
def create_triangle():
    pass
def create_box():
    pass
def create_arrow():
    pass
def create_cross():
    pass

### control shape namer

def increment_name(base_name: str, start: int = 1, pad: int = 2) -> str:
    i = start
    
    while True:
        candidate = f"{base_name}_{i:0{pad}d}"
        if not cmds.objExists(candidate):
            break
        i += 1
    return candidate


def ctrl_name(mode, ctrl, joint_name):

    if mode == "default":
        new_name = increment_name("anim_control")

    elif mode == "snap":
        if joint_name.startswith("bn_"):
            basename = joint_name.replace("bn_", "anim_", 1)
        else:
            basename = f"anim_{joint_name}"

        if not cmds.objExists(basename):
            new_name = basename
        else:
            new_name = increment_name(basename)
            
    else:
        raise RuntimeError(f"Invalid mode: {mode}")
    
    cmds.rename(ctrl, new_name)
    
    return new_name

### control curve registry: labels and functions

ctrl_registry = [

[("Circle", create_circle), 
("Square", create_square), 
("Triangle", create_triangle)],

[("Box", create_box), 
("Arrow", create_arrow), 
("Cross", create_cross)]

]


def showUI():

### UI style

    w_id = "ccc"
    w_title = "Control Curve Creator"
    w_width = 250
    w_height = 170
    w_pad = w_width//12
    gap = w_pad//4
    w_content = w_width - w_pad*2
    half = w_content//2

    def sep():
        cmds.separator(h=gap, style="none")
    
    def par():
        cmds.setParent("..")


### button functions

    def onClose(*args):
        cmds.deleteUI(w_id)

    def onClick(label, create_fn, *args):

        mode, joint_name = validate()
        print(f"\nControl creator mode: {mode}, joint name: {joint_name}")

        ctrl = create_fn()
        print(f"Shape created: {label} with function '{create_fn}'")

        name = ctrl_name(mode, ctrl, joint_name)
        print(f"Shape name: {name}")

        # create control group
        # enable drawing overrides
        # if joint selected, snap offset group to joint, lock offset group attributes





### curve creation
    
    def create_control(control_id: str):

        pass            

### create window

    if cmds.window("ccc",exists=True):
        cmds.deleteUI("ccc")

    cmds.window(w_id, t=w_title, wh=[w_width, w_height], s=False)
    cmds.showWindow(w_id)

    cmds.columnLayout(adj=True, columnOffset=["both", w_pad])
    sep()
    sep()

    cmds.rowLayout(adj=True,nc=3)

    cmds.columnLayout(adj=True, w=(half-gap))

    for c in ctrl_registry[0]:
        cmds.button(l=c[0],c=ft.partial(onClick, c[0], c[1]))
        sep()

    par()
    cmds.columnLayout(adj=True, w=gap)

    par()
    cmds.columnLayout(adj=True, w=(half-gap))
    for c in ctrl_registry[1]:
        cmds.button(l=c[0],c=ft.partial(onClick, c[0], c[1]))
        sep()

    par()
    par()

    sep()
    side_dd = cmds.optionMenuGrp(l="Side", cw=(1,half//4),ann="Affects drawing overrides")
    cmds.menuItem(l="Auto")
    cmds.menuItem(l="Center")
    cmds.menuItem(l="Left")
    cmds.menuItem(l="Right")

    sep()
    sep()
    cmds.button(l="Close",c=onClose)

showUI()






