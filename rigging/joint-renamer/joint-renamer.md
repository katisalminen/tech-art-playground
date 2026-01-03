
# JOINT CHAIN RENAMING TOOL

This tool assists with renaming joint chains after placement during character rigging in Autodesk Maya.

It is designed to reduce repetitive manual naming particularly regarding affixes and suffixes while keeping the naming decisions user-controlled.

The tool provides options for joint type, side of the body, and numeric indexing.

This tool does not perform fully automatic or template-based naming. The user is responsible for providing naming input and confirming each step.



## How to use

1. Select the root joint of the joint chain you want to rename.

2. Run the tool.

3. Choose the desired modifiers: joint type, joint side, and numerical indexing.

4. Manually input or confirm the base name of the joint.

5. Confirm the renaming process.

6. The tool will then move on to naming the next joint.

7. By default, joints that already start with a known prefix are skipped to avoid double-prefixing. Untick "Rename joints that already look named" to disable this.


## Options

### Joint Type

- Joint type options are chosen to simplify selecting joints by name.

    - Regular joints: `bn_`
    - Hair joints: `hbn_`
    - Eye joints: `ebn_`
    - End of a joint chain: `be_`


### Joint Side

- Add a modifier to indicate the left or right side of the body.

    - None: no modifier
    - Left: `l_`
    - Right: `r_`

- Further modifiers for upper, lower or middle part of e.g. lips, teeth or eyelids.

    - None: no modifier
    - Upper: `upper_`
    - Lower: `lower_`
    - Middle: `mid_`


### Numerical Indexing

- Choose whether you wish to add numerical indexing to the end of the joint name: 01, 02, etc.


## Example joint chains 

1. `bn_l_hip01`
2. `bn_l_knee01`
3. `bn_l_ankle01`

---

1. `bn_r_upper_indexfinger01`
2. `bn_r_middle_indexfinger01`
3. `bn_r_lower_indexfinger01`
4. `be_r_indexfinger01`

---

1. `bn_r_indexfinger01`
2. `bn_r_indexfinger02`
3. `bn_r_indexfinger03`
4. `be_r_indexfinger01`