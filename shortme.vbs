Dim FileName
FileName = "C:\User\Konstas\workspace\apodixis\apodixis.py"
'Create a WshShell Object
Set WshShell = Wscript.CreateObject("Wscript.Shell")

'Create a WshShortcut Object
Set oShellLink = WshShell.CreateShortcut("C:\Users\Konstas\Desktop\Apodixis.lnk")

'Set the Target Path for the shortcut
oShellLink.TargetPath = FileName

'Set the additional parameters for the shortcut
' oShellLink.Arguments = "c:\windows\desktop\aaa.txt"

'Save the shortcut
oShellLink.Save

'Clean up the WshShortcut Object
Set oShellLink = Nothing
