# EYE CONTROL CREATION

Needed features:

- Create eye controls: individual + parent
- Constrain eye joints to controls
- Follow head blend attribute
- Fleshy eyes
- Blink control




## FLESHY EYES MEL CODE -- USE NODES INSTEAD

e.g. multiply (rotateX * 0.35) → multiplyDivide

```mel
// fleshy eyes expression, left side

bn_eyelid_l_upper.rotateX = (eyebn_l_1.rotateX * 0.35) + (anim_eyes.BlinkL);
bn_eyelid_l_upper.rotateY = eyebn_l_1.rotateY * 0.15;

bn_eyelid_l_lower.rotateX = (eyebn_l_1.rotateX * 0.25) + (-anim_eyes.BlinkL * 0.3);
bn_eyelid_l_lower.rotateY = eyebn_l_1.rotateY * 0.15;
```

## Fleshy eyes manual method

- parent eye controls under empty and center pivot

- parent constrain head bone -> group

- key transform + rotate on eye control parent (shift W + E) - change this away from keyed in script to sth else

- create follow attribute on main eye control

- connect eye control attribute to blend parent on parent group with connection editor --- DOUBLE CHECK 

- single chain IK handle from eye bone root to end. check if need IK at all, or driving through constraints is enough

- in tutorial, use point constraint to snap - with Python, can align/snap + maintain offset?

- system to double check for issues, naming, functionality etc?

- lock and hide channels

