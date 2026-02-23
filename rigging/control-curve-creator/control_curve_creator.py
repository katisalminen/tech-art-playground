
import functools as ft
import maya.cmds as cmds

shape = ""
mode = ""
joint_name = ""
attr = ["Translate", "Rotate", "Scale"]
side_colors = {
    "Center": 13,
    "Left": 17,
    "Right": 18 }
side_labels = ["Auto", "Center", "Right", "Left"]

# general runtimeError function
def error(criminal, words="Internal error with"):
    raise RuntimeError(f"{words} {criminal}.")

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
# left side buttons
[("Circle", create_circle), 
("Square", create_square), 
("Triangle", create_triangle)],
# right side buttons
[("Box", create_box), 
("Arrow", create_arrow), 
("Cross", create_cross)]]

# FREEZE, LOCK, HIDE ATTRIBUTES
## check what is frozen, locked, hidden to determine action
def check_transforms(target: str, trs: str) -> dict:
    tform = trs.lower()     # ensure input is lowercase
    tform_short = tform[0]  # first letter of input, should be t, r, or s
    basenumber = 0 if tform_short in ("t", "r") else 1      # 0 for t/r, 1 for s
    transforms = []         
    for axis in ("X", "Y", "Z"):
        name = f"{target}.{tform_short}{axis.lower()}"
        info = { # this is pretty scuffed but it works as intended even if ugly
            "frozen": True if abs((cmds.getAttr(name)) - basenumber) < 1e-6 else False,
            "unlocked": False if cmds.getAttr(name, lock=True) else True,
            "visible": False if cmds.getAttr(name, channelBox=True) else True,
            "keyable": True if cmds.getAttr(name, keyable=True) else False
        } 
        transforms.append(info)
    result = {key: all(d[key] for d in transforms) for key in transforms[0]}
    return result


# lock, hide, freeze master function
def lhf(do_freeze, do_lh, target, trs): # true, false, or none
    if not target:
        return
    if isinstance(trs, str):
        trs = ["t", "r", "s"] if trs == "all" else [trs.lower()]
    trs = list(dict.fromkeys(t[0] if len(t) > 1 else t for t in trs))
    allowed_trs = {"t", "r", "s"}
    trs = [t for t in trs if t in allowed_trs]
    if not trs:
        error("transformation token")

    for tform in trs:
        if do_freeze:
            cmds.makeIdentity(target, a=True, **{tform: True})
        for letter in ("x", "y", "z"):
            if do_lh is not None:
                cmds.setAttr(f"{target}.{tform}{letter}", keyable=not do_lh, channelBox=False)
                cmds.setAttr(f"{target}.{tform}{letter}", lock=do_lh)
                
# CTRL CURVE CREATION FUNCTIONS
## mode definer
def validate_mode():
    sel = cmds.ls(sl=True,type="joint",sn=True)
    mode = "default" if not sel else "snap"
    return mode, sel

## control shape naming
### index incrementing for unique names
def increment_name(base_name: str, start: int = 1, pad: int = 2) -> str:
    i = start
    while True:
        candidate = f"{base_name}_{i:0{pad}d}"
        if not cmds.objExists(candidate):
            break
        i += 1
    return candidate

### create and apply unique name
def ctrl_name(mode, ctrl, joint_name) -> str:
    if mode == "default":
        new_name = increment_name("anim_control")
    elif mode == "snap":
        basename = joint_name.replace("bn_", "anim_", 1) if joint_name.startswith("bn_") else f"anim_{joint_name}"
        if not cmds.objExists(basename):
            new_name = basename
        else:
            new_name = increment_name(basename)     
    else:
        error(mode, "Invalid mode:")
    cmds.rename(ctrl, new_name)
    return new_name

### offset group
def create_offset_group(ctrl, mode, sel) -> str:
    os_group = cmds.group(ctrl, n=f"{ctrl}_offset")
    if mode == "snap":
        constr = cmds.parentConstraint(sel, os_group, mo=False)
        cmds.delete(constr)
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
        error(ctrl, "No shape found under control:")
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
    cmds.setAttr(f"{name}.v", lock=True, keyable=False, channelBox=False)
    return name

# MIRROR FUNCTIONS
## mirror validation
def mirror_validate(sel: list) -> list:
    targets = []
    for name in sel:
        if "offset" in name:
            targets.append(name)
        else:
            parents = cmds.listRelatives(name, p=True, f=True)
            if not parents:
                error("selection: select a control curve or its control group.")
            candidates = []
            for candidate in parents:
                if "offset" in candidate:
                    candidates.append(candidate)
            if len(candidates) > 1:
                error(name, "Multiple offset groups:")
            if not candidates:
                error("", "Selected curve has no offset group!")
            else:
                targets.append(candidate)     
    return targets

