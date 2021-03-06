; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Simple DBF Browser"
#define MyAppVersion "1.0.1-20110327_0324.dev"
#define MyAppPublisher "Mondial Teknologi Solusi, PT"
#define MyAppURL "http://www.mondial.co.id/products/simpledbfbrowser"
#define MyAppExeName "simpledbfbrowser.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{7BB552F8-1A1B-45B4-A722-0FC7FA20E71A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\MTS\Simple DBF Browser
DefaultGroupName={#MyAppName}
LicenseFile=LICENSES.txt
InfoBeforeFile=README.txt
OutputBaseFilename=simpledbfbrowser-win32-{#MyAppVersion}
OutputDir=build
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "build\exe.win32\simpledbfbrowser.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\User\Documents\adhisimon\simpledbfbrowser\build\exe.win32\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Visit our web"; Filename: "{#MyAppURL}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, "&", "&&")}}"; Flags: nowait postinstall skipifsilent

