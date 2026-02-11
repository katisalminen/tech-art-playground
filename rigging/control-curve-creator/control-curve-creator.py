
import functools as ft
import maya.cmds as cmds

shape = ""
mode = ""
joint_name = ""

side_colors = {
    "Center": 13,
    "Left": 17,
    "Right": 18
}

side_labels = ["Auto","Center","Right","Left"]

# mode definer
def validate():
    sel = cmds.ls(sl=True,type="joint",sn=True)
    mode = "default" if not sel else "snap"

    return mode, sel

# shape functions
def create_circle(s):
    return cmds.circle(nr=(0, 1, 0), r=s, ch=False)[0]
def create_square(s):
    return cmds.curve(d=1, p=[(-s,0,s), (s,0,s), (s,0,-s), (-s,0,-s), (-s,0,s)])
def create_triangle(s):
    return cmds.curve(d=1, p=[(0,0,-s), (-s,0,s), (s,0,s), (0,0,-s)])
def create_box(s):
    s *= 0.75
    v = [
        (-s, -s, -s),(-s, -s,  s),
        ( s, -s,  s),( s, -s, -s),
        (-s,  s, -s),(-s,  s,  s),
        ( s,  s,  s),( s,  s, -s)]
    path = [0, 1, 2, 3, 0, 4, 5, 1, 2, 6, 5, 4, 7, 3, 2, 6, 7]
    pts = [v[i] for i in path]
    return cmds.curve(d=1, p=pts)
def create_arrow(s):
    s *= 0.5
    return cmds.curve(
        d=1,
        p=[
            (-1*s, 0,  3*s),( 1*s, 0,  3*s),
            ( 1*s, 0,  0*s),( 2*s, 0,  0*s),
            ( 0  , 0, -3*s),(-2*s, 0,  0*s),
            (-1*s, 0,  0*s),(-1*s, 0,  3*s)])

def create_cross(s):
    s *= 0.5
    return cmds.curve(
        d=1,
        p=[
            ( 1*s, 0, -3*s),(-1*s, 0, -3*s),
            (-1*s, 0, -1*s),(-3*s, 0, -1*s),
            (-3*s, 0,  1*s),(-1*s, 0,  1*s),
            (-1*s, 0,  3*s),( 1*s, 0,  3*s),
            ( 1*s, 0,  1*s),( 3*s, 0,  1*s),
            ( 3*s, 0, -1*s),( 1*s, 0, -1*s),
            ( 1*s, 0, -3*s)])


# control curve registry: labels and functions
ctrl_registry = [

[("Circle", create_circle), 
("Square", create_square), 
("Triangle", create_triangle)],

[("Box", create_box), 
("Arrow", create_arrow), 
("Cross", create_cross)]

]

## lock transforms
def lock_trs(node):
    for attr in ("tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"):
        cmds.setAttr(f"{node}.{attr}", lock=True)

## lock and hide scale and visibility
def lock_hide_sv(node):
    for attr in ("sx", "sy", "sz", "v"):
        cmds.setAttr(
            f"{node}.{attr}",
            lock=True,
            keyable=False,
            channelBox=False
        )

### control shape naming
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
        basename = joint_name.replace("bn_", "anim_", 1) if joint_name.startswith("bn_") else f"anim_{joint_name}"

        if not cmds.objExists(basename):
            new_name = basename
        else:
            new_name = increment_name(basename)
            
    else:
        raise RuntimeError(f"Invalid mode: {mode}")
    
    cmds.rename(ctrl, new_name)
    
    return new_name



### offset group
def create_offset_group(ctrl, mode, sel):
    os_group = cmds.group(ctrl, n=f"{ctrl}_offset")

    if mode == "snap":
        constr = cmds.parentConstraint(sel, os_group, mo=False)
        cmds.delete(constr)
        rz = cmds.getAttr(f"{os_group}.rz")
        cmds.setAttr(f"{os_group}.rz", rz + 90.0)
        lock_trs(os_group)

    return os_group


### drawing overrides
def resolve_color(ctrl, side_token):
    if side_token != "Auto":
        return side_colors[side_token]
    
    tx = cmds.xform(ctrl, q=True, t=True, ws=True)[0]

    EPS = 1e-4
    if abs(tx) <= EPS:
        resolved = "Center"
    elif tx > 0:
        resolved = "Left"
    else:
        resolved = "Right"
    return side_colors[resolved]

