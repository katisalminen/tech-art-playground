
import maya.cmds as cmds

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


def show_ui():

    def read_state(*args):
        value = cmds.intSlider(on_or_off, query=True, value=True)
        return value

    def onSelB(*args):
        toggle("single", read_state())

    def onHieB(*args):
        toggle("hierarchy", read_state())
    
    def onAllB(*args):
        toggle("all", read_state())

    def onClose(*args):
        cmds.deleteUI(window_id)


    window_id = "lra_toggle"
    window_title = "LRA Toggle"

    window_width = 180
    window_height = 200
    window_padding = 20
    window_content_width = window_width-window_padding*2
    big_separator = 20
    mini_separator = 5
    third = window_content_width//3

    if cmds.window(window_id, exists=True):
        cmds.deleteUI(window_id)

    cmds.window(
        window_id, 
        title=window_title, 
        widthHeight=(window_width, window_height),
        sizeable=False
        )
        
    cmds.columnLayout(columnOffset=["both", window_padding], adj=True)
    cmds.separator(height=big_separator, style="none")
    cmds.rowLayout(numberOfColumns=3)

    cmds.text(l="OFF", width=third)

    on_or_off = cmds.intSlider(minValue=0,maxValue=1, width=third)

    cmds.text(l="ON", width=third)

    cmds.setParent("..")
    cmds.separator(height=big_separator, style="none")

    selection_button = cmds.button(l="Toggle Selection", command=onSelB)
    cmds.separator(height=mini_separator, style="none")

    hierarchy_button = cmds.button(l="Toggle Hierarchy", command=onHieB)
    cmds.separator(height=mini_separator, style="none")

    all_button = cmds.button(l="Toggle All", command=onAllB)

    cmds.separator(height=big_separator, style="none")

    close_button = cmds.button(l="Close", command=onClose)

    cmds.showWindow(window_id)

show_ui()