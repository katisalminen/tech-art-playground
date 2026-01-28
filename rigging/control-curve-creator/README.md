# CONTROL CURVE CREATION TOOL


- Create a control curve without deformation history based on pre-selected shape

- Create a control group for clean transforms

- Snap pivot to selected joint

- If a joint is chosen, orient control group based on the joint orientation

- Name the control and its group based on joint
    - `bn_l_knee01` -> `anim_l_knee01`, `ctrl_anim_l_knee01`

- Or give the control a default name and index it if the name already exists
    - anim_curve01

- Hide and lock transform, scale, and visibility channels

- Finish with control group selected, not the curve to ensure clean positioning

The user can then modify the shape of the curve to fit the mesh geometry, but they won't need to move, rotate, or scale the curve itself anymore. Locking and hiding the channels ensure this.


## UI options:

Curve shape dropdown or checkbox

- Circle
- Square
- Box
- Triangle
- Arrow

## Notes

Control curves created with this tool will **not** have **construction history**. They are created once and do not auto-update if the joint they were based on is changed. History nodes support procedural regeneration, not behavioral rigging. For animator-facing controls, authorship stability outweighs procedural flexibility.

## Future improvements

- Potential further development: add a constraint option that automatically constraints the created curve to the selected joint with the selected constraint type, auto-naming it as well.

- Separate into three modes?
    - Curve mode: only control curve creation.
    - Constraint mode: apply and auto-name constraint.
    - Both: create curve and apply constraint to selected joint.

Potential issues: applying constraints with native tools is fairly fast as well. Naming them adds friction, but is not of highest importance anyway.
This mode would use preset, generic constraint settings, any custom settings would need to still be done through the actual constraint tool.