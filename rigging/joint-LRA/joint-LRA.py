
import maya.cmds as cmds


mode = "hierarchy"
# "single", "hierarchy", or "all"

vis = 1
# 0 or 1


def toggle(mode: str, vis: int):

    if mode not in ("single", "hierarchy", "all"):
        raise RuntimeError(f"Invalid mode: '{mode}'.")
    
    if vis not in (0, 1):
        raise RuntimeError(f"Invalid visibility: '{vis}'.")       
     
    if mode == "all":
        joint_list = cmds.ls(type="joint", long=True)
        if not joint_list:
            raise RuntimeError("No joints in scene.")
        
    else:
        
        joint_list = []
        sel = cmds.ls(selection=True, long=True)
        sel_joints = cmds.ls(selection=True, long=True, type="joint")

        if mode == "hierarchy":
            if not sel:
                raise RuntimeError("Please make a selection.")

            joint_list = cmds.listRelatives(sel, allDescendents=True, fullPath=True, type="joint")
            if not joint_list:
                joint_list = sel_joints
            else:
                joint_list.extend(sel_joints)
            if not joint_list:
                raise RuntimeError("Selection should contain joints.")
            
        elif mode == "single":
            if not sel_joints:
                raise RuntimeError("Please select a joint or joints.")
            joint_list = sel_joints
        
        else:
            raise RuntimeError(f"Internal error: invalid mode '{mode}'.")
        
    for j in joint_list:
        cmds.setAttr(f"{j}.displayLocalAxis", vis)

    print(f"{len(joint_list)} joint LRA set to {vis}.")

toggle(mode, vis)