## mirror name fix
def fix_mirror_naming(old, new) -> str:
    olds = (cmds.listRelatives(old, ad=True, f=True) or []) + [old]
    news = (cmds.listRelatives(new, ad=True, f=True) or []) + [new]
    if len(olds) != len(news):
        cmds.warning("Naming issue: check naming of mirrored objects.")
    og_side = "left" if "_l_" in olds[0] else "right"
    if og_side == "left":
        set_drawing_or(news[1], "Right")
        for a, b in zip(olds, news):
            newname = a.replace("_l_", "_r_")
            parent = cmds.rename(b, newname.split("|")[-1])
    elif og_side == "right":
        set_drawing_or(news[1], "Left")
        for a, b in zip(olds, news):
            newname = a.replace("_r_", "_l_")
            parent = cmds.rename(b, newname.split("|")[-1])
    return parent

# WINDOW
def show_ui():

## UI style
    w_id = "ccc"
    w_title = "Control Curve Creator"
    w_width = 260
    w_height = 270
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

## button functions
    def onClose(*args):
        cmds.deleteUI(w_id)

    def onClick(create_fn, *args):
        side_token = cmds.optionMenuGrp(side_dd, query=True, value=True)
        scale_token = cmds.floatSlider(scale_slider, query=True, value=True)
        mode, joint_list = validate_mode()
        if mode == "snap":
            ctrl_list = []
            for joint in joint_list:
                ctrl_list.append(ctrl_setup(create_fn, scale_token, mode, joint, side_token))
            cmds.select(ctrl_list, replace=True)
        else:
            joint = []
            ctrl_setup(create_fn, scale_token, mode, joint, side_token)

    def onFreeze(*args):
        sel = cmds.ls(sl=True, long=True)
        if not sel:
            return
        for node in sel:
            if not cmds.listRelatives(node, shapes=True, type="nurbsCurve"):
                cmds.warning("Invalid selection.")
                return
        for member in sel:
            to_freeze = []
            for letter in ("tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"):
                if cmds.getAttr(f"{member}.{letter}", lock=False):
                    to_freeze.append(letter)
            lhf(True, None, member, to_freeze)
        
    def onMirror(*args):
        sel = cmds.ls(sl=True, long=False)
        og_groups = mirror_validate(sel)
        new_groups = cmds.duplicate(og_groups, rr=True, rc=True)
        for old, new in zip(og_groups, new_groups):
            new_os_grp = fix_mirror_naming(old, new)
            mirror_grp = cmds.group(new_os_grp, n=f"{new_os_grp}_mirror")
            cmds.xform(mirror_grp, ws=True, rp=(0,0,0), sp=(0,0,0))
            cmds.setAttr(f"{mirror_grp}.sx", -1)

    def onLHToggle(trs, *args):
        sel = cmds.ls(sl=True, long=False)
        if not sel:
            return
        for item in sel:
            attrs = check_transforms(item, trs)
            if not attrs["frozen"]:
                cmds.select(item, replace=True)
                error(f"selection {item}: unfrozen {trs} value(s).")
            todo = all(attrs[k] for k in ("unlocked", "visible", "keyable"))
            lhf(False, todo, item, trs)

## create window
    if cmds.window(w_id,exists=True):
        cmds.deleteUI(w_id)

    cmds.window(w_id, t=w_title, wh=[w_width, w_height], s=False)
    cmds.showWindow(w_id)

    cmds.columnLayout(adj=True, columnOffset=["both", w_pad])
    sep(2)

### shape creation buttons
    cmds.rowLayout(adj=True,nc=3)
    cmds.columnLayout(adj=True, w=half-gap)

    for c in ctrl_registry[0]:
        cmds.button(l=c[0],c=ft.partial(onClick, c[1]))
        sep(1)

    par()
    cmds.columnLayout(adj=True, w=gap)

    par()
    cmds.columnLayout(adj=True, w=(half-gap))
    for c in ctrl_registry[1]:
        cmds.button(l=c[0],c=ft.partial(onClick, c[1]))
        sep(1)

    par2()
    sep(1)

### side dropdown menu: drawing override colors
    side_dd = cmds.optionMenuGrp(
        l="Side", 
        cw=(1,half//4),
        ann="Affects drawing overrides")
    for item in side_labels:
        cmds.menuItem(l=item)
    sep(1)

### curve scale slider
    cmds.rowLayout(adj=True, nc=2)
    cmds.columnLayout(adj=True)
    cmds.text(l="Control Size")
    par()
    cmds.columnLayout(adj=True)
    scale_slider = cmds.floatSlider(min=5.0, max=50.0, v=15.0, w=half)
    par2()
    sep(2)

### freeze and mirror buttons
    cmds.rowLayout(adj=True, nc=3)
    cmds.columnLayout(adj=True, w=half-gap)
    freeze_b = cmds.button(l="Freeze",c=onFreeze)
    par()
    cmds.columnLayout(adj=True,w=gap)
    par()
    cmds.columnLayout(adj=True,w=half-gap)
    mirror_b = cmds.button(l="Mirror",c=onMirror)
    par2()
    sep(2)

### lock and hide toggle buttons
    cmds.text(l="Lock & Hide Toggle")
    sep(1)
    cmds.rowLayout(nc=3)
    for b in attr:
        cmds.columnLayout(adj=True, w=(third-gap//2))
        cmds.button(l=b, c=ft.partial(onLHToggle, b))
        par()
    par()

### close button
    sep(2)
    cmds.button(l="Close",c=onClose)

show_ui()


