# Resource pack tools for GIRSignals

This python file includes a lot of useful tools in order to easily create and distribute resource packs for our signal mod. To be clear you currently can not add your own signals but you can customize the look of your signal.

## How does our model system work?

Our model system uses normal block json models. If you use Wavefront (.obj) or MagicaVoxel Models you can use Blockbench with the according extensions in order to convert them into a normal block json. As our models are prebaked and optimized for performance we use a texture path replacement system in order to still have good quality when mipmaps are enabled.

This texture replacement system works as following: If you have a signal light for example, the signal model has a specific identifier for that signal light texture. The HV Signal system has one green lamp which can be turned on or off. This lamp texture for example has the internal json texture name `lamp_greennorth` if this variable is not present it will not work. The intial value of each texture variable should be the off state. The textures are replaced by the according hardcoded texture hence your UVs should be compatiable with those states. If you want to know which names are required by which model in order to function see the `GIRCustomModelLoader.java` which is automatically downloaded if you use our tool. If you cannot read Java code or if you want to check whether you did everything write you can use the check or checkall command in our tool which shows you all the missing textures that are needed for the functions to work.

Additionally we use block rotation to automate the process of rotation. This unfortuanlly means that block rotations cannot be used and will be overwritten by our system. We will try to find a different solution for this problem but for now this issue remains.

## Usage of our tool system

### Downloading

You can either use git to pull form the master branch or you can use the `Download ZIP` function if you press the green `Code` button and extract that zip file where you want your workspace to be.

### Prerequirements

In order to run the python script you need to have `python 3` installed. In order to install [python.org](https://www.python.org/downloads/) and download the latest installer and install it.

Optionally: If you want to use compression you might want to install zlib

### Usage

You should now be able to start the python file with a double click! If this does not work you might want to restart your PC and/or use the console in order to start it. The script will ask you for a project name in order to write the neccesary files. This system will layout the asset tree with dummy files that contain the original model files.

### Note

Please note that all of our code and assets are released under the Apache 2.0 License (See the original mod repository. This is not being updatet!). So make sure you adhere to our license
