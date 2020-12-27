import os
import shutil

def locationcheck(Location, string): # verantwoordelijk voor het controleren of het opgegeven al bestaat.
    while (os.path.isdir(Location)) != True:
        if (os.path.isfile(Location)) == True:
            break
        else:
            print("Locatie is incorrect")
            Location = input(string)
    return Location

def ask():
    backupLocation = input("Wat is de locatie van de back-up: ") # vraagt de locatie van de backup
    backupLocation=locationcheck(backupLocation, "Wat is de locatie van de back-up: ") # controleert of de opgegeven locatie correct is

    toLocation = input("Wat is de locatie waar het naar toe moet: ") # vraagt waar de backup naartoe moet
    toLocation = locationcheck(toLocation,"Wat is de locatie waar het naar toe moet:")# controleert of de opgegeven locatie correct is

    if (os.path.isfile(backupLocation)) == True: # WIP bedoelt om losse bestanden te kunnen doen
        pass

    print("\nBackup: {}\nTo: {}".format(backupLocation,toLocation)) # Geeft gegevens die zijn ingevuld terug voor controlle

    check = input("\nDit zijn de gegevens klopt dit? (y,n,c) ") # vraagt of de gegevens goed zijn
    if check.lower() == "n":  # als dat niet het geval is vraag hij nog eens
        backupLocation, toLocation = ask()
    elif check.lower() == "c":
        quit()
    
    return backupLocation, toLocation

backupLocation, toLocation = ask()

DirectoryFiles = os.listdir(backupLocation) # verkrijgt de naam van alle bestanden in de backup directory
os.chdir(backupLocation) # zodat het controleren op dir makelijker is
for file in DirectoryFiles: 
        checkIfDir = os.path.isdir(file) 

        if checkIfDir == False: # als het bestand geen dir is copieerd hij het niet
                shutil.copy(file, toLocation) # hier copieerd hij het
        else:
                pass
print("Done")