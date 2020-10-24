__author__ = "rinorocks8"
__version__ = "1.1"
# This goes in the loaders folder!
# It is run by right clicking the mdl0 and going down to plugins at the bottom on the menu and clicking Easy Replace
#
# Material IDs
# Add these IDs to your materials in your 3D Modeling software to have them updated appropriately
# (sX) Shader (X is the shader integer)
# (1) Adds Transparent
# (2) Cull-None
# (3) Semi-Transparent
# (4-X) Draw Pass (X is the Draw Pass Int)
# (5-NameOfFinalTexture) Temporary Texture Update
# (6-ShadowTextureName) Shadow Update
# (7-X) LODBias (X is the LODBias float *can be positive or negative)
#
# Built-in Fixes
# Alphabetically Sorts Materials
# Exports and Replaces the MDL0 to fix any errors
# Replaces files from the folder your imported model is from automatically
# Name your files the name of your material pre id removal, like "(3)ice" not "ice"
# Adds Shaders Automatically - Have a Subfolder in selected folder called "Shaders" and label
# the shader file as the number of the shader. The file for "Shader 0" will be called "0.mdl0shade"
# Replaces Materials Automatically - Have a Subfolder in selected folder called "Materials" and label
# the material file as the number of the shader. The file for "(3)ice" will be called "(3)ice.mdl0mat"
# Replaces Colors Automatically - Have a Subfolder in selected folder called "Colors" and label
# the color file as the name of the color node that is being replaced. The file for "course_ice_(3)ice"
# will be called "course_ice_(3)ice" (the color file does not have an extension type)
# Example:
# Imported Model Folder                     C:\Folder\course.dae
# Shader Folder where files are pulled      C:\Folder\Shaders\0.mdl0shade
# Material Folder where files are pulled    C:\Folder\Materials\(3)ice.mdl0mat
# Color Folder where files are pulled       C:\Folder\Colors\course_ice_(3)ice
#
# Example
# A material with the name "(s1)(6-rockshadow)rock" will have its shader set to "Shader 1",
# it will have another Texture Reference added and linked to "rockshadow", and the UV will 
# be set to the second TexCoord
#
# Remove IDs so "(s1)(6-rockshadow)rock" will become "rock" when it's finished?
RemoveID = True
# Close the Progress Box automatically when completed?
AutomaticallyCloseProgressBox = True

from BrawlCrate.API import BrawlAPI
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
import BrawlLib
import BrawlCrate

# Credits to _tZ for this function below
def getCourse(root):
    folders = root.Children
    for f in folders:
        if f.Name == "3DModels(NW4R)":
            models = f.Children
            break
    else:
        BrawlAPI.ShowMessage("There's no model folder", 'Error')
        return -1

    for m in models:
        if m.Name == "course":
            return m
            break
        else:
            BrawlAPI.ShowMessage("Model is not named course", 'Error')
    else:
        BrawlAPI.ShowMessage("There's no course model", 'Error')
        return -1

def mat_search(node):
    if isinstance(node, MDL0MaterialNode):
        return [node] 
    list = []
    for child in node.Children:
        list += mat_search(child) 
    print(list)
    return list

def object_search(node):
    if isinstance(node, MDL0ObjectNode):
        return [node] 
    list = []
    for child in node.Children:
        list += object_search(child) 
    print(list)
    return list

def color_search(node):
    if isinstance(node, MDL0ColorNode):
        return [node] 
    list = []
    for child in node.Children:
        list += color_search(child) 
    print(list)
    return list
    
def normal_search(node):
    if isinstance(node, MDL0NormalNode):
        return [node] 
    list = []
    for child in node.Children:
        list += normal_search(child) 
    print(list)
    return list
    
def vertex_search(node):
    if isinstance(node, MDL0VertexNode):
        return [node] 
    list = []
    for child in node.Children:
        list += vertex_search(child) 
    print(list)
    return list
    
