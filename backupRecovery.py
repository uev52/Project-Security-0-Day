_Author_ = "Twenne Elffers"

import os
import shutil

class RemoteServer: # made by Ethem Varol
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

def Server():
    #deze functies zetten de hele rerver comunnictie tussen host en gast op
    Make = RemoteServer.OpenConnect()
    RemoteServer.Auth(Make)
    sftp = RemoteServer.Login(Make)
    return sftp, Make


def RecoverDir(BackupSoort,BackupLocation, ToLocation, sftp):
        if BackupSoort == "2":
            DirFiles = sftp.listdir(BackupLocation)
            sftp.chdir(BackupLocation)
        elif BackupSoort == "1":
            DirFiles = os.listdir(BackupLocation)
            os.chdir(BackupLocation) #Veranderd huidige positie naar de backup directory
        # ga elke file af in de opgevraagde director/ 1 voor 1 kopieren

        for file in DirFiles:
                if BackupSoort == "1":
                    CheckIfDir = os.path.isdir(file) # controleerd of file een directory is
                elif BackupSoort == "2":
                    if str(sftp.stat(file))[:1] != "d":
                        CheckIfDir = False
                    elif str(sftp.stat(file))[:1]=="d":
                        CheckIfDir = True # controleerd of file een directory is
                # Als file geen directory is kopier naar backup locatie
                if CheckIfDir == False :
                        # check of de backup local of op de remote server plaats vind
                        if BackupSoort == '1':
                                shutil.copy(file , ToLocation)
                                print(file, "Copied")
                        elif BackupSoort == '2': #als server gebruik put functie in sftp
                                sftp.get(localpath=str(os.path.join(ToLocation,file)),remotepath=str(os.path.join(BackupLocation, file))) 
                                print(file, "Copied")
                elif CheckIfDir == True :
                    if os.path.isdir(os.path.join(ToLocation,file)) == False:
                        os.mkdir(os.path.join(ToLocation,file))
                    RecoverDir(BackupSoort,os.path.join(BackupLocation,file), os.path.join(ToLocation,file), sftp)
                    print(file+"/ Copied")
                    if BackupSoort == "2":
                        print("Are you sure")
                        sftp.chdir(BackupLocation)
                    elif BackupSoort == "1" :
                        os.chdir(BackupLocation) # veranderd het terug 
                else: # als file een directory is doe niks/ sla over
                        pass
        return
def RecoverFile(BackupSoort,BackupLocation, ToLocation, sftp):       
        #checkt of backup locaal of op remote server is
        if BackupSoort == '1':
                shutil.copy(BackupLocation, ToLocation)
                print(ToLocation, "Copied")
        elif BackupSoort == '2':# Als het op server plaats vin gebruik secure file transfer protecol
                sftp.get(remotepath=str(BackupLocation.strip()), localpath=str(ToLocation.strip()))
                print(ToLocation, "Copied")

def LocationCheck(Location, string): # verantwoordelijk voor het controleren of het opgegeven al bestaat.
    while (os.path.isdir(Location)) == False and (os.path.isfile(Location)) == False:
            print("Locatie is incorrect")
            Location = input(string)
    return Location

def Ask(BackupSoort):
    BackupLocation = input("Wat is de locatie van de back-up: ") # vraagt de locatie van de backup
    if BackupSoort == "1": # Hij controlleert niet als het op de server staat
        BackupLocation=LocationCheck(BackupLocation, "Wat is de locatie van de back-up: ") # controleert of de opgegeven locatie correct is


    ToLocation = input("Wat is de locatie waar het naar toe moet: ") # vraagt waar de backup naartoe moet
    ToLocation = LocationCheck(ToLocation,"Wat is de locatie waar het naar toe moet: ")# controleert of de opgegeven locatie correct is


    if (os.path.isdir(BackupLocation) == True and os.path.isfile(ToLocation) == True ): # als hij een dir naar een bestand probeert te sturen staat niet toe
        print("Een map kan niet naar een bestand")
        BackupLocation, ToLocation = Ask(BackupSoort) # Vraagt het nog een keer
        return BackupLocation, ToLocation # als het goed is gegaan stuurt hij het gelijk terug


    print("\nBackup: {}\nTo: {}".format(BackupLocation,ToLocation)) # Geeft gegevens die zijn ingevuld terug voor controlle


    CorrectCheck = False #  om te controlleren dat de output goed is gecontroleerd
    while CorrectCheck != True:
        check = input("\nDit zijn de gegevens klopt dit? (Yes,No,Cancel): ") # vraagt of de gegevens goed zijn
        if check.lower() == "n" or check.lower() == "no":  # als dat niet het geval is vraag hij nog eens
            BackupLocation, ToLocation = Ask(BackupSoort)
            CorrectCheck = True            
        elif check.lower() == "c" or check.lower() == "cancel": # Sluit het programma af
            CorrectCheck = True
            print("Quitting...")
            quit()
        elif check.lower() == "y" or check.lower() == "yes": # Als er niks fout is gaat hij verder
            CorrectCheck = True
            return BackupLocation, ToLocation
            continue
        else: # zodat de output goed gecontrolleerd is moet een goede input gegeven worden
            CorrectCheck = False
            print("Verkeerde input")

    return BackupLocation, ToLocation

BackupSoort = 0
while  not(BackupSoort == "1" or  BackupSoort == "2"):
    BackupSoort = input('Waar staat de back-up \n1) Locaal opgeslagen \n2) Op de backupserver\n: ')
    
if BackupSoort == "2":
    try:# als het kan import paramiko library om te kunnen werken met een server connectie
        import paramiko

    except ModuleNotFoundError: #Als de library niet aanwezig is download deze met pip en import deze vervolgens
        import pip
        pip.main(['install', 'paramiko'])
        import paramiko
    
    sftp, Make = Server()
    BackupLocation, ToLocation = Ask("2")# haalt de locaties op voor server bestanden

    if str(sftp.stat(BackupLocation))[:1] != "d": #als het een file is
        RecoverFile(BackupSoort, BackupLocation, ToLocation, sftp)
    elif str(sftp.stat(BackupLocation))[:1]=="d":# als het een dir is
       RecoverDir(BackupSoort, BackupLocation, ToLocation, sftp)# controleerd of file een directory is # gezien de informatie van het bestand niet verkregen kan worden wordt het gevraagd aan de gebruiker
    RemoteServer.Close(sftp,Make) # sluit de server


elif BackupSoort == "1":
    BackupLocation, ToLocation = Ask("1") # haalt de locaties op voor locaal opgeslagen bestanden

    # test of de backup een bestand of dir is. 
    if os.path.isfile(BackupLocation): #als file
        RecoverFile(BackupSoort, BackupLocation, ToLocation, sftp = None)
    elif os.path.isdir(BackupLocation): # als dir
        RecoverDir(BackupSoort, BackupLocation, ToLocation, sftp = None)
    
print("Done")
