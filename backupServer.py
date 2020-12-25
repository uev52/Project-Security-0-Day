import platform
import os 
import datetime
import shutil


date = datetime.datetime.now()
system=  platform.system()



BackupData= ''

BD = bool(int(input('Wilt du een hele directory backup (1= yes, 0= no): ')))
BF = bool(int(input('Wilt du een file backup (1= yes, 0= no): ')))
BackupDestination = input('geef hier de pad van de directory waar u de backup wilt opslaan: ')



if BD is True:
    BackupDirectory = input('geef hier de volledige pad van de directory waar u een backup van wilt maken: ')

    DirectoryFiles = os.listdir(BackupDirectory)
    
    os.chdir(BackupDirectory)

    for file in DirectoryFiles:
        shutil.copy(file, Backupdestination)

elif BF is True:
    BackupFile = './'+input('geef hier de hier de volledige naam het bestand waar u een backup van wilt maken: ')

    os.chdir(BackupFile)

    shutil.copy(Backupfile, Backupdestination)


print(date)
print(system)
print(DirectoryFiles)
print(BD)
print(BF)
