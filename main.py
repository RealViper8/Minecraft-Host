import os
import pystyle
import configparser
import wget
import psutil
import zipfile
from jdk4py import JAVA, JAVA_HOME, JAVA_VERSION

config = configparser.ConfigParser()
curdir = os.getcwd()

def get_version(version_name : str, link : str, count : int | str):
    config.read("config.ini")
    os.chdir("Versions")
    try: os.mkdir(version_name.replace("-","."))
    except: pass
    os.chdir(version_name.replace("-","."))
    ver2 = version_name.replace("-",".")
    try:
        if not os.path.exists(version_name+".jar"): wget.download(link,out=version_name+".jar",bar=lambda current, total, width=80: wget.bar_adaptive(round(current/1024/1024, 2), round(total/1024/1024, 2), width) + ' MB')
        else: print(pystyle.Colors.green+"Version already exists !"+pystyle.Colors.reset)
        print()
        print(pystyle.Colors.blue+"[*] Version "+ver2+" was downloaded !"+pystyle.Colors.reset)
        os.system("pause")
    except:
        print(pystyle.Colors.red+"Please check your internet connection and try again !"+pystyle.Colors.reset)
        os.system("pause")
    os.chdir(curdir)
    if not config.has_section("InstalledVersions"): config.add_section("InstalledVersions")
    config.set("InstalledVersions","version"+str(count),ver2)
    with open("config.ini","w") as f: config.write(f)

