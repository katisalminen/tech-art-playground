

# FOOT ROLL SCRIPT FOR MAYA -- WIP


try:
    import maya.cmds as cmds
except ImportError:
    cmds = None

def ensure_maya():
    if cmds is None:
        raise RuntimeError("This script must be run inside Maya.")



# User selects joints: ankle, ball, toe, foot control
# Check if foot roll system already exists
# Validate required objects exist (ankle, ball, toe, foot control)
# Check if L or R based on naming, run the entire code for that side
# Everything OK -> run script. If not, abort and inform user

def build_foot_roll():
    ensure_maya

    


    # Create heel + reverse joint chain OR locators

    # Create the IK handles, OR one IK to ball + FK toe ?
    # Pay extra attention to IK handle names and parenting!!

    # Parent IKs appropriately

    # Add footRoll attribute with min/max

    # Node network to define foot roll max/min values etc.
    # Sensible defaults + editable values for TA
    # Tooltips to attributes eg. "Minimum value for foot roll. Recommended range: -10 to -5"

    cmds.addAttr(
        "foot_ctrl",
        longName="footRollMin",
        attributeType="double",
        defaultValue=-10,
        min=-20,
        max=0,
        keyable=False,
        niceName="Foot Roll Min",
        help="Minimum value for foot roll. Recommended range: -10 to -5."
    )

    # or

    cmds.addAttr("foot_ctrl.footRollMin", e=True,
                help="Minimum value for foot roll. Recommended range: -10 to -5.")



    # Checks
    # joint scaling
    # rotations at expected defaults
    # consistent joint orientation

    # To solve:
    # How to handle left and right foot separately?
        # Code checks which side -> automatically mirrors everything.
        # Need to choose both sides at start?
    # Undo support in case something goes wrong
    # Re-running the tool without everything becoming a duplicated mess
    # Simple UI needed for custom selecting / adding joint and control names?