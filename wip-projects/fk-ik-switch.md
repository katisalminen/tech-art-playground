# FK/IK SWITCH

Reference:

https://www.youtube.com/watch?v=uzHn_4ByyjY&t=3306s


## FK AND IK JOINT CHAINS

duplicate shoulder joint hierarchy and delete finger

unparent from hierarchy, there should be 3 joints: shoulder, elbow, wrist

rename joints e.g. l_shoulder_IK

duplicate again, rename e.g. l_shoulder_FK etc.

-> these will be the two joint chains for IK and FK


## CONNECT NEW JOINTS

to make the new joints move the arm:

- parent constrain them to the original joint

- -> select IK shoulder, FK shoulder, and original shoulder

- -> parent constrain (maintain offset off)

repeat for all 3 joints

## FK CONTROLS

place circles on joints, color, freeze transform + history

create offset groups, center pivots, rename OS_* etc.

to rotate, select OS group and joint, modify -> match transformations

(may need to rotate 90 degrees)

edit curves to match model better

parent wrist OS group to elbow ctrl, elbow OS group to shoulder ctrl

parent constrain controls to their respective FK bones (maintain offset on)

## IK CONTROLS

create controls for IK wrist and FK/IK blending (e.g. box and arrow)

place IK control on wrist w offset group

place switch control near wrist wherever suitable

create IK/FK switch attribute on the switch control (IK_FK_Switch etc.)

create pole vector control

create IK handle (rotate-plane)

parent IK handle to wrist IK control

!! at this point when moving FK or IK controls, the real arm should follow in between the two

## IK FK SWITCH

open node editor (window -> node editor)

add in switch control and the three parent constraints (shoulder, elbow, wrist)

connect IK FK Switch attribute to IKW1 attributes on parent constraints

create reverse node, rename it

connect IK FK Switch on switch control to input X on reverse node

connect output X on reverse node to each FKW0 attribute on the parent constraints

(this will ensure that when IK weight is 1, FK will always be opposite, e.g. 0)

drag controls to node editor: IK wrist offset and pole vector, FK shoulder offset

connect IK FK Switch on switch control to IK wrist offset and pole vector visibility

connect output X on reverse node to FK shoulder offset visibility

orient constrain IK wrist control to IK wrist bone

point constrain main wrist bone to FK/IK switch control


## FINGER JOINTS FOLLOW

https://www.youtube.com/watch?v=3vJxXLw16Ak&t=1004s around 11:00

to make finger joints follow whether IK or FK is active:

- create an offset group and match its transforms to wrist bone

- parent finger joints to offset group

- parent constrain wrist bone to offset group