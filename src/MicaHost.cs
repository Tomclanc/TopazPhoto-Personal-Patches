using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;
using System.Windows.Forms;
class MicaHost {
 [DllImport("dwmapi.dll")] static extern int DwmSetWindowAttribute(IntPtr hwnd,int attr,ref int value,int size);
 [DllImport("dwmapi.dll")] static extern int DwmGetWindowAttribute(IntPtr hwnd,int attr,out int value,int size);
 static string Quote(string a) {
  var b=new StringBuilder("\""); int slash=0;
  foreach(char c in a) {
   if(c=='\\'){slash++;continue;}
   if(c=='"'){b.Append('\\',slash*2+1);b.Append(c);slash=0;continue;}
   b.Append('\\',slash);slash=0;b.Append(c);
  }
  b.Append('\\',slash*2);b.Append('"');return b.ToString();
 }
 [STAThread] static int Main(string[] args) {
  try {
   string dir=AppDomain.CurrentDomain.BaseDirectory;
   var info=new ProcessStartInfo(Path.Combine(dir,"Topaz Photo.exe"));
   info.UseShellExecute=false; info.WorkingDirectory=dir;
   // Qt's D3D composition swap chain must expose transparency to DWM.
   info.EnvironmentVariables["QT_QPA_DISABLE_REDIRECTION_SURFACE"]="1";
   info.EnvironmentVariables["QSG_RHI_BACKEND"]="d3d11";
   var encoded=new StringBuilder();foreach(var a in args){if(encoded.Length>0)encoded.Append(' ');encoded.Append(Quote(a));}info.Arguments=encoded.ToString();
   using(var child=Process.Start(info)) {
    IntPtr previous=IntPtr.Zero;
    while(!child.WaitForExit(1000)) {
     child.Refresh();var h=child.MainWindowHandle;
     if(h!=IntPtr.Zero && h!=previous) {
      int round=2;int result=DwmSetWindowAttribute(h,33,ref round,4);previous=h;
      File.WriteAllText(Path.Combine(dir,"Mica-status.txt"),"Corner preference request: "+result+Environment.NewLine);
     }
     if(h!=IntPtr.Zero) {
      int backdrop,corner,dark;DwmGetWindowAttribute(h,38,out backdrop,4);DwmGetWindowAttribute(h,33,out corner,4);DwmGetWindowAttribute(h,20,out dark,4);
      string status="Backdrop="+backdrop+"; Corners="+corner+"; Dark="+dark+Environment.NewLine;
      string file=Path.Combine(dir,"Mica-status.txt");if(!File.Exists(file)||File.ReadAllText(file)!=status)File.WriteAllText(file,status);
     }
    }
    return child.ExitCode;
   }
  }catch(Exception e){MessageBox.Show(e.Message,"Topaz Photo Mica");return 1;}
 }
}
