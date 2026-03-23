# RIGGING TOOLS

Current contents:

- Control Curve Creator tool
- Joint Tools:
    - Joint Local Rotation Axes toggle
    - Joint Renamer
    - Non-Zero Rotations Checker
    - Zero Joint Orient tool

Using the tools:

- Option 1: Copy the entire code into Maya Script Editor and run it for a one-time use or test

- Option 2:
    - Download the Python file
    - Place it inside the following folder: `C:\Users\<your-username>\Documents\maya\scripts`
    - Add a custom button in the Shelf Editor
    - Paste the following code into the button's Command tab with Python chosen as the language:

```python
import <toolname>
<toolname>.run()
```

Where `<toolname>` is the name of the chosen tool, without the .py suffix.