# Resource pack tools for OpenSignals

This python file includes a lot of useful tools in order to easily create and distribute resource packs for our signal mod. To be clear you currently can not add your own signals but you can customize the look of your signals.

## How does our model system work?

Our model system uses normal block json models. If you use Wavefront (.obj) or MagicaVoxel Models you can use Blockbench with the according extensions in order to convert them into a normal block json (use the convert project feature). As our models are prebaked and optimized for performance we use a texture path replacement system, to still have good quality when mipmaps are enabled.

This texture replacement system works as following: Take a signal light for example, the signal model has a specific identifier for that signal light texture. To make it more concrete the HV signal system has one green lamp which can be turned on or off. This lamp texture has the internal json texture name `lamp_greennorth` if this variable is not present it will not work. The initial value of each texture variable should be the off state. The textures are replaced by the according hardcoded texture hence your UVs should be compatible with those states. If you want to know which names are required by which model in order to function see the `GIRCustomModelLoader.java` which is automatically downloaded if you use our tool. If you cannot read java code or if you want to check whether you did everything right you can use the `check` or `checkall` command in our tool which shows you all the missing textures that are needed for the functions to work.

## Usage of our tool system

### Downloading

You can either use git to clone the master branch or you can use the `Download ZIP` function if you press the green `Code` button and extract that zip file where you want your workspace to be.

### Requirements

In order to run the python script you need to have `python 3` installed. In order to install python you need to go to [python.org](https://www.python.org/downloads/) and download the latest installer and install it.

Optionally: If you want to use compression you might want to install zlib

### Usage

You should now be able to start the python file with a double click! If this does not work you might want to restart your PC and/or use the console in order to start it. The script will ask you for a project name in order to write the necessary files. This system will layout the asset tree with dummy files that contain the original model files.

### Note

Please note that all of our code and assets are released under the Apache 2.0 License (See the original mod repository. This is not being updated!). So make sure you adhere to our license.

## Commands

### update

Updates the asset structure and version information according to newer version of the mod. You can trigger this anytime and it checks whether there was an update of the mod or not and downloads the new information.

### pack

This packs all your data in one zip file and names it accordingly so you can distribute it. It only packs what is needed for the resource pack to work.

### check, checkall

This checks the texture dependencies and warns you if you have forgotten some dependencies. Additionally it checks your json's to not be malformed.
