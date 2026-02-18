# CONTROL CURVE CREATION TOOL

This tool assists the user in creating control curves for animations, providing a set of pre-made shapes, automating drawing overrides settings, naming, and offset group creation.

The tool does not automatically adjust the curve shape and positioning to the geometry. The user needs to manipulate the curve to their liking, the tool only provides a starting template.

## UI options

### Curve shape options

Clicking any button will create a control curve with the labeled shape with an offset group. If one or more joints are chosen, the tool creates a control curve, sets its pivot point and renames it according to each selected joint.

- Circle
- Square
- Box
- Triangle
- Arrow
- Cross

### Side

The tool sets Drawing Override colors based on the side:

- Center -> red
- Left (+X) -> yellow
- Right (-X) -> blue

By default, the tool automatically detects the side and therefore the color of the control, but this can be manually set by changing the side from the dropdown.

### Control Size

Adjust the slider to set the initial size of the control: left for smaller, right for larger.

### Freeze

If a control curve was manipulated after its creation for aesthetics, click Freeze to zero out its rotations - the offset group ensures correct pivot. The Freeze button ignores values that are already locked.


### Mirror

The Mirror button mirrors the selected control curve on the X axis. Naming and drawing overrides are automatically set to the opposite side if either `_r_` or `_l_` is detected in the name.

Note: mirroring a curve creates an additional parent group, `*_mirror`, with Scale X set to -1.


## Notes

Control curves created with this tool will **not** have **construction history**. They are created once and do not auto-update if the joint they were based on is changed. History nodes support procedural regeneration, not behavioral rigging. For animator-facing controls, authorship stability outweighs procedural flexibility.

## Future improvements

- A constraint option that automatically constraints the created curve to the selected joint with the selected constraint type, auto-naming it as well.

- Separate into three modes?
    - Curve mode: only control curve creation.
    - Constraint mode: apply and auto-name constraint.
    - Both: create curve and apply constraint to selected joint.

Potential issues: applying constraints with native tools is fairly fast as well. Naming them is not as fast, but this is not typically a high priority task in rigging.