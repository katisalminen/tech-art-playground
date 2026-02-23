import maya.cmds as cmds


# create eye control curves: two eye circles + parent goggles
def create_eye_ctrl():
    ecl = cmds.circle(c=(4, 0, 0), r=2.5, ch=False, n="anim_l_eye01")[0]
    ecr = cmds.circle(c=(-4, 0, 0), r=2.5, ch=False, n="anim_r_eye01")[0]
    ecp = cmds.circle(r=9, ch=False, n="anim_eyes01")[0]
    cv1 = [f"{ecp}.cv[1]", f"{ecp}.cv[5]"]
    cv2 = [f"{ecp}.cv[0]", f"{ecp}.cv[2]",
        f"{ecp}.cv[4]", f"{ecp}.cv[6]"]
    cmds.scale(1, 0.3, 1, cv1)
    cmds.scale(1, 0.8, 1, cv2)
    cmds.parent([ecl, ecr], ecp)
    cmds.xform([ecl, ecr], centerPivots=True)
    for curve in (ecl, ecr, ecp):
        if "l" in curve:
            c_id = 17
        elif "r" in curve:
            c_id = 18
        else:
            c_id = 13
        cmds.setAttr(f"{curve}.overrideEnabled", 1)
        cmds.setAttr(f"{curve}.overrideRGBColors", 0)
        cmds.setAttr(f"{curve}.overrideColor", c_id)
        for v in ("sx", "sy", "sz", "v"):
            cmds.setAttr(f"{curve}.{v}", lock=True, keyable=False, channelBox=False)
    cmds.select(ecp, r=True)
    for bs in ("l", "r"):
        b_sn = f"b{bs}"
        cmds.addAttr(ln=f"blink_{bs}", sn=b_sn, at="float", dv=0, min=10, max=(-10)) # adjust these later!!
        cmds.setAttr(f"{ecp}.{b_sn}", l=False, k=True, cb=False)
    cmds.addAttr(ln="follow", sn="f", at="float", dv=1, min=0, max=1)
    cmds.setAttr(f"{ecp}.f", l=False, k=True, cb=False)
    return ecl, ecr, ecp


def ctrl_creation():
    eye_ctrl_l, eye_ctrl_r, eye_ctrl = create_eye_ctrl()



ctrl_creation()


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


    if cmds.window(w_id,exists=True):
        cmds.deleteUI(w_id)

    cmds.window(w_id, t=w_title, wh=[w_width, w_height], s=False)
    cmds.showWindow(w_id)

    cmds.columnLayout(adj=True, columnOffset=["both", w_pad])

show_ui()