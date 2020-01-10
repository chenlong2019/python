function OnMoved() 
   string szCommand,szCmdLine,szPath,svResult,LicPath,tempdir; 
   STRING svLine,svReturnLine,InsertTxt; //////操作文件的变量 
   NUMBER nvFileHandle; //////////文件句柄 
   NUMBER nvLineNumber ,nvResult; //////////操作文件的变量 
begin 
   szPath=TARGETDIR^"temp"; 
   szCommand = WINSYSDIR^"msiexec.exe"; 
   LongPathToShortPath(szCommand); 
                                           
          /////安装 dotnetfx35sp1.exe 
 GetEnvVar("TEMP", tempdir);//得到临时目录   
FindAllFiles(tempdir, "dotnetfx35sp1.exe" , tempdir, CONTINUE );//在临时目录下搜索 dotnetfx.exe 文件    
 if(LaunchAppAndWait(tempdir, "/q /norestart",WAIT)<0) then 
     abort; 
 endif;                           
                               
                                           
   
////////////////////////安装 AE 运行时 
   if (FindFile (szPath^"ArcGIS Engine10", "setup.msi", svResult) = 0) then 
        szCmdLine =TARGETDIR^"temp"^"ArcGIS Engine10"^"setup.msi\" /qn"; 
        LongPathToShortPath(szCmdLine); 
        Delay(1); 
       if (LaunchAppAndWait(szCommand ,"/i \""+szCmdLine,WAIT) < 0) then 
         
         abort; 
         endif; 
        
    endif; 
/////////////////////////AE 授权 
    
     LicPath="/Lif \""+TARGETDIR^"temp"^"ArcGIS Engine10"^"ArcGIS Engine Runtime License.asr\" /S"; 
     if (FindFile (TARGETDIR^"temp"^"ArcGIS Engine10", "ArcGIS Engine Runtime License.asr", svResult) = 
0) then 
           
           szCmdLine="C:\\Program Files\\Common Files\\ArcGIS\\bin\\SoftwareAuthorization.exe"; 
            
          if (LaunchAppAndWait(szCmdLine,LicPath,WAIT) < 0) then 
           abort; 
          endif; 
      endif;        
       
        LicPath="/Lif \"" +TARGETDIR^"temp"^"ArcGIS Engine10"^"GeodatabaseUpdate.asr\" /S"; 
     if (FindFile (TARGETDIR^"temp"^"ArcGIS Engine10", "GeodatabaseUpdate.asr", svResult) = 0) then 
               
           szCmdLine="C:\\Program Files\\Common Files\\ArcGIS\\bin\\SoftwareAuthorization.exe"; 
          
          if (LaunchAppAndWait(szCmdLine ,LicPath,WAIT) < 0) then 
           abort; 
          endif; 
      endif; 
   if (ExistsDir(TARGETDIR^"temp")=0 ) then 
    if (DeleteProgramFolder (TARGETDIR^"temp") < 0) then 
       
      endif ; 
      endif ; 
 end;