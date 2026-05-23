'''
EYE CONTROL CREATION HELPER TOOL

- Create two control circles for each eye + locator parent that also controls blink and head follow attribute
- Position the control curves in relation to the character's eyes
- Make each eye circle follow their control's movement
- Implement follow attribute: blend whether the head's movement moves the eye controls
- Blink attribute: rotation of eyelid bones for blinking animation
- Fleshy eyes: eye rotation slightly rotates eyelid bones
'''

import maya.cmds as cmds

# ctrl shape info -- for easier editing later
ctrl_info = [
    {"id": "ecl", "side": "l", "x": 4, "color": 17}, # left eye control
    {"id": "ecr", "side": "r", "x": -4, "color": 18}, # right eye control
    {"id": "ecp", "name": "anim_eyes01", "color": 13}, # eye parent control
]

# blink and follow attribute info for parent locator
attr_info = [
    {"name": "blink_l", "shortname": "b_l", "min": -10, "max": 10, "dv": 0},
    {"name": "blink_r", "shortname": "b_r", "min": -10, "max": 10, "dv": 0},
    {"name": "follow", "shortname": "f", "min": 0, "max": 1, "dv": 1}
]

# how far from eyes the control is created in the Z axis
# make configurable through UI with 40 as default value later!
move_distance = 40

# X world position checker
def check_x_pos(sel) -> list:
    return [cmds.xform(joint, q=True, t=True, ws=True)[0] for joint in sel]

# validate selection and return names of eye joints
def validate() -> list:
    sel = cmds.ls(sl=True, type="joint", sn=True)

    # check for 2 selected joints
    if not sel or len(sel) != 2:
        raise RuntimeError("Please select two eye joints.")
    
    # check for mirrored x position
    x_pos = check_x_pos(sel)
    mid_x = (x_pos[0] + x_pos[1])/2
    if abs(mid_x) > 1e-4:
        raise RuntimeError("Eye joints must me symmetrical around world X.")

    return sel

# create eye control curves: left eye curve, right eye curve, parent locator
def create_shapes() -> list:
    controls = []
    for entry in ctrl_info:
        if "x" in entry:
            c = cmds.circle(
                c=(entry['x'], 0, 0), 
                r=2.5, 
                ch=False, 
                n=f"anim_{entry['side']}_01"
                )[0]
        else:
            c = cmds.spaceLocator(n=entry["name"])[0]
            cmds.setAttr(f"{c}.localScaleY", 2.5)
            for n in ["px", "py", "pz", "sx", "sy", "sz"]:
                cmds.setAttr(
                    f"{c}Shape.l{n}",
                    keyable=False,channelBox=False,lock=True)
            
            for attr in attr_info:
                longname=f"{attr['name']}"
                cmds.addAttr(
                    ln=longname,sn=f"{attr['shortname']}",
                    at="float",dv=attr['dv'],
                    min=attr["min"],max=attr["max"])
                cmds.setAttr(f"{c}.{longname}",channelBox=True)
        
        cmds.xform(c, centerPivots=True)
        cmds.setAttr(f"{c}.overrideEnabled", 1)
        cmds.setAttr(f"{c}.overrideRGBColors", 0)
        cmds.setAttr(f"{c}.overrideColor", entry["color"])
        for value in ("sx", "sy", "sz", "v"):
            cmds.setAttr(
                f"{c}.{value}",
                lock=True,keyable=False,channelBox=False)
            
        controls.append(c) # list: ecl, ecr, ecp
    return controls

# position controls in relation to eyes and connect them
def position_controls(ecl, ecr, ecp, ej: list):

    # check joint sides
    x_pos = check_x_pos(ej)
    left_joint = ej[0] if x_pos[0] > 0 else ej[1]
    right_joint = ej[1] if x_pos[1] < 0 else ej[0]

    # snap eye controls to joints
    for ctrl, joint in zip([ecl, ecr], [left_joint, right_joint]):
        eye_control_constraint = cmds.parentConstraint(joint, ctrl, mo=False)
        cmds.delete(eye_control_constraint)
        cmds.setAttr(f"{ctrl}.rotate", 0, 0, 0)
        cmds.makeIdentity(ctrl, a=True, t=True)
    
    # move locator, parent eye controls to it
    locator_constraint = cmds.parentConstraint(ecl, ecr, ecp, mo=False)
    cmds.delete(locator_constraint)
    cmds.parent([ecl, ecr], ecp)
    cmds.setAttr(f"{ecp}.translateZ", move_distance)
    cmds.makeIdentity(ecp, a=True, t=True)

    # aim constrain
    cmds.aimConstraint(ecl, left_joint, mo=True)
    cmds.aimConstraint(ecr, right_joint, mo=True)

def show_ui():
    
    w_id = "ect"
    w_title = "Eye Control Tool"
    w_width = 250
    w_height = 300
    w_pad = w_width//16
    gap = w_pad//4
    w_content = w_width - w_pad*2
    half = w_content//2
    third = w_content//3

    def sep(n):
        cmds.separator(h=(gap*n), style="none")
    def par():
        cmds.setParent("..")
    def par2():
        cmds.setParent("..")
        cmds.setParent("..")

    def onCreate(*args):
        eye_joints = validate() # check selection
        ecl, ecr, ecp = create_shapes() # left, right, and parent controls as strings
        position_controls(ecl, ecr, ecp, eye_joints) # position and parent controls
        # eye_rotation()
        # implement_follow()
        # create_blink()
        # fleshy_eyes()
        



    if cmds.window(w_id,exists=True):
        cmds.deleteUI(w_id)

    cmds.window(w_id, t=w_title, wh=[w_width, w_height], s=False)
    cmds.showWindow(w_id)

    cmds.columnLayout(adj=True, columnOffset=["both", w_pad])
    sep(2)
    cmds.checkBox(l="Fleshy Eyes", v=True, ann="Enable or disable Fleshy Eyes.")

    sep(2)

    cmds.button(
        l="Create Controls", c=onCreate,
        ann="Select two eye joints to start.")


show_ui()