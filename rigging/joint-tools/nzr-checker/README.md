# JOINT NON-ZERO ORIENTATION CHECKER

This script checks the selected joint's hierarchy (joint children only) for non-zero orientations (NZOs). If such joint is found, the script selects it and stops. The user can then fix the issue, re-select the parent and re-run the script until no NZRs are found.

While convenient at any stage of skeleton creation process, this tool is particularly useful for checking skeleton hierarchies that have joints that are already skinned and therefore can't simply have their transformations frozen.

The tool does not fix any NZOs, but only helps the user to detect them.

## RULES

- The tool ignores non-joint objects in the selection and hierarchy.

- If the selected hierarchy has more than one joint with NZOs, it only selects the first one. To find all NZOs, the tool needs to be run multiple times.

- The tool uses full DAG path names, and therefore handles duplicate names in the scene without issues.


## HOW TO USE

1. Select the parent joint which hierarchy you wish to check, e.g. pelvis joint.

2. Run the script.

3. If the script detects a NZR, it selects the joint in question and stops.

4. Fix the NZR, all rotation values should be 0.

5. Repeat steps 1-4 until the script prints "All clear!"