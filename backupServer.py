import platform
import os 
import datetime
import shutil


date = datetime.datetime.now()
system=  platform.system()



BackupData= ''

BackupVorm = input('hoe wilt u uw data backuppen opslaan 1) Local 2) Op de backupserver : ')
BD = bool(int(input('Wilt du een hele directory backup (1= yes, 0= no): ')))
BF = bool(int(input('Wilt du een file backup (1= yes, 0= no): ')))
BackupDestination = input('geef hier de pad van de directory waar u de backup wilt opslaan: ')



if BackupVorm == '1':

        if BD is True:
                BackupDirectory = input('geef hier de volledige pad van de directory waar u een backup van wilt maken: ')

                DirectoryFiles = os.listdir(BackupDirectory)
                os.chdir(BackupDirectory)
                print(DirectoryFiles)

                for file in DirectoryFiles:
                        checkIfDir = os.path.isdir(file)

                        if checkIfDir == False:
                                shutil.copy(file, BackupDestination)
                        else:
                                pass

        elif BF is True:
                BackupFileDir = input('geef hier de hier de volledige pad naar het bestand waar u een backup van wilt maken: ')
                os.chdir(BackupFileDir)
                Filename = input('geef de volledige naam van het bestand waar u een backup van wilt maken: ')
                abolutePath= os.path.abspath(Filename)
                shutil.copy(abolutePath, BackupDestination)

elif BackupVorm == '2':

        try:
                import paramiko
                import pysftp
        except ModuleNotFoundError:
                import pip
                pip.main(['install', 'pysftp'])
                pip.main(['install', 'paramiko'])
                import paramiko
                import pysftp 

        # Open een connenctie met host
        host,port = input("Wat is de hostnaam van de server waar u verbinding mee wilt maken?: "), int(input("Op welke poort draait de SSH service?: "))
        transport = paramiko.Transport((host,port))

        # login gegevens voor SSH
        username,password = input("Wat is de gebruikersnaam van de server?: "),input("Wat is de wachtwoord van de gebruiker?: ")
        transport.connect(None,username,password)

        # connectie maken met SSH server
        sftp = paramiko.SFTPClient.from_transport(transport)


        BD = bool(int(input('Wilt du een hele directory backup (1= yes, 0= no): ')))
        BF = bool(int(input('Wilt du een file backup (1= yes, 0= no): ')))
        BackupDestination = input('geef hier de pad van de directory waar u de backup wilt opslaan: ')



        if BD is True:
                BackupDirectory = input('geef hier de volledige pad van de directory waar u een backup van wilt maken: ')

                DirectoryFiles = os.listdir(BackupDirectory)
                os.chdir(BackupDirectory)
                print(DirectoryFiles)

                for file in DirectoryFiles:
                        checkIfDir = os.path.isdir(file)

                        if checkIfDir == False:
                                sftp.put(file,os.path.join(BackupDestination, file))
                        else:
                                pass
        elif BF is True:
                BackupFileDir = input('geef hier de hier de volledige pad naar het bestand waar u een backup van wilt maken: ')
                os.chdir(BackupFileDir)
                Filename = input('geef de volledige naam van het bestand waar u een backup van wilt maken: ')
                abolutePath= os.path.abspath(Filename)
                sftp.put(abolutePath, BackupDestination)


# SSH verbinding afsluiten

        if sftp: sftp.close()
        if transport: transport.close()






