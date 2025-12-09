# FOOT ROLL

References:

https://www.youtube.com/watch?v=FfGfV7Lc_34
https://www.youtube.com/watch?v=HOtHR1CagXM

---

leg bone set up: ankle bone -> toe bone

---
create heel bone

continue chain by snapping heel -> toe -> ball of foot -> ankle

this creates the reverse joint chain for foot roll
(rename!)

---

create single chain solver IK's on original joints:

- ankle -> ball of foot

- ball of foot -> toe

- parent IK's to their corresponding foot roll joints

---

create Foot Roll attribute on foot control curve: min -10, max 5

set driven keys for foot roll attribute:

- 5 -> max rotation from heel
- 0 -> flat on the ground
- -5 -> max rotation from ball of foot (stepping motion)
- -10 -> max rotation from toe (tippy toes)

---

WIP -- DOUBLE CHECK