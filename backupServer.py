import platform
import os 
import datetime
import shutil




date = datetime.datetime.now()
system=  platform.system()


try:
        import tkinter as tk
        from tkinter.filedialog import askopenfile

        import pip
        pip.main(['install', 'pillow'])
        from PIL import Image, ImageTk

        pip.main(['install', 'PyPDF2'])
        import PyPDF2

except ModuleNotFoundError:
        if system == 'Darwin':

                import pip
                pip.main(['install', 'python3-tk'])
                import tkinter as tk
                from tkinter.filedialog import askopenfile

                pip.main(['install', 'pillow'])
                from PIL import Image ,ImageTk

                pip.main(['install', 'PyPDF2'])
                import PyPDF2

        elif system == 'Windows':

                import pip
                pip.main(['install', 'pillow'])
                from PIL import Image, ImageTk
                
                pip.main(['install', 'python3-tk'])
                import tkinter as tk
                from tkinter.filedialog import askopenfile

                pip.main(['install', 'PyPDF2'])
                import PyPDF2
                
                


#Onze hoofdscherm voor GUI aanmaken
root = tk.Tk()

#onze werkscherm maken we hier aan (onze scherts en werk veld/doek)
canvas = tk.Canvas(root, width= 700, height= 750) # 550 X 900 is schermgrootte
canvas.grid(columnspan=6, rowspan= 8) # dit verdeeld onze scherm in 3 onzichtbare stukken ( een 3 x 3 grid)

#logo implementatie
logo = Image.open('/Users/yildiray/Pictures/LogoX.png') #opent betreffende logo-file
logo = ImageTk.PhotoImage(logo)#converteerd de image / opent hem als een tkinter image
logo_label = tk.Label(image=logo) # maakt een object waar de logo in kan
logo_lable_image = logo #Plaatst de logo/image in het object
logo_label.grid(column=0, row=0)# plaatst het object met de logo op de scherm

#optie menu en userinput velden
instructieBackupVorm = tk.Label(root, text="Hoe wilt u de backup opslaan", font="Raleway") #maak instuctie aan
instructieBackupVorm.grid(columnspan=1,column=0,row=1)# plaats instructie op scherms


#scherm sluiten
def Close():
        root.destroy()
#als er gekozen word voor lokaal opslag toon de opties voor lokaal opslag
def local(aanroep):
        BackupVorm = '1'


        # destroy all widgets from frame

        if aanroep == '0':
                window1 = tk.Toplevel()
        elif aanroep =='1':
                window1 = tk.Tk()
        canvas = tk.Canvas(window1, width= 700, height= 750) # 550 X 900 is schermgrootte
        canvas.grid(columnspan=6, rowspan= 20) # dit verdeeld onze scherm in 3 onzichtbare stukken ( een 3 x 3 grid)
        


        #logo implementatie
        logo1 = Image.open('/Users/yildiray/Pictures/LogoX.png') #opent betreffende logo-file
        logo1 = ImageTk.PhotoImage(logo1)#converteerd de image / opent hem als een tkinter image
        logo_label = tk.Label(window1,image=logo1) # maakt een object waar de logo in kan
        logo_lable_image = logo1 #Plaatst de logo/image in het object
        logo_label.grid(column=0, row=0)# plaatst het object met de logo op de scherm

        def openFile():
                file = str(askopenfile(parent=window1,mode='rb',title="Kies een file"))
                if file:
                        dirFiles= file.split("'")
                        file= dirFiles[1]
                        print(file)

        #Backup file(s) instructie(s)
        instructieBackupVorm1 = tk.Label(window1, text="kies uw backup", font="Raleway") #maak instuctie aan
        instructieBackupVorm1.grid(column=0,row=3)# plaats instructie op scherms

        instructieBackupVorm1 = tk.Label(window1, text="kies een bestand waar u een backup van wilt maken", font="Raleway") #maak instuctie aan
        instructieBackupVorm1.grid(columnspan=1,column=0,row=4)# plaats instructie op scherms


        #open een backupbestand knop
        LocalTekst2= tk.StringVar() # maakt data type aan voor tekst in knop / container
        LocalOptie2 = tk.Button(window1, text='backup file',textvariable=LocalTekst2, font="Raleway", height=2 , width=14, highlightbackground="#20bebe", fg="#58646a", command=lambda:openFile())# maakt de knop aan
        LocalTekst2.set("backup nu")# maakt de tekst aan/ zet tekst in container
        LocalOptie2.grid(column=1,row=4)

        #backup directory pad specificeren
        instructieBackupVorm1 = tk.Label(window1, text="Voor een directory backup voer de directory pad in:", font="Raleway") #maak instuctie aan
        instructieBackupVorm1.grid(columnspan=1,column=0,row=6)# plaats instructie op scherms

        #invoer scherm om de directory pad aan te geven
        invoerveld1 = tk.Entry (window1, textvariable='bijv.: home/user/Downloads',width=30) 
        invoerveld1.grid(column= 1, row=6)

        #Backup locatie instructies
        instructieBackupVorm1 = tk.Label(window1, text="Waar wilt u de backup opslaan. Bijv. home/user/etc", font="Raleway") #maak instuctie aan
        instructieBackupVorm1.grid(columnspan=1,column=0,row=8)# plaats instructie op scherms

        #invoer scherm om de backup locatie aan te geven
        invoerveld2 = tk.Entry (window1, textvariable='bijv.: home/user/Downloads',width=30) 
        invoerveld2.grid(column= 0, row=9)

        #start backup knop
        LocalTekst2= tk.StringVar() # maakt data type aan voor tekst in knop / container
        LocalOptie2 = tk.Button(window1, text='backup file',textvariable=LocalTekst2, font="Raleway", height=2 , width=14, highlightbackground="#20bebe", fg="#58646a", command=lambda:openFile())# maakt de knop aan
        LocalTekst2.set("start backup")# maakt de tekst aan/ zet tekst in container
        LocalOptie2.grid(column=1,row=9)



        window1.mainloop()



