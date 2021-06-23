# Resource pack tools for GIRSignals

This python file includes a lot of useful tools in order to easily create and distribute resource packs for our signal mod. To be clear you currently can not add your own signals but you can customize the look of your signal.

## How does our model system work?

Our model system uses normal block json models. If you use Wavefront (.obj) or MagicaVoxel Models you can use Blockbench with the according extensions in order to convert them into a normal block json. As our models are prebaked and optimized for performance we use a texture path replacement system in order to still have good quality when mipmaps are enabled.

This texture replacement system works as following: If you have a signal light for example, the signal model has a specific identifier for that signal light texture. The HV Signal system has one green lamp which can be turned on or off. This lamp texture for example has the internal json texture name `lamp_greennorth` if this variable is not present it will not work. The intial value of each texture variable should be the off state. The textures are replaced by the according hardcoded texture hence your UVs should be compatiable with those states. If you want to know which names are required by which model in order to function see the `GIRCustomModelLoader.java` which is automatically downloaded if you use our tool. If you cannot read Java code or if you want to check whether you did everything write you can use the check or checkall command in our tool which shows you all the missing textures that are needed for the functions to work.

Additionally we use block rotation to automate the process of rotation. This unfortuanlly means that block rotations cannot be used and will be overwritten by our system. We will try to find a different solution for this problem but for now this issue remains.
