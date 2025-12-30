

# FLESHY EYES SCRIPT FOR MAYA --- WIP

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None

def ensure_maya():
    if cmds is None:
        raise RuntimeError("This script must be run inside Maya.")
    
def build_fleshy_eyes():
    ensure_maya()

    # Check that the required bones and controls exist

    # Build the MEL expression as a string

    # ---





# To solve:
# Hardcode names or create UI for user picking nodes?
# How to handle left and right eye?
