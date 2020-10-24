# EasyReplace
EasyReplace is a BrawlCrate plugin created by Rinorocks. The plugin works by modifying material names in the 3D modeling software with IDs that indicate changes that are automatically applied to the model upon import to BrawlCrate. It is placed in the "Loaders" folder within the BrawlCrate folder, and is run by right-clicking the MDL0 file, going down to plugins at the bottom on the menu and clicking "Easy Replace".

#####The Material ID Key - Add these to your materials to have them updated appropriately:

- (sX) Shader (X is the shader integer) (The shader defaults to Shader 0 if not used)
- (1) Adds Transparent
- (2) Cull-None
- (3) Semi-Transparent
- (4-X) Draw Pass (X is the Draw Pass Int)
- (5-NameOfFinalTexture) Temporary Texture Update
- (6-ShadowTextureName) Shadow Update
- (7-X) LODBias (X is the LODBias float; can be positive or negative)

#####Built in Fixes

- Alphabetically sorts materials.
- Exports and replaces the MDL0 to fix any errors.
- Replaces files from the folder your imported model is from automatically.
- Name your files the name of your material pre-ID removal, like "(3)ice" and not "ice".
- Adds Shaders Automatically - Have a subfolder in a selected folder called "Shaders" and label the shader file as the number of the shader. The file for "Shader 0" will be called "0.mdl0shade".
- Replaces Materials Automatically - Have a subfolder in a selected folder called "Materials" and label the material file as the number of the shader. The file for "(3)ice" will be called "(3)ice.mdl0mat".
- Replaces Colors Automatically - Have a Subfolder in selected folder called "Colors" and label the color file as the name of the color node that is being replaced. The file for "course_ice_(3)ice" will be called "course_ice_(3)ice" (the color file does not have an extension type)
- RemoveIDs can be enabled so "(s1)(6-rockshadow)rock" will become "rock" when it's finished and so on...
- Example:
 - Imported Model Folder                     C:\Folder\course.dae
 - Material Folder where files are pulled    C:\Folder\Materials\(3)ice.mdl0mat
 - Shader Folder where files are pulled      C:\Folder\Shaders\0.mdl0shade
 - Color Folder where files are pulled       C:\Folder\Colors\course_ice_(3)ice

##### Plugin Use Example:
- A material with the name "(s1)(6-rockshadow)rock" will have its shader set to "Shader 1", it will have another texture reference added and linked to "rockshadow", and the UV will be set to the second TexCoord.

## Preview
![](http://wiki.tockdom.com/w/images/thumb/4/45/EasyReplace_Location_Usage.PNG/400px-EasyReplace_Location_Usage.PNG)
