import os
import shutil

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

def server():
    try:# als het kan import paramiko library om te kunnen werken met een server connectie
        import paramiko

    except ModuleNotFoundError: #Als de library niet aanwezig is download deze met pip en import deze vervolgens
        import pip
        pip.main(['install', 'paramiko'])
    #deze functies zetten de hele rerver comunnictie tussen host en gast op
    Make = RemoteServer.OpenConnect()
    RemoteServer.Auth(Make)
    sftp = RemoteServer.Login(Make)
    return sftp, Make

def locationcheck(Location, string): # verantwoordelijk voor het controleren of het opgegeven al bestaat.
    while (os.path.isdir(Location)) == False and (os.path.isfile(Location)) == False:
            print("Locatie is incorrect")
            Location = input(string)
    return Location

def recoverDir(BackupSoort,backupLocation, toLocation, sftp):

        DirFiles = os.listdir(backupLocation)
        os.chdir(backupLocation) #Veranderd huidige positie naar de backup directory
        # ga elke file af in de opgevraagde director/ 1 voor 1 kopieren
        for file in DirFiles:
                CheckIfDir = os.path.isdir(file) # controleerd of file een directory is

                # Als file geen directory is kopier naar backup locatie
                if CheckIfDir == False:

                        # check of de backup local of op de remote server plaats vind
                        if BackupSoort == '1':
                                shutil.copy(file , toLocation)
                        elif BackupSoort == '2': #als server gebruik put functie in sftp
                                
                                sftp.put(file,os.path.join(toLocation, file)) 

                else: # als file een directory is doe niks/ sla over
                        pass
        

def recoverFile(BackupSoort,backupLocation, toLocation, sftp):       
        absolutePath= os.path.abspath(backupLocation)
        DestinationFile = toLocation

        #checkt of backup locaal of op remote server is
        if BackupSoort == '1':
                shutil.copy(backupLocation, toLocation)
        elif BackupSoort == '2':# Als het op server plaats vin gebruik secure file transfer protecol
                sftp, Make = server()
                sftp.put(backupLocation, toLocation)
                RemoteServer.Close(sftp,Make)

def ask():
    backupLocation = input("Wat is de locatie van de back-up: ") # vraagt de locatie van de backup
    backupLocation=locationcheck(backupLocation, "Wat is de locatie van de back-up: ") # controleert of de opgegeven locatie correct is

    toLocation = input("Wat is de locatie waar het naar toe moet: ") # vraagt waar de backup naartoe moet
    toLocation = locationcheck(toLocation,"Wat is de locatie waar het naar toe moet:")# controleert of de opgegeven locatie correct is

    if (os.path.isdir(backupLocation) == True and os.path.isfile(toLocation) == True ): # als hij een dir naar een bestand probeert te sturen staat niet toe
        print("Een map kan niet naar een bestand")
        backupLocation, toLocation = ask() # Vraagt het nog een keer
        return backupLocation, toLocation # als het goed is gegaan stuurt hij het gelijk terug

    print("\nBackup: {}\nTo: {}".format(backupLocation,toLocation)) # Geeft gegevens die zijn ingevuld terug voor controlle

    correctCheck = False #  om te controlleren dat de output goed is gecontroleerd
    while correctCheck != True:
        check = input("\nDit zijn de gegevens klopt dit? (Yes,No,Cancel): ") # vraagt of de gegevens goed zijn
        if check.lower() == "n" or check.lower() == "no":  # als dat niet het geval is vraag hij nog eens
            backupLocation, toLocation = ask()
            correctCheck = True            
        elif check.lower() == "c" or check.lower() == "cancel": # Sluit het programma af
            correctCheck = True
            print("Quitting...")
            return "QUIT", "QUIT" # Dit is los omdat het anders het sluit voordat de ssh verbinding is gesloten
        elif check.lower() == "y" or check.lower() == "yes": # Als er niks fout is gaat hij verder
            correctCheck = True
            return backupLocation, toLocation
            continue
        else: # zodat de output goed gecontrolleerd is moet een goede input gegeven worden
            correctCheck = False
            print("Verkeerde input")



BackupSoort = input('Waar staat de back-up \n1) Locaal opgeslagen \n2) Op de backupserver\n: ')

if BackupSoort == "2":
    sftp, Make = server()
    backupLocation, toLocation = ask()
    if backupLocation == "QUIT": # als hij moet stoppen doet hij dat nu zodat de ssh wordt gesloten
        RemoteServer.Close(sftp,Make)
        quit()
    if os.path.isfile(backupLocation): # test of de backup een bestand of dir is
        recoverFile(BackupSoort, backupLocation, toLocation, sftp)
    elif os.path.isdir(backupLocation): 
        recoverDir(BackupSoort, backupLocation, toLocation, sftp)
    RemoteServer.Close(sftp,Make) # sluit de server

elif BackupSoort == "1":
    backupLocation, toLocation = ask()
    if backupLocation == "QUIT": # als hij moet stoppen doet hij dat nu
        quit()
    if os.path.isfile(backupLocation): # test of de backup een bestand of dir is
        recoverFile(BackupSoort, backupLocation, toLocation, sftp)
    elif os.path.isdir(backupLocation): 
        recoverDir(BackupSoort, backupLocation, toLocation, sftp)
