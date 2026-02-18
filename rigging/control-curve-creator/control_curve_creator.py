
import functools as ft
import maya.cmds as cmds

shape = ""
mode = ""
joint_name = ""
attr = ["Translate", "Rotate", "Scale"]

side_colors = {
    "Center": 13,
    "Left": 17,
    "Right": 18
}

side_labels = ["Auto","Center","Right","Left"]

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
("Cross", create_cross)]]

# mode definer
def validate_mode():
    sel = cmds.ls(sl=True,type="joint",sn=True)
    mode = "default" if not sel else "snap"
    return mode, sel

# freeze, lock, hide master function
def lock_hide_freeze(do_lock, do_hide, freeze, target, trs):
    if not target:
        return
    
    if isinstance(trs, str):
        trs = ["t", "r", "s"] if trs == "all" else [trs.lower()]
    trs = list(dict.fromkeys(
        t[0] if len(t) > 1 else t 
        for t in trs))
    allowed_trs = {"t", "r", "s"}
    trs = [t for t in trs if t in allowed_trs]
    if not trs:
        raise RuntimeError("Invalid transformation token.")
                
    for tform in trs:
        if freeze:
            cmds.makeIdentity(target, a=True, **{tform: True})
        for letter in ("x", "y", "z"):
            if do_lock:
                cmds.setAttr(
                    f"{target}.{tform}{letter}",
                    lock=True
                    )
            if do_hide:
                cmds.setAttr(
                    f"{target}.{tform}{letter}",
                    channelBox=False,
                    keyable=False
                    )
                
def check_transforms(target: str, trs: str):
    tform = trs.lower()
    tform_short = tform[0]
    basenumber = 0 if tform_short in ("t", "r") else 1

    # check unfrozen values, locked, hidden+keyable

    transforms = []
    for axis in ("X", "Y", "Z"):
        info = {
            "freeze": True if cmds.getAttr(f"{target}.{tform}{axis}") == basenumber else False
                                   
        }

        if cmds.getAttr(f"{target}.{tform}{axis}") != basenumber:
            cmds.select(target, replace=True)
            return
                
    return 


        
# CTRL CURVE CREATION FUNCTIONS
## control shape naming
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

## offset group
def create_offset_group(ctrl, mode, sel):
    os_group = cmds.group(ctrl, n=f"{ctrl}_offset")

    if mode == "snap":
        constr = cmds.parentConstraint(sel, os_group, mo=False)
        cmds.delete(constr)

    return os_group

## drawing overrides
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

## control set-up: holds all control creation related functions
def ctrl_setup(create_fn, scale_token, mode, joint, side_token):
    ctrl = create_fn(scale_token)
    short_name = joint.split(":")[-1] if mode == "snap" else []
    name = ctrl_name(mode, ctrl, short_name)
    create_offset_group(name, mode, joint)
    set_drawing_or(name, side_token)
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
                raise RuntimeError("Select a control curve or its control group.")
            candidates = []
            for candidate in parents:
                if "offset" in candidate:
                    candidates.append(candidate)
            if len(candidates) > 1:
                raise RuntimeError(f"Error: {name} has multiple offset groups.")
            if not candidates:
                raise RuntimeError("Selected curve has no offset group!")
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
            lock_hide_freeze(False, False, True, member, to_freeze)
        
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
            check_transforms(item, trs)

        sel_status = []
        for object in sel:
            sel_status.append({
                "lock": cmds.getAttr(object, lock=False),
                "hidden": cmds.getAttr(object, channelBox=False)
                })

        for (object, info) in zip(sel, sel_status):
            lock_hide_freeze(info["lock"], info["hidden"], False, object, trs)
        

        # feed first letter as parameter to function


                    

## create window

    if cmds.window(w_id,exists=True):
        cmds.deleteUI(w_id)

    cmds.window(w_id, t=w_title, wh=[w_width, w_height], s=False)
    cmds.showWindow(w_id)

    cmds.columnLayout(adj=True, columnOffset=["both", w_pad])
    sep(2)

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

    side_dd = cmds.optionMenuGrp(
        l="Side", 
        cw=(1,half//4),
        ann="Affects drawing overrides")
    for item in side_labels:
        cmds.menuItem(l=item)
    sep(1)

    cmds.rowLayout(adj=True, nc=2)
    cmds.columnLayout(adj=True)
    cmds.text(l="Control Size")
    par()
    cmds.columnLayout(adj=True)
    scale_slider = cmds.floatSlider(min=5.0, max=50.0, v=15.0, w=half)
    par2()
    sep(2)

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

    cmds.text(l="Lock & Hide Toggle")
    sep(1)
    cmds.rowLayout(nc=3)
    for b in attr:
        cmds.columnLayout(adj=True, w=(third-gap//2))
        cmds.button(l=b, c=ft.partial(onLHToggle, b))
        par()
    par()

    sep(2)
    cmds.button(l="Close",c=onClose)

show_ui()


