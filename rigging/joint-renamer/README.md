
# JOINT CHAIN RENAMING TOOL

This tool assists with renaming joint chains after placement during character rigging in Autodesk Maya.

It is designed to reduce repetitive manual naming while keeping the naming decisions user-controlled.

The tool provides options for joint type, side of the body, region, and numeric indexing.

This tool does not perform fully automatic or template-based naming. The user is responsible for providing naming input and confirming each step.



## How to use

1. Select the root joint of the joint chain you want to rename.

2. Select desired mode: rename all joints in one, or rename one by one.

3. Type desired basename in the text field.

4. Choose modifiers: joint type, side and region, numerical indexing, skip named joints.

5. Click Rename.




## Options

### Joint Type

- Joint type options are chosen to simplify selecting joints by name.

    - Regular joints: `bn_`
    - Hair joints: `hbn_`
    - Eyelid joints: `ebn_`


### Joint Side

- Add a modifier to indicate the left or right side of the body.

    - Default: no modifier
    - Left: `l_`
    - Right: `r_`

### Joint Region

- Further modifiers for upper, lower or middle part of e.g. lips, teeth or eyelids.

    - Default: no modifier
    - Upper: `upper_`
    - Lower: `lower_`
    - Middle: `mid_`


### Numerical Indexing

- Choose whether you wish to add numerical indexing to the end of the joint name: 01, 02, etc.


### Skip Named Joints

- Choose whether you wish to skip naming joints that already appear named.


## Example joint chains 

1. `bn_l_hip01`
2. `bn_l_knee01`
3. `bn_l_ankle01`
4. `bn_l_toebox01`
5. `be_l_toe01`

---

1. `bn_r_upper_eyelid01`
2. `be_r_upper_eyelid02`

---

1. `bn_spine01`
2. `bn_spine02`
3. `bn_spine03`
4. `bn_spine04`


## Known bugs

- Chosen joint chain must only contain joints with unique names, duplicate names in the scene will cause errors.

- If Preserve Basename is toggled off, but the user types in the same Basename manually, numerical indexing incrementation may not be reliable.


## Future improvements

- Use Classes instead of Dictionaries to store joint information.

- User can customize joint prefix label and name and add or remove them at will.

- User preferences are stored between Maya restarts.