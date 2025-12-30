
# CONTROL CIRCLE

# import cmds + maya check

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


def build_control_circle():
    ensure_maya()

    # joint selected y/n?
    # control name, joint or default?


    # create circle

    ctrl = cmds.circle(nr=(0, 1, 0), r=20, ch=False)[0]

    shapes = cmds.listRelatives(ctrl, shapes=True, fullPath=True) or []
    if not shapes:
        raise RuntimeError(f"No shape found under control: {ctrl}")

    shape = shapes[0]

    # rename circle

    # create offset group


    # if joint selected, snap offset group to joint, lock offset group attributes

    # if no joint selection, default name

    ctrl = cmds.rename(ctrl, "anim_circle_01")
    

    # enable drawing overrides
    if not shape or not cmds.objExists(shape):
        raise RuntimeError(f"Shape node not found: {shape}")
    
    cmds.setAttr(f"{shape}.overrideEnabled", 1)
    cmds.setAttr(f"{shape}.overrideRGBColors", 0)
    cmds.setAttr(f"{shape}.overrideColor", 13) # red


build_control_circle()