def main() -> None:
    while True:
        os.system("clear" if os.name == "posix" else "cls")
        os.system("color 0a & title Main")
        print("\n--MINECRAFT-SERVER--")
        print("\n1. Host")
        print("2. Versions")
        print("3. Configure")
        print("4. Delete Version")
        print()
        I = pystyle.Write.Input("Number -> ",pystyle.Colors.blue_to_green,interval=0.025)
        if I == "1":
            os.system("title HOST")
            try:
                os.chdir(curdir)
                config.read("config.ini")
                if not config.has_section("System"):
                    config.add_section("System")
                    config.set("System","Installed","False")
                    config.set("System","localhost","True")
                    with open("config.ini","w") as f: config.write(f); f.close()
                if not config.has_option("System","ngrok_token") or config.get("System","ngrok_token") == "":
                    print()
                    print(pystyle.Colors.green+"To get the token sign in or login : https://dashboard.ngrok.com/get-started/your-authtoken")
                    I = pystyle.Write.Input("Ngrok Auth Token -> ",pystyle.Colors.blue_to_green,interval=0.025)
                    if I == "" or I.isspace() or len(I) < 25:
                        print(pystyle.Colors.red+"The token is invalid !")
                        os.system("pause")
                        main()
                        break
                    config.set("System","ngrok_token",I if I != "" and not I.isspace() else "")
                    with open("config.ini","w") as f: config.write(f); f.close()
                config.read("config.ini")
                if config.has_section("InstalledVersions"):
                    os.system("clear" if os.name == "posix" else "cls")
                    os.system("color 0a")
                    print("Wich version do you want to host?")
                    count = 1
                    CurrentVersion = []
                    for i in config.items("InstalledVersions"):
                        print(str(count)+" "+i[1])
                        CurrentVersion.append(i[1])
                        count += 1
                    print(str(count)+" "+"Go Back\n")
                    I = pystyle.Write.Input("Number -> ",pystyle.Colors.green_to_blue,interval=0.025)
                    if I.isdigit():
                        os.chdir(curdir)
                        if int(I) == int(count):
                            main()
                            break
                        os.chdir("Versions")
                        os.chdir(CurrentVersion[int(I)-1])
                        print()
                        print(pystyle.Colors.light_green+"How much ram should the server use ? (GB)"+pystyle.Colors.reset)
                        RAM = pystyle.Write.Input("Ram in GB : ",pystyle.Colors.green_to_blue, interval=0.025)
                        print()
                        print(pystyle.Colors.dark_blue+"Do you want a graphical user interface? default = True"+pystyle.Colors.reset)
                        Gui = pystyle.Write.Input("Gui (True or False) -> ",pystyle.Colors.green_to_cyan, interval=0.025)
                        if Gui == "" or Gui.isspace() or Gui == None:
                            Gui = "True"
                        if RAM.isdigit():
                            Ram = (int(RAM) * 1000) + int(RAM) * 24
                            CorrectRam = psutil.virtual_memory().available / 1000000
                            if Ram > CorrectRam:
                                print(pystyle.Colors.red+"You cant set the ram to "+str(Ram)+" when your available ram is "+str(int(CorrectRam) / 1000)+" GB"+pystyle.Colors.reset)
                                Ram = 1024
                            print(pystyle.Colors.green+"SERVER IS STARTING ON LOCALHOST" if config.get("System","localhost") == "True" else pystyle.Colors.green+"SERVER IS STARTING ON NGROK")
                            if config.get("System","localhost") == "False":
                                if not os.path.exists("eula.txt"):
                                    print(pystyle.Colors.green+"Please wait !"+pystyle.Colors.reset)
                                    os.system("timeout 7 > nul")
                                    f = open("eula.txt","w")
                                    f.write("eula=TRUE")
                                    f.close()

                                if os.path.exists("server.properties"):
                                    f = open("server.properties","r")
                                    Lines = f.readlines()
                                    f.close()
                                    for line in Lines:
                                        if line.__contains__("server-port"):
                                            port = line.replace("server-port","").replace("=","")
                                    Path2 = os.getcwd()
                                    os.chdir(curdir)
                                else:
                                    port = 25565
                                    Path2 = os.getcwd()
                                    os.chdir(curdir)

                                os.system("ngrok config add-authtoken "+config.get("System","ngrok_token"))
                                os.system("start ngrok.exe tcp "+ str(port))

                                os.chdir(Path2)

                                os.system(str(JAVA)+" -Xmx"+str(Ram)+"M"+" -Xms"+str(Ram)+"M"+" -jar "+str(CurrentVersion[int(I)-1]).replace(".","-")+".jar"+" "+"nogui" if Gui == "False" or Gui == "false" else str(JAVA)+" -Xmx"+str(Ram)+"M"+" -Xms"+str(Ram)+"M"+" -jar "+str(CurrentVersion[int(I)-1]).replace(".","-")+".jar")
                            
                                os.chdir("Versions")
                                os.chdir(CurrentVersion[int(I)-1])
                            else:
                                os.system("color 0a")
                                if not os.path.exists("eula.txt"):
                                    print(pystyle.Colors.green+"Please wait !"+pystyle.Colors.reset)
                                    os.system("timeout 7 > nul")
                                    f = open("eula.txt","w")
                                    f.write("eula=TRUE")
                                    f.close()
                                print(Gui)
                                os.system("pause")
                                os.system(str(JAVA)+" -Xmx"+str(Ram)+"M"+" -Xms"+str(Ram)+"M"+" -jar "+str(CurrentVersion[int(I)-1]).replace(".","-")+".jar"+" "+"nogui" if Gui == "False" or Gui == "false" else str(JAVA)+" -Xmx"+str(Ram)+"M"+" -Xms"+str(Ram)+"M"+" -jar "+str(CurrentVersion[int(I)-1]).replace(".","-")+".jar")
                        try: os.system("taskkill /F /IM  ngrok.exe /T")
                        except: print(pystyle.Colors.green+"[-] Tried closing ngrok process it was already closed !"+pystyle.Colors.reset)
                else:
                    print(pystyle.Colors.red+"You dont have any versions installed !\nInstall some in the main menu")
                    os.system("pause")
            except Exception as E:
                print(E)
                os.system("pause")
        elif I == "2":
            config.read("config.ini")
            os.system("title Version & color 0a")
            os.system("clear" if os.name == "posix" else "cls")
            print("\n--VERSIONS--")
            print("\n1. 1.20.1")
            print("2. 1.20")
            print("3. 1.19.4")
            print("4. 1.19.3")
            print("5. 1.19.2")
            print("6. 1.19.1")
            print("7. 1.19")
            print("8. 1.18.2")
            print("9. 1.18.1")
            print("10. 1.18")
            print("11. 1.17")
            print("12. 1.16.5")
            print("13. Go Back")
            Version = ["1.20.1","1.20","1.19.4","1.19.3","1.19.2","1.19.1","1.19","1.18.2","1.18.1","1.18","1.17","1.16.5"]
        
            os.chdir(curdir)

            if not os.path.exists("Versions"): os.mkdir("Versions")
            if not config.has_section("Versions"): 
                config.add_section("Versions")
                with open("config.ini","w") as f: config.write(f); f.close()
            count = 0
            for i in Version:
                config.set("Versions","Version"+str(count),Version[count])
                count += 1
                f = open("config.ini","w")
                config.write(f)
                f.close()

            I = pystyle.Write.Input("Number -> ",pystyle.Colors.green_to_cyan,interval=0.025)
            if I == "1":
                get_version(version_name="1-20-1",link="https://piston-data.mojang.com/v1/objects/84194a2f286ef7c14ed7ce0090dba59902951553/server.jar",count=0)
            elif I == "2":
                get_version(version_name="1-20",link="https://piston-data.mojang.com/v1/objects/15c777e2cfe0556eef19aab534b186c0c6f277e1/server.jar",count=1)
            elif I == "3":
                get_version(version_name="1-19-4",link="https://piston-data.mojang.com/v1/objects/8f3112a1049751cc472ec13e397eade5336ca7ae/server.jar",count=2)
            elif I == "4":
                get_version(version_name="1-19-3",link="https://piston-data.mojang.com/v1/objects/8f3112a1049751cc472ec13e397eade5336ca7ae/server.jar",count=3)
            elif I == "5":
                get_version(version_name="1-19-2",link="https://piston-data.mojang.com/v1/objects/f69c284232d7c7580bd89a5a4931c3581eae1378/server.jar",count=4)
            elif I == "6":
                get_version(version_name="1-19-1",link="https://piston-data.mojang.com/v1/objects/8399e1211e95faa421c1507b322dbeae86d604df/server.jar",count=5)
            elif I == "7":
                get_version(version_name="1-19",link="https://piston-data.mojang.com/v1/objects/e00c4052dac1d59a1188b2aa9d5a87113aaf1122/server.jar",count=6)
            elif I == "8":
                get_version(version_name="1-18-2",link="https://piston-data.mojang.com/v1/objects/c8f83c5655308435b3dcf03c06d9fe8740a77469/server.jar",count=7)
            elif I == "9":
                get_version(version_name="1-18-1",link="https://piston-data.mojang.com/v1/objects/125e5adf40c659fd3bce3e66e67a16bb49ecc1b9/server.jar",count=8)
            elif I == "10":
                get_version(version_name="1-18",link="https://piston-data.mojang.com/v1/objects/3cf24a8694aca6267883b17d934efacc5e44440d/server.jar",count=9)
            elif I == "11":
                get_version(version_name="1-17",link="https://piston-data.mojang.com/v1/objects/0a269b5f2c5b93b1712d0f5dc43b6182b9ab254e/server.jar",count=10)
            elif I == "12":
                get_version(version_name="1-16-5",link="https://piston-data.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar",count=11)
            elif I == "13":
                main()
                break
        elif I == "3":
            config.read("config.ini")
            os.system("clear" if os.name == "posix" else "cls"); os.system("title Configure & color 0a")
            print("\n--CONFIGURE--")
            if config.has_section("System") and config.has_option("System","localhost"):
                print("\n LOCAL HOST IS ON" if config.get("System","localhost") == "True" else "\nLOCAL HOST IS OFF")
            print("\n1. Set Localhost OFF")
            print("2. Set Localhost ON")
            print("3. Go Back")
            print()
            I = pystyle.Write.Input("Number -> ",pystyle.Colors.green, interval=0.025)
            if I == "1":
                print()
                print(pystyle.Colors.red+"[*] SETTING LOCALHOST OFF"+pystyle.Colors.reset)
                if config.has_section("System") and config.has_option("System","localhost"):
                    if config.get("System","localhost") == "True":
                        config.set("System","localhost","False")
                        with open("config.ini","w") as f: config.write(f); f.close()
                        print(pystyle.Colors.cyan+"Press enter to continiue"+pystyle.Colors.reset)
                        os.system("pause > nul")
                    else:
                        print(pystyle.Colors.cyan+"Press enter to continiue"+pystyle.Colors.reset)
                        os.system("pause > nul")
                else:
                    config.add_section("System")
                    config.set("System","localhost","False")
                with open("config.ini","w") as f: config.write(f); f.close()
            elif I == "2":
                print()
                print(pystyle.Colors.green+"[*] SETTING LOCALHOST ON"+pystyle.Colors.reset)
                if config.has_section("System") and config.has_option("System","localhost"):
                    if config.get("System","localhost") == "False":
                        config.set("System","localhost","True")
                        with open("config.ini","w") as f: config.write(f); f.close()
                        print(pystyle.Colors.cyan+"Press enter to continiue"+pystyle.Colors.reset)
                        os.system("pause > nul")
                    else:
                        print(pystyle.Colors.cyan+"Press enter to continiue"+pystyle.Colors.reset)
                        os.system("pause > nul")         
                else:
                    config.add_section("System")
                    config.set("System","localhost","True")
                with open("config.ini","w") as f: config.write(f); f.close()
        elif I == "4":
            def Del():
                os.system("clear" if os.name == "posix" else "cls")
                os.chdir(curdir)
                config.read("config.ini")
                print("\n--DELETE-VERSION--")
                os.system("color 0a")
                print("\nWich version do you want to delete?")

                CurrentVersion = []
                if config.has_section("InstalledVersions"):
                    count = 1
                    for i in config.items("InstalledVersions"):
                        if count == 1:
                            print()
                        print(str(count)+" "+i[1])
                        CurrentVersion.append(i[1])
                        count += 1
                    if len(config.items("InstalledVersions")) == 0:
                        print()
                        print("You dont have any versions installed !")
                else:
                    count = 1
                print(str(count)+" "+"Go Back\n")
                I = pystyle.Write.Input("Number -> ",pystyle.Colors.green_to_blue,interval=0.025)
                if I.isdigit():
                    os.chdir(curdir)
                    if int(I) == int(count):
                        main()
                    os.chdir("Versions")
                    try: os.system("rmdir /S /Q "+CurrentVersion[int(I)-1])
                    except: print(pystyle.Colors.red+"Error: Something unexpected happend"+pystyle.Colors.reset)
                    os.system("pause")
                    Del()
            Del()

            


