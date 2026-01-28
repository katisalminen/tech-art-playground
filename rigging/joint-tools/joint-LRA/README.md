# JOINT LOCAL ROTATION AXES VISIBILITY TOOL

This tool manages the visibility of joint Local Rotation Axes (LRA) in Maya.

It does not modify joint orientation, rotation values, or axis alignment in any way.
The tool is intended to be used alongside Maya’s default Orient Joint tool, purely as a visual aid during rigging.

## Visibility Slider

- ON — show Local Rotation Axes

- OFF — hide Local Rotation Axes

## Scope Options

### Toggle Selected

Applies the visibility action to all selected joints.

### Toggle Hierarchy

Applies the visibility action to:

- the selected joint(s), and

- all descendant joints in their hierarchy
(Branching hierarchies are fully supported.)

### Toggle All

Applies the visibility action to all joints in the scene, regardless of selection.

## Selection Rules & Error Handling

- Selected and Hierarchy modes require an active selection.

- If no joints are found within the chosen scope, the tool reports an error and performs no action.

- Non-joint objects may be selected in Hierarchy mode, as long as joint descendants exist.


## Limitations / Non-Goals

This tool does NOT:

- Validate joint orientation correctness.

- Detect reversed or inconsistent axes.

- Replace the Orient Joint tool.

Its sole purpose is to ensure clear, consistent control over LRA visibility during iterative rigging work.