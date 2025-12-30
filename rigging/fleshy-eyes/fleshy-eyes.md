# FLESHY EYES


Reference:

https://www.youtube.com/watch?v=c6XPGvq1Vck



## MEL CODE -- CONSIDER USING NODES INSTEAD

e.g. multiply (rotateX * 0.35) → multiplyDivide

```mel
// fleshy eyes expression, left side

bn_eyelid_l_upper.rotateX = (eyebn_l_1.rotateX * 0.35) + (anim_eyes.BlinkL);
bn_eyelid_l_upper.rotateY = eyebn_l_1.rotateY * 0.15;

bn_eyelid_l_lower.rotateX = (eyebn_l_1.rotateX * 0.25) + (-anim_eyes.BlinkL * 0.3);
bn_eyelid_l_lower.rotateY = eyebn_l_1.rotateY * 0.15;
```

## CONTROL & HIERARCHY

- parent eye controls under empty and center pivot

- parent constrain head bone -> group

- key transform + rotate on eye control parent (shift W + E) - change this away from keyed in script to sth else



## FOLLOW ATTRIBUTE

- create follow attribute on main eye control

- connect eye control attribute to blend parent on parent group with connection editor --- DOUBLE CHECK 

## IK SETUP

- single chain IK handle from eye bone root to end. check if need IK at all, or driving through constraints is enough

- in tutorial, use point constraint to snap - with Python, can align/snap + maintain offset?

## FINISH

- system to double check for issues, naming, functionality etc?

- lock and hide channels


## CONSIDER

- check if expression, IK, groups etc. exist
- if yes, either prompt user or update instead of recreating
- user selects joints: upper and lower lid, eyeball, head joint, then run tool
- -> script validates and builds
- script creates eye control, or user creates and selects it, and the script applies?
- name things correctly as the script goes