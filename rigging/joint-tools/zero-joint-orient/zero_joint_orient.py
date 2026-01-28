
import maya.cmds as cmds

def run():

    sel = cmds.ls(selection=True, type="joint", long=True)
    count = 0

    for n in sel:
        cmds.setAttr(f"{n}.jointOrientX", 0)
        cmds.setAttr(f"{n}.jointOrientY", 0)
        cmds.setAttr(f"{n}.jointOrientZ", 0)
        count += 1

    print(f"{count} joints zeroed out.")
