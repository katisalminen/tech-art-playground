import maya.cmds as cmds


'''
EYE CONTROL CREATION HELPER TOOL

- Create two control circles for each eye + locator parent that also controls blink and head follow attribute
- Position the control curves in relation to the character's eyes
- Make each eye circle follow their control's movement - point constraint? Need to research
- Implement follow attribute: blend whether the head's movement moves the eye controls
- Blink attribute: rotation of eyelid bones for blinking animation
- Fleshy eyes: eye rotation slightly rotates eyelid bones
'''


ctrl_registry = []
letters = ['l', 'r', 'p']
coords = [4, -4, 0]
colors = [17, 18, 13]

for l, c, rgb in zip(letters, coords, colors):
    entry = {"id": f"ec{l}", "x": c, "name": f"anim_{l}_eye01", "color": rgb}
    ctrl_registry.append(entry)

def create_ctrls(registry: list):

    shapes = []
    for item in registry:
        if "p" not in item['id']:
            s = cmds.circle(c=(item['x'], 0, 0), r=2.5, ch=False, n=item['name'])[0]
        else:
            s = cmds.spaceLocator(n=item['name'])[0]
            cmds.setAttr(f"{s}, localScaleY", 2.5)
            for side in ("l", "r"):
                token = f"b{side}"
                cmds.addAttr(ln=f"blink_{side}", sn=token, at="float", dv=0, min=10, max=(-10)) # adjust later
                cmds.setAttr(f"{item["name"]}.{token}", l=False, k=True, cb=False)
            cmds.addAttr(ln="follow", sn="f", at="float", dv=1, min=0, max=1)
            cmds.setAttr(f"{shapes[2]}.f", l=False, k=True, cb=False)
        shapes.append(s)

    for item in shapes:
        cmds.xform(item, centerPivots=True)
        cmds.setAttr(f"{item}.overrideEnabled", 1)
        cmds.setAttr(f"{item}.overrideRGBColors", 0)
        cmds.setAttr(f"{item}.overrideColor", item["color"])
        for v in ("sx", "sy", "sz", "v"):
            cmds.setAttr(f"{item}.{v}", lock=True, keyable=False, channelBox=False)

    cmds.parent([shapes[0], shapes[1]], shapes[2])
    cmds.select(shapes[2]["name"], r=True)

    return shapes
    




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