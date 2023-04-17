

__author__ = "Mathupathy"
__copyright__ = "Copyright (C) 2023 Mathupathy"
__license__ = "DSM SOFT"




import clr
import Autodesk.Revit.DB
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI') 
from Autodesk.Revit.DB import * 
from Autodesk.Revit.UI import * 
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.UI import TaskDialog

DB = Autodesk.Revit.DB 

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
view = uidoc.ActiveView
pt_overrides = view.GetPointCloudOverrides()
tx = Transaction(doc, 'My Transaction Name')

# Check if point cloud overrides are available
if pt_overrides is None:
    TaskDialog.Show("Error", "The active view does not support point cloud overrides.")
    raise Exception("Point cloud overrides are not available in this view.")

# Get all point cloud instances in the model
pts = DB.FilteredElementCollector(doc).OfClass(DB.PointCloudInstance).WhereElementIsNotElementType().ToElements()

# Check if any point cloud instances were found
if len(pts) == 0:
    TaskDialog.Show("Information", "There are no point cloud instances in the model.")
else:
    # Create a new transaction and start it
    tx = Transaction(doc, 'Point Cloud Color Mode Change')
    tx.Start()

    # Determine the current color mode
    current_mode = pt_overrides.GetPointCloudScanOverrideSettings(pts[0].Id).ColorMode

    # Change the color mode for each point cloud instance
    pt_cloud_settings = DB.PointClouds.PointCloudOverrideSettings()
    if current_mode == DB.PointCloudColorMode.NoOverride:
        pt_cloud_settings.ColorMode = DB.PointCloudColorMode.Normals


    elif current_mode == DB.PointCloudColorMode.Normals:
        pt_cloud_settings.ColorMode = DB.PointCloudColorMode.FixedColor
    elif current_mode == DB.PointCloudColorMode.FixedColor:
        pt_cloud_settings.ColorMode = DB.PointCloudColorMode.Intensity
    elif current_mode == DB.PointCloudColorMode.Intensity:
        pt_cloud_settings.ColorMode = DB.PointCloudColorMode.Elevation
    

    else:
        pt_cloud_settings.ColorMode = DB.PointCloudColorMode.NoOverride
    for pt in pts:
        pt_overrides.SetPointCloudScanOverrideSettings(pt.Id, pt_cloud_settings)

    # Commit the transaction
    tx.Commit()

    # Show a message indicating success
    if current_mode == DB.PointCloudColorMode.NoOverride:
        TaskDialog.Show("Success", "Point cloud color mode has been changed to Normals.")

    elif current_mode == DB.PointCloudColorMode.Normals:
        TaskDialog.Show("Success", "Point cloud color mode has been changed to FixedColor.")
    elif current_mode == DB.PointCloudColorMode.FixedColor:
        TaskDialog.Show("Success", "Point cloud color mode has been changed to Intensity.")
    elif current_mode == DB.PointCloudColorMode.Intensity:
         TaskDialog.Show("Success", "Point cloud color mode has been changed to Elevation.")



    else:
        TaskDialog.Show("Success", "Point cloud color mode has been changed to NoOverride.")
