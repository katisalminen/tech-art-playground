'''
EYE CONTROL CREATION HELPER TOOL

- Create two control circles for each eye + locator parent that also controls blink and head follow attribute
- Position the control curves in relation to the character's eyes
- Make each eye circle follow their control's movement - point constraint? Need to research
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

blink_info = {"min": -10, "max": 10, "name": "Blink", "shortname": "b"} # blink attribute
follow_info = {"min": 0, "max": 1, "name": "Follow", "shortname": "f"} # head follow attribute

# validate selection
def validate():
    sel = cmds.ls(sl=True, type="joint", sn=True)
    if not sel or len(sel) != 2:
        raise RuntimeError("Please select two eye joints.")
# check for other edge cases resulting in errors and safeguard against them!!


# create eye control curves: two eye circles + parent locator
def create_shapes():
    controls = {}
    for entry in ctrl_info:
        if "x" in entry:
            c = cmds.circle(c=(entry["x"], 0, 0), r=2.5, ch=False, n=f"anim_{entry["side"]}_01")[0]
        else:
            c = cmds.spaceLocator(n=entry["name"])[0]
            cmds.setAttr(f"{c}.localScaleY", 2.5)
            for n in ("l", "r"):
                cmds.addAttr(
                    ln=f"{blink_info["name"]} {n}", 
                    sn=f"{blink_info["shortname"]}_{n}", 
                    at="float", 
                    dv=0, 
                    min=blink_info["min"], 
                    max=blink_info["max"])
            cmds.addAttr(
                ln=f"{follow_info["name"]}", 
                sn=f"{follow_info["shortname"]}", 
                at="float", 
                dv=1, 
                min=follow_info["min"], 
                max=follow_info["max"])
        cmds.xform(c, centerPivots=True)
        cmds.setAttr(f"{c}.overrideEnabled", 1)
        cmds.setAttr(f"{c}.overrideRGBColors", 0)
        cmds.setAttr(f"{c}.overrideColor", entry["color"])
        for value in ("sx", "sy", "sz", "v"):
            cmds.setAttr(f"{c}.{value}", lock=True, keyable=False, channelBox=False)
        controls[entry["id"]] = c
    return controls

# position controls in relation to eyes and connect them
def position_controls(controls: dict):
    cmds.parent([controls["ecl"], controls["ecr"]], controls["ecp"])






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
        validate()
        controls = create_shapes()
        position_controls(controls)
        eye_rotation()
        implement_follow()
        create_blink()
        fleshy_eyes()
        



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