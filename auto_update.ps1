# Commend de volgende commando's uit als de modules niet geïnstaleerd zijn
# Install-Module -Name PSWindowsUpdate
# Save-Module -Name PSWindowsUpdate -Path C:\

# Voor het ophalen van de updates
Get-WindowsUpdate

# Voor het downlaoden van updates en niet rebooten
Get-WUInstall -AcceptAll –IgnoreReboot -Install

# volgend commando uit commenten als reboot gewild is
# Get-WUInstall -AcceptAll –AutoReboot -Install

