
# CONTROL CIRCLE -- start of control creation tool

import re

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None

def ensure_maya():
    if cmds is None:
        raise RuntimeError("This script must be run inside Maya.")
    try:
        cmds.about(version=True)
    except Exception:
        raise RuntimeError("Maya Python environment not initialized.")
    

# renaming helper

def get_unique_name(base_name: str, start: int = 1, pad: int = 2) -> str:
    i = start
    while True:
        candidate = f"{base_name}_{i:0{pad}d}"
        if not cmds.objExists(candidate):
            return candidate
        i += 1



def create_control():
    ensure_maya()

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
            f"Joint '{joint} uses Maya default naming - please rename."
            )
        
        mode = "joint"

    else:
        raise RuntimeError(f"Multiple items selected: {sel}")

    # create control

    ctrl = cmds.circle(nr=(0, 1, 0), r=20, ch=False)[0]

    shapes = cmds.listRelatives(ctrl, shapes=True, fullPath=True) or []
    if not shapes:
        raise RuntimeError(f"No shape found under control: {ctrl}")

    shape = shapes[0]

    # rename control

    if mode == "default":
        new_name = get_unique_name("anim_control")
        ctrl = cmds.rename(ctrl, new_name)

    elif mode == "joint":
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


create_control()


