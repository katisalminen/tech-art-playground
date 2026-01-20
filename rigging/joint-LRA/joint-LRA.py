
'''
JOINT ROTATION AXES VISIBILITY TOOL

V1: callable functions

V2: UI wrapper that actually uses the functions

'''


import maya.cmds as cmds


mode = "all"
# or "single", "hierarchy"

action = 1
# or 0


def toggle(mode: str, action: int):

    if mode not in ("single", "hierarchy", "all"):
        raise RuntimeError(f"Invalid mode: '{mode}'.")
    
    if action not in (0, 1):
        raise RuntimeError(f"Invalid action: '{action}'.")       
     
    if mode == "all":
        joint_list = cmds.ls(type="joint", long=True)
        if not joint_list:
            raise RuntimeError("No joints in scene.")
        
    else:
        
        joint_list = []

        if mode == "hierarchy":
            joint_list = cmds.listRelatives(allDescendents=True, fullPath=True)
            if not joint_list:
                raise RuntimeError("Selected hierarchy has no joints.")
            
        sel = cmds.ls(selection=True, long=True, type="joint")
        joint_list.append(*sel)

        if mode == "single" and not sel:
            raise RuntimeError("Please make a selection.")

    for j in joint_list:
        cmds.setAttr(f"{j}.displayLocalAxis", action)






    