#Backup optie knoppen lokaal optie
LocalTekst= tk.StringVar() # maakt data type aan voor tekst in knop / container
LocalOptie = tk.Button(root, textvariable=LocalTekst, font="Raleway", height=4 , width=20, highlightbackground="#20bebe", fg="#58646a", command=lambda:local('0'))# maakt de knop aan
LocalTekst.set("lokaal")# maakt de tekst aan/ zet tekst in container
LocalOptie.grid(column=0,row=2)

#als er word gekozen voor opslag op de remote server
def ServerOptie():
        BackupVorm='2'
        aanroep = '1'
        # destroy all widgets from frame


        window2 = tk.Tk()
        canvas = tk.Canvas(window2, width= 700, height= 750) # 550 X 900 is schermgrootte
        canvas.grid(columnspan=6, rowspan= 25) # dit verdeeld onze scherm in 3 onzichtbare stukken ( een 3 x 3 grid)
        


        #info tekst
        instructieBackupVorm = tk.Label(window2, text="Server Login - Access", font="Raleway") #maak instuctie aan
        instructieBackupVorm.grid(columnspan=1,column=0,row=1)# plaats instructie op scherms

        #Instructies om verbinding te maken meet server
        instructieBackupVorm = tk.Label(window2, text="Hostnaam", font="Raleway") #maak instuctie aan
        instructieBackupVorm.grid(columnspan=1,column=0,row=2)# plaats instructie op scherms

        #optie menu en userinput velden
        instructieBackupVorm = tk.Label(window2, text="Poort", font="Raleway") #maak instuctie aan
        instructieBackupVorm.grid(columnspan=1,column=1,row=2)# plaats instructie op scherms

        #invoer scherm voor host name
        invoerveldH = tk.Entry (window2,width=20) 
        invoerveldH.grid(column= 0, row=3)

         #invoer scherm voor poort waarop server draait
        invoerveldP = tk.Entry (window2,width=20) 
        invoerveldP.grid(column= 1, row=3)

         #Instructies om verbinding te maken meet server
        instructieBackupVorm = tk.Label(window2, text="Gebruiker", font="Raleway") #maak instuctie aan
        instructieBackupVorm.grid(columnspan=1,column=0,row=4)# plaats instructie op scherms


        #invoer scherm voor de gebruikersnaam van de server
        invoerveldU = tk.Entry (window2,width=20) 
        invoerveldU.grid(column= 0, row=5)

        #Instructies om verbinding te maken meet server
        instructieBackupVorm = tk.Label(window2, text="Wachtwoord", font="Raleway") #maak instuctie aan
        instructieBackupVorm.grid(columnspan=1,column=1,row=4)# plaats instructie op scherms


        #invoer scherm voor de wachtwoord van de gebruiker
        invoerveldW = tk.Entry (window2,width=20,show='*') 
        invoerveldW.grid(column= 1, row=5)

        def verbindServer():
                UserImputHost = invoerveldH.get()
                UserImputPort = invoerveldP.get()
                UserImputName = invoerveldU.get()
                UserImputPass = invoerveldW.get()

                infoData = [UserImputHost,UserImputPort,UserImputName,UserImputPass]
                print(infoData)

                class RemoteServer:
                        # opent een connecte met de ssh host
                        def OpenConnect():
                                Host = infoData[0]
                                Port = int(infoData[1])
                                Make = paramiko.Transport((Host,Port))
                                return Make

                        #Handeld de authenticatie met de ssh host / remote server af
                        def Auth(Make):
                                UserName = infoData[2]
                                Password = infoData[3]
                                Make.connect(None, UserName, Password)

                        #Maakt connectie met de remote server
                        def Login(Make):
                                sftp = paramiko.SFTPClient.from_transport(Make)
                                return sftp

                        #sluit verbinding met remote server af
                        def Close(sftp,Make):
                                if sftp: sftp.close()
                                if Make: Make.close()

                if BackupVorm == '2':
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

                        status = str(sftp)
                        check= []
                        for item in status:
                                check.append(item)
                        print(status)
                        if '<' in status and '>' in status:
                                window2.destroy()
                                window2.mainloop()
                                
                

        #verbind knop
        VerbindTekst= tk.StringVar() # maakt data type aan voor tekst in knop / container
        VerbindKnop = tk.Button(window2, text='Verbind', font="Raleway", height=2 , width=13, highlightbackground="#20bebe", fg="#58646a", command=lambda:[verbindServer(),local('1')])# maakt de knop aan
        VerbindTekst.set("Verbinden")# maakt de tekst aan/ zet tekst in container
        VerbindKnop.grid(column=0,row=6)

        return aanroep




      
   

#Backup optie knoppen server optie
ServerTekst= tk.StringVar() # maakt data type aan voor tekst in knop / container
ServerOp = tk.Button(root, textvariable=ServerTekst, font="Raleway", height=4 , width=20, highlightbackground="#20bebe", fg="#58646a", command=lambda:[Close(),ServerOptie()])# maakt de knop aan
ServerTekst.set("server")# maakt de tekst aan/ zet tekst in container
ServerOp.grid(column=1,row=2)

canvas = tk.Canvas(root, width= 600, height= 600) # 550 X 900 is schermgrootte
canvas.grid(columnspan=6) # dit verdeeld onze scherm in 3 onzichtbare stukken ( een 3 x 3 grid)



root.mainloop()








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





#Hier word onze GUI afgesloten / hele GUI vind plaats tussen root en mainloop






