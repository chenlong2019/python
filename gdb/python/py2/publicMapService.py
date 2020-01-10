import arcpy
import arcpy.mapping as mapping
wrkspc =r'D:\\bysj\\data\\service'
mxd=mapping.MapDocument(wrkspc+r'\\max4.mxd')
service='max4'
sddraft=wrkspc+service+'.sddraft'
mapping.CreateMapSDDraft(mxd,sddraft,service)
analysis=mapping.AnalyzeForSD(wrkspc+'max4.sddraft')
if analysis['errors']=={}:
    arcpy.StageService_server(sddraft,sd)
