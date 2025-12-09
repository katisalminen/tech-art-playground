https://www.youtube.com/watch?v=c6XPGvq1Vck


// fleshy eyes

bn_eyelid_l_upper.rotateX = (eyebn_l_1.rotateX * 0.35) + (anim_eyes.BlinkL);
bn_eyelid_l_upper.rotateY = eyebn_l_1.rotateY * 0.15;

bn_eyelid_l_lower.rotateX = (eyebn_l_1.rotateX * 0.25) + (-anim_eyes.BlinkL * 0.3);
bn_eyelid_l_lower.rotateY = eyebn_l_1.rotateY * 0.15;



parent eye controls under empty and center pivot

parent constrain head bone -> group

key transform + rotate on eye control parent (shift W + E)

create follow attribute on main eye control

connect eye control attribute to blend parent on parent group with connection editor


IK handle from eye bone root to end

point constrain control -> IK handle

parent IK handle to control

remove point constraint