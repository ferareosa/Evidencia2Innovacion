[Setup]
AppName=Agenda
AppVersion=1.0
DefaultDirName={pf}\Agenda
DefaultGroupName=Agenda
OutputBaseFilename=Instalador_Agenda
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\Agenda.exe"; DestDir: "{app}"; Flags: ignoreversion
; Incluí también el ícono si lo tenés
Source: "icono.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{commondesktop}\Agenda"; Filename: "{app}\Agenda.exe"; IconFilename: "{app}\icono.ico"

[UninstallDelete]
; Borra carpeta del programa
Type: filesandordirs; Name: "{app}"
; Borra también la base de datos en AppData
Type: filesandordirs; Name: "{userappdata}\ContactosApp"