def set_drawing_or(ctrl, side_token):
    shapes = cmds.listRelatives(ctrl, shapes=True, fullPath=True) or []
    if not shapes:
        raise RuntimeError(f"No shape found under control: {ctrl}")
    shape = shapes[0]

    color_id = resolve_color(ctrl, side_token)

    cmds.setAttr(f"{shape}.overrideEnabled", 1)
    cmds.setAttr(f"{shape}.overrideRGBColors", 0)
    cmds.setAttr(f"{shape}.overrideColor", color_id)

### control set-up: holds all control creation related functions
def ctrl_setup(create_fn, scale_token, mode, joint, side_token):
    ctrl = create_fn(scale_token)
    short_name = joint.split(":")[-1] if mode == "snap" else []
    name = ctrl_name(mode, ctrl, short_name)
    create_offset_group(name, mode, joint)
    set_drawing_or(name, side_token)
    return name
        

# WINDOW
def showUI():

### UI style

    w_id = "ccc"
    w_title = "Control Curve Creator"
    w_width = 250
    w_height = 225
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

    def onClick(create_fn, *args):
        side_token = cmds.optionMenuGrp(side_dd, query=True, value=True)
        scale_token = cmds.floatSlider(scale_slider, query=True, value=True)
        mode, joint_list = validate()
        if mode == "snap":
            ctrl_list = []
            for joint in joint_list:
                ctrl_list += ctrl_setup(create_fn, scale_token, mode, joint, side_token)
        else:
            joint = []
            ctrl_setup(create_fn, scale_token, mode, joint, side_token)

    def is_locked():
        cmds.getAttr(f"")

    def onFreeze(*args):
        sel = cmds.ls(sl=True, long=True)
        result = []

        if not sel:
            return
        else:
            for node in sel:
                curves = cmds.listRelatives(node, shapes=True, type="nurbsCurve")
                if curves:
                    result.append(node)
                else:
                    cmds.warning("No valid selection.")
                    return

        check = {"t": False, "r": False, "s": False}
        for attr in ("tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"):
            letter = attr[0]
            current = check[letter]
            check[letter] = cmds.getAttr(f"{result}.{attr}", lock=True) if not current else True
            
        for attr in check:
            cmds.makeIdentity(result, a=True, **attr) if attr else pass
        

        # , "rx", "ry", "rz", "sx", "sy", "sz"):
        # loop through attributes
        # if not locked, freeze transformations, otherwise pass


    def onMirror(*args):
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
    cmds.columnLayout(adj=True, w=half-gap)

    for c in ctrl_registry[0]:
        cmds.button(l=c[0],c=ft.partial(onClick, c[1]))
        sep()

    par()
    cmds.columnLayout(adj=True, w=gap)

    par()
    cmds.columnLayout(adj=True, w=(half-gap))
    for c in ctrl_registry[1]:
        cmds.button(l=c[0],c=ft.partial(onClick, c[1]))
        sep()

    par()
    par()
    sep()

    side_dd = cmds.optionMenuGrp(
        l="Side", 
        cw=(1,half//4),
        ann="Affects drawing overrides")
    for item in side_labels:
        cmds.menuItem(l=item)
    sep()

    cmds.rowLayout(adj=True, nc=2)
    cmds.columnLayout(adj=True)
    cmds.text(l="Control Size")
    par()
    cmds.columnLayout(adj=True)
    scale_slider = cmds.floatSlider(min=5.0, max=50.0, v=15.0, w=half)
    par()
    par()
    sep()

    cmds.rowLayout(adj=True, nc=3)
    cmds.columnLayout(adj=True, w=half-gap)
    freeze_b = cmds.button(l="Freeze",c=onFreeze)
    par()
    cmds.columnLayout(adj=True,w=gap)
    par()
    cmds.columnLayout(adj=True,w=half-gap)
    mirror_b = cmds.button(l="Mirror",c=onMirror)
    par()
    par()
    sep()

    cmds.button(l="Close",c=onClose)

showUI()






