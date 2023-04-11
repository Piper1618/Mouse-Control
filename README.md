# Mouse Control

This script adds functionality to [OBS](https://obsproject.com/). It allows the position of a single source to be moved using the mouse. The chosen source will track mouse motion even if OBS is not in focus. I use this to overlay and control a pointer image over games that hide the mouse cursor. I have a global hotkey bound to show the overlaid pointer when there's something I want to point out.

Only one source can be controlled. If you want to have identical sources move in multiple scenes, create a blank scene, add the source you want to move, and then add scene sources to other scenes where it should be visible. The source will move even if its scene is not the selected one. To truly control multiple sources, you'd need to create a copy of the script with a different name and import it separately.

The only file that's needed is "Mouse Control.py". Once the file is on your local drive, the script can be imported from inside OBS by navigating to Tools -> Scripts. Because this is a Python script, the path in the Python Settings tab must be filled out.

This was tested on Python 3.6 and OBS version 28.0.2.

You'll also need to install pynput, which is used to read mouse positions: https://pypi.org/project/pynput/

# Settings

Scene Name: Enter the name of the scene where the source can be found.

Source Name: Enter the name of the source to be controlled.

Offsets: The mouse's position is offset by this amount. Negative values effectively move the origin point of the source being controlled. If you want to use the mouse's position on a monitor other than the main monitor, you'll also need to subtract the relevant monitor's position.

Scale: Mouse movements will be multiplied by this scale before being applied to the source. This is applied after the offsets are added. For example, if your monitor is 1080p and your OBS canvas is 720p, you'll need to scale down the motion to 0.67.

# Known issues

Occasionally, the source will snap to position (0, 0) for one frame. I've confirmed that pynput is still reading the correct mouse position on these frames, so I don't know what OBS thinks it's doing.