import arcpy
class ToolValidator(object):
  """Class for validating a tool's parameter values and controlling
  the behavior of the tool's dialog."""

  def __init__(self):
    """Setup arcpy and the list of tool parameters."""
    self.params = arcpy.GetParameterInfo()

  def initializeParameters(self):
    """Refine the properties of a tool's parameters.  This method is
    called when the tool is opened."""
    return

  def updateParameters(self):
    """Modify the values and properties of parameters before internal
    validation is performed.  This method is called whenever a parameter
    has been changed."""
    if self.params[0].altered and self.params[0].value <> "":
      self.params[1].enabled = True
      self.params[1].filter.list=['Point','Polyline','Polygon']
      self.params[3].obtainedfrom=self.params[0]
    elif self.params[0].value == "":
      self.params[1].enabled = False
    return

  def updateMessages(self):
    """Modify the messages created by internal validation for each tool
    parameter.  This method is called after internal validation."""
    #self.params[1].setErrorMessage(self.params[1].enabled)
#    arcpy.AddMessage('params[0]={0} '.format(self.params[0].value))
#    arcpy.AddMessage('params[1]={0} '.format(self.params[1].value))
    return
