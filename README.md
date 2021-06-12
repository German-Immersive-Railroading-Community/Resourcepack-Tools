# Resource pack tools for GIRSignals

This python file includes a lot of useful tools in order to easily create and distribute resource packs for our signal mod. To be clear you currently can not add your own signals but you can customize the look of your signal.

## How does our model system work?

Our model system uses normal block json models. If you use Wavefront (.obj) or MagicaVoxel Models you can use Blockbench with the according extensions in order to convert them into a normal block json. As our models are prebaked and optimized for performance we use a texture path replacement system in order to still have good quality when mipmaps are enabled.

This texture replacement system works as following: If you have a signal light for example
![]()
