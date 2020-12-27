import platform
import os 
import datetime
import shutil


date = datetime.datetime.now()
system=  platform.system()



BackupData= ''

BackupVorm = input('hoe wilt u uw data backuppen opslaan 1) Local 2) Op de backupserver : ')


def BackupDirectory(sftp):

        DirPath = input('\ngeef hier de volledige pad waar u een backup van wilt opslaan: ')
        BackupDestination = input('\ngeef hier vervolgens de bestemmings locatie/pad van de directory waar u de backup wilt hebben (sluit af met /): ')

        DirFiles = os.listdir(DirPath)
        os.chdir(DirPath) #Veranderd huidige positie naar de backup directory
        # ga elke file af in de opgevraagde director/ 1 voor 1 kopieren
        for file in DirFiles:
                CheckIfDir = os.path.isdir(file) # controleerd of file een directory is

                # Als file geen directory is kopier naar backup locatie
                if CheckIfDir == False:

                        # check of de backup local of op de remote server plaats vind
                        if BackupVorm == '1':
                                shutil.copy(file , BackupDestination)
                        elif BackupVorm == '2': #als server gebruik put functie in sftp
                                sftp.put(file,os.path.join(BackupDestination, file)) 

                else: # als file een directory is doe niks/ sla over
                        pass

def BackupFile(sftp):
        DirRootFile = input('\ngeef hier de pad naar de directory waar de file zich bevind (sluit af met /): ')
        os.chdir(DirRootFile)
        FileName = input('\ngeef de volledige naam van het bestand waar u een backup van wilt maken + extentie: ')
        absolutePath= os.path.abspath(FileName)
        DestinationFile = input('\nVoer hier de directory pad in waar u de backup wilt habben: ')
        print(absolutePath)

        #checkt of backup locaal of op remote server is
        if BackupVorm == '1':
                shutil.copy(absolutePath, DestinationFile)
        elif BackupVorm == '2':# Als het op server plaats vin gebruik secure file transfer protecol
                sftp.put(absolutePath, os.path.join(DestinationFile, FileName))

class RemoteServer:
        # opent een connecte met de ssh host
        def OpenConnect():
                Host = input("\nWat is de hostnaam van de server waar u verbinding mee wilt maken?: ")
                Port = int(input("Op welke poort draait de SSH service?: "))
                Make = paramiko.Transport((Host,Port))
                return Make

        #Handeld de authenticatie met de ssh host / remote server af
        def Auth(Make):
                UserName = input("Wat is de gebruikersnaam van de server?: ")
                Password = input("Wat is de wachtwoord van de gebruiker?: ")
                Make.connect(None, UserName, Password)

        #Maakt connectie met de remote server
        def Login(Make):
                sftp = paramiko.SFTPClient.from_transport(Make)
                return sftp

        #sluit verbinding met remote server af
        def Close(sftp,Make):
                if sftp: sftp.close()
                if Make: Make.close()
                        
#Voer dit uit als er gekozen is voor een lokale opslag van de backup
if BackupVorm == '1':

        BD = bool(int(input('\nWilt du een hele directory backup (1= yes, 0= no): ')))
        if BD != True: # deze conditie check wat voor keuze is gemaakt, backup hele directory of 1 file
                BF = bool(int(input('\nWilt du een file backup (1= yes, 0= no): ')))
        #als er gekozen is voor een lokale backup van een hele directory
        if BD is True:
                BackupDirectory('skip')# skip is er voor omdat de functie een argument (sftp) moet meegrijgen, maar niet nodig voor lokaal
        #als er gekozen is voor een lokaal backup van 1 file
        elif BF is True:
                BackupFile('skip')

#Voer dit uit als her gekozen is voor opslag op een server
elif BackupVorm == '2':

        try:# als het kan import paramiko library om te kunnen werken met een server connectie
                import paramiko

        except ModuleNotFoundError: #Als de library niet aanwezig is download deze met pip en import deze vervolgens

                import pip
                pip.main(['install', 'paramiko'])

                import paramiko
        #deze functies zetten de hele rerver comunnictie tussen host en gast op
        Make = RemoteServer.OpenConnect()
        RemoteServer.Auth(Make)
        sftp = RemoteServer.Login(Make)


        BD = bool(int(input('Wilt du een hele directory backup (1= yes, 0= no): ')))
        if BD != True:
                BF = bool(int(input('Wilt du een file backup (1= yes, 0= no): ')))


        if BD is True:
                BackupDirectory(sftp)

        elif BF is True:
                BackupFile(sftp)

# SSH verbinding afsluiten

        RemoteServer.Close(sftp,Make)






