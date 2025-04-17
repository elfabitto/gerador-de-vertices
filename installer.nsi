
; Script de instalação para o GeradorVertices
; Gerado automaticamente

!include "MUI2.nsh"

; Informações gerais
Name "GeradorVertices"
OutFile "installer\GeradorVertices_Setup_2.0.0.exe"
InstallDir "$LOCALAPPDATA\GeradorVertices"
InstallDirRegKey HKCU "Software\GeradorVertices" ""
RequestExecutionLevel user

; Interface
!define MUI_ABORTWARNING
!define MUI_ICON "resources\planeta.ico"

; Páginas
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Idiomas
!insertmacro MUI_LANGUAGE "PortugueseBR"

; Seção de instalação
Section "Instalar" SecInstall
  SetOutPath "$INSTDIR"
  
  ; Arquivos do aplicativo
  File /r "dist\GeradorVertices\*.*"
  
  ; Criar atalhos
  CreateDirectory "$SMPROGRAMS\GeradorVertices"
  CreateShortcut "$SMPROGRAMS\GeradorVertices\GeradorVertices.lnk" "$INSTDIR\GeradorVertices.exe"
  CreateShortcut "$DESKTOP\GeradorVertices.lnk" "$INSTDIR\GeradorVertices.exe"
  
  ; Registrar desinstalador
  WriteRegStr HKCU "Software\GeradorVertices" "" $INSTDIR
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\GeradorVertices" "DisplayName" "GeradorVertices"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\GeradorVertices" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\GeradorVertices" "DisplayIcon" "$INSTDIR\GeradorVertices.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\GeradorVertices" "DisplayVersion" "2.0.0"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\GeradorVertices" "Publisher" "Gerador de Vértices"
SectionEnd

; Seção de desinstalação
Section "Uninstall"
  ; Remover arquivos e diretórios
  RMDir /r "$INSTDIR"
  
  ; Remover atalhos
  Delete "$SMPROGRAMS\GeradorVertices\GeradorVertices.lnk"
  RMDir "$SMPROGRAMS\GeradorVertices"
  Delete "$DESKTOP\GeradorVertices.lnk"
  
  ; Remover registros
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\GeradorVertices"
  DeleteRegKey HKCU "Software\GeradorVertices"
SectionEnd