def brresnamecheck():
    if BrawlAPI.RootNode.Name == "course_model.brres":
        return True
    else:
        BrawlAPI.ShowMessage("Brres File is not named course_model.brres", '')
        return False

def easy_replace(sender, event_args):
    FilePath = BrawlAPI.OpenFileDialog("Open File", "All Supported Formats (*.mdl0, *.pmd, *.dae)|*.mdl0;*.pmd;*.dae|NW4R Model (*.mdl0)|*.mdl0|PMD File (*.pmd)|*.pmd|DAE File (*.dae)|*.dae|All files (*.*)|*.*")
    a = BrawlLib.BrawlManagerLib.ProgressDialog()
    if FilePath == '':
        BrawlAPI.ShowMessage("No File Selected", '')
    elif brresnamecheck():
        l = []
        s = ""
        a.Show()
        FolderPath = ((FilePath[::-1]).split('\\', 1)[1])[::-1] + "\\"
        BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "Files Folder Selected: \n"+ FolderPath)
        if (BrawlAPI.RootNode is not None) & (BrawlAPI.NodeWrapperList != -1):
            root = BrawlAPI.RootNode
            course = getCourse(root)

            BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "Waiting for model import")
            course.Replace(FilePath)

            a.Progress = 12.5
            for item in mat_search(root):
                BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "Updating " + item.Name + " Material")
                # Shaders
                loc = item.Name.find("(s")
                if (loc != -1):
                    x = str(item.Name[(loc+2):item.Name.find(")", loc + 2)])
                    if not x.isdigit():
                        BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "**Error: " + item.Name + " has an invalid shader number")
                        a.ProgressTitle = "Error Found"
                    elif x != "0":
                        s = item.Shader
                        item.Shader = "Shader " + x
                        if (s == item.Shader) & (item.Shader != "Shader " + x) & (x not in l):
                            l.append(x)
                # Transparent
                if (item.Name.find("(1)") != -1):
                    item.Ref0 = 128
                    item.Comp0 = item.Comp0.GreaterOrEqual
                    item.Ref1 = 255
                # Cull-None
                if (item.Name.find("(2)") != -1):
                    item.CullMode = 0
                # Semi-Transparent
                if (item.Name.find("(3)") != -1):
                    item.EnableBlend = 1
                    for item1 in object_search(root):
                        if (item1.DrawCalls[0].Material == item.Name):
                            item1.DrawCalls[0].DrawPass = DrawCall.DrawPassType.Transparent
                # Draw Pass
                loc = item.Name.find("(4-")
                if (loc != -1):
                    x = str(item.Name[(loc+3):item.Name.find(")", loc+3)]) 
                    try:
                        int(x)
                        is_dig = True
                    except ValueError:
                        is_dig = False
                    if not is_dig:
                        BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "**Error: " + item.Name + " has an invalid Draw Pass number")
                        a.ProgressTitle = "Error Found"
                    else:
                        for item1 in object_search(root):
                            if (item1.DrawCalls[0].Material == item.Name):
                                item1.DrawCalls[0].DrawPriority = int(x)
                # Temporary Texture
                loc = item.Name.find("(5-")
                if (loc != -1):
                    if item.Children.Count < 1:
                        item.AddChild(MDL0MaterialRefNode())
                    item.Children[0].Name = item.Name[(loc+3):item.Name.find(")", loc+3)]
                # Shadow
                loc = item.Name.find("(6-")
                if (loc != -1):
                    if (item.Children.Count < 2):
                        item.AddChild(MDL0MaterialRefNode())
                        item.Children[1].Name = item.Name[(loc+3):item.Name.find(")", loc+3)]
                        item.Children[1].EmbossSource = 5
                        item.Children[1].Coordinates = item.Children[1]._texMtxFlags.SourceRow.TexCoord1
                else:
                    item.LightChannel0.Color.Enabled = 0
                # LODBias
                loc = item.Name.find("(7-")
                if (loc != -1):
                    x = str(item.Name[(loc+3):item.Name.find(")", loc+3)]) 
                    try:
                        float(x)
                        is_dig = True
                    except ValueError:
                        is_dig = False
                    if not is_dig:
                        BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "**Error: " + item.Name + " has an invalid LODBias number")
                        a.ProgressTitle = "Error Found"
                    else:
                        item.Children[0].LODBias = float(x)
            a.Progress = 25
            # Sort Materials
            # yes this is inefficent but the built-in sort function causes issues
            for c in course.Children:
                if (c.Name == "Materials"):
                    for x in range(1, len(c.Children)):
                        for x in range(1, len(c.Children)):
                            if c.Children[x].Name < c.Children[x-1].Name:  
                                c.Children[x-1].MoveDown()
            BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "Sorting Materials")
            a.Progress = 37.5
            # Replace Materials
            for c in course.Children: #run way to many times?
                if (c.Name == "Materials"):
                    for material in c.Children:
                        try:
                            material.Replace(FolderPath + 'Materials\\' + material.Name + '.mdl0mat')
                        except:
                            continue
            BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "Replacing Materials from files")
            #Replacing Color Files
            for item in color_search(root):
                try:
                    item.Replace(FolderPath + 'Colors\\' + item.Name)
                except:
                    continue
            BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "Replacing Colors from files")
            a.Progress = 50
            # Creates Missing Shaders
            for d in BrawlAPI.NodeWrapperList:
                if (type(d) == BrawlCrate.NodeWrappers.MDL0Wrapper):
                    BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, str(len(l)) + " Shaders Identified")
                    for x in range(0, len(l)):
                        d.NewShader()
            BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "Creating Missing Shaders")
            a.Progress = 62.5
            # Replaces Shaders from file if found                    
            for c in course.Children:
                if (c.Name == "Shaders"):
                    for x in range(0, len(c.Children)):
                        try:
                            c.Children[x].Replace(FolderPath + 'Shaders\\' + str(x) + '.mdl0shade')
                        except: 
                            continue
            BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "Replacing Shaders from files")
            a.Progress = 75
            #Sets Shaders
            for item in mat_search(root):
                loc = item.Name.find("(s")
                if (loc != -1):
                    x = item.Name[(loc+2):item.Name.find(")", loc + 2)]
                    item.Shader = "Shader " + str(x)
                #Remove IDs
                if (RemoveID is True):
                    item.Name = item.Name.replace('(1)', '')
                    item.Name = item.Name.replace('(2)', '')
                    item.Name = item.Name.replace('(3)', '')
                    item.Name = item.Name.replace('(4-' + item.Name[(item.Name.find("(4-")+3):item.Name.find(")", item.Name.find("(4-")+3)] + ')', '')
                    item.Name = item.Name.replace('(5-' + item.Name[(item.Name.find("(5-")+3):item.Name.find(")", item.Name.find("(5-")+3)] + ')', '')
                    item.Name = item.Name.replace('(6-' + item.Name[(item.Name.find("(6-")+3):item.Name.find(")", item.Name.find("(6-")+3)] + ')', '')
                    item.Name = item.Name.replace('(7-' + item.Name[(item.Name.find("(7-")+3):item.Name.find(")", item.Name.find("(7-")+3)] + ')', '')
                    item.Name = item.Name.replace('(s' + item.Name[(item.Name.find("(s")+2):item.Name.find(")", item.Name.find("(s")+2)] + ')', '')
            if (RemoveID is True):
                #Remove IDs
                for item in color_search(root):
                    item.Name = item.Name.replace('(1)', '')
                    item.Name = item.Name.replace('(2)', '')
                    item.Name = item.Name.replace('(3)', '')
                    item.Name = item.Name.replace('(4-' + item.Name[(item.Name.find("(4-")+3):item.Name.find(")", item.Name.find("(4-")+3)] + ')', '')
                    item.Name = item.Name.replace('(5-' + item.Name[(item.Name.find("(5-")+3):item.Name.find(")", item.Name.find("(5-")+3)] + ')', '')
                    item.Name = item.Name.replace('(6-' + item.Name[(item.Name.find("(6-")+3):item.Name.find(")", item.Name.find("(6-")+3)] + ')', '')
                    item.Name = item.Name.replace('(7-' + item.Name[(item.Name.find("(7-")+3):item.Name.find(")", item.Name.find("(7-")+3)] + ')', '')
                    item.Name = item.Name.replace('(s' + item.Name[(item.Name.find("(s")+2):item.Name.find(")", item.Name.find("(s")+2)] + ')', '')
                for item in normal_search(root):
                    item.Name = item.Name.replace('(1)', '')
                    item.Name = item.Name.replace('(2)', '')
                    item.Name = item.Name.replace('(3)', '')
                    item.Name = item.Name.replace('(4-' + item.Name[(item.Name.find("(4-")+3):item.Name.find(")", item.Name.find("(4-")+3)] + ')', '')
                    item.Name = item.Name.replace('(5-' + item.Name[(item.Name.find("(5-")+3):item.Name.find(")", item.Name.find("(5-")+3)] + ')', '')
                    item.Name = item.Name.replace('(6-' + item.Name[(item.Name.find("(6-")+3):item.Name.find(")", item.Name.find("(6-")+3)] + ')', '')
                    item.Name = item.Name.replace('(7-' + item.Name[(item.Name.find("(7-")+3):item.Name.find(")", item.Name.find("(7-")+3)] + ')', '')
                    item.Name = item.Name.replace('(s' + item.Name[(item.Name.find("(s")+2):item.Name.find(")", item.Name.find("(s")+2)] + ')', '')
                for item in vertex_search(root):
                    item.Name = item.Name.replace('(1)', '')
                    item.Name = item.Name.replace('(2)', '')
                    item.Name = item.Name.replace('(3)', '')
                    item.Name = item.Name.replace('(4-' + item.Name[(item.Name.find("(4-")+3):item.Name.find(")", item.Name.find("(4-")+3)] + ')', '')
                    item.Name = item.Name.replace('(5-' + item.Name[(item.Name.find("(5-")+3):item.Name.find(")", item.Name.find("(5-")+3)] + ')', '')
                    item.Name = item.Name.replace('(6-' + item.Name[(item.Name.find("(6-")+3):item.Name.find(")", item.Name.find("(6-")+3)] + ')', '')
                    item.Name = item.Name.replace('(7-' + item.Name[(item.Name.find("(7-")+3):item.Name.find(")", item.Name.find("(7-")+3)] + ')', '')
                    item.Name = item.Name.replace('(s' + item.Name[(item.Name.find("(s")+2):item.Name.find(")", item.Name.find("(s")+2)] + ')', '')
            if (RemoveID is True):
                BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "Setting Shaders and Removing IDs")
            else:
                BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "Setting Shaders")
            a.Progress = 87.5
            # Exports and Replaces MDL0
            course.Export(BrawlAPI.AppPath+"\course.mdl0")
            course.Replace(BrawlAPI.AppPath+"\course.mdl0")
            BrawlLib.BrawlManagerLib.FileOperations.Delete(BrawlAPI.AppPath+"\course.mdl0")
            
            BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "Exporting and Replacing MDL0")
            a.Progress = 100
            
            if a.ProgressTitle != "Error Found":
                BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "Done!")
            else:
                BrawlLib.BrawlManagerLib.ProgressDialog.AppendLogLine(a, "Finished with Errors")
    if (a.ProgressTitle != "Error Found") & AutomaticallyCloseProgressBox:
        a.Dispose()

BrawlAPI.AddContextMenuItem(BrawlCrate.NodeWrappers.MDL0Wrapper, "", None, None, ToolStripMenuItem("Easy Replace", None, easy_replace))