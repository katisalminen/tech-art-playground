
import maya.cmds as cmds

def run():

    sel = cmds.ls(selection=True, type="joint", long=True)
    children = []
    found = False

    if not sel:
        raise RuntimeError("Select a joint.")

    for n in sel:
        c = cmds.listRelatives(n, type="joint", ad=True, f=True) or []
        children.extend(c)

    joint_hierarchy = sel + children

    def get_orients(n):
        x = cmds.getAttr(f"{n}.rotateX")
        y = cmds.getAttr(f"{n}.rotateY")
        z = cmds.getAttr(f"{n}.rotateZ")
        return x + y + z

    for n in joint_hierarchy:
        xyz = get_orients(n)
        if xyz != 0:
            cmds.select(n)
            found = True
            break

    if found:
        warn = "Non-zero rotation encountered."

    cmds.warning(warn if found else "All clear!")