if __name__ == "__main__":
    if not os.path.exists("ngrok.exe") or os.path.exists("ngrok.zip"):
        if not os.path.exists("ngrok.zip"): wget.download("https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip","ngrok.zip")
        with zipfile.ZipFile("ngrok.zip","r") as zip_ref:
            zip_ref.extractall()
        os.system("del ngrok.zip")
    config.read("config.ini")
    if not os.path.exists("config.ini"):
        with open("config.ini","w") as f: f.close()
    else:
        config.read("config.ini")
        if config.has_section("InstalledVersions") and config.has_section("Versions"):
            for i in config.items("InstalledVersions"):
                try: 
                    os.chdir("Versions")
                    os.chdir(str(i[1]))
                except: pass

                if not os.path.exists(str(i[1]).replace(".","-")+".jar"):
                    os.chdir("..")
                    os.system("rmdir "+str(i[1]))
                    config.remove_option("InstalledVersions",str(i[0]))
                    os.chdir(curdir)
                    with open("config.ini","w") as f: config.write(f); f.close()
                else:
                    os.chdir(curdir)
        os.chdir(curdir)
        with open("config.ini","w") as f: config.write(f); f.close()
        config.read("config.ini")
        if not config.has_section("InstalledVersions"):
            os.system("rmdir Versions")
    main()