from .utils import check_dependencies
check_dependencies()


import cmd
import os
import sys
import requests
import zipfile
import io
import curses


from tqdm import tqdm
from datetime import datetime

from .modules import *
from .modules import module_list, all_modules
from .utils import logo, about, update





completions = module_list()




class RpiBootloaderTool(cmd.Cmd):
    
    update(where="main_menu")

    
    
    intro = logo()
    
    prompt = 'rpi-tool > '
    
    doc_header = 'Commands'
    undoc_header = 'Undocumented Commands'





    def do_get_bootloader(self, arg):
        "Download Bootloader: get_bootloader"
        print("Bootloader Downloading...")

    def do_get_eeprom(self, arg):
        "Download EEPROM: get_eeprom"
        print("EEPROM Downloading...")


    def do_help(self, arg):
        """
        Zeigt allgemeine Hilfe für das Programm.
        """
        print("Hilfe: Willkommen im Raspberry Pi Bootloader - Download Utility.")
        print("Verfügbare Befehle:")
        print("  get_bootloader   - Download Bootloader")
        print("  get_eeprom       - Download EEPROM")
        print("  update           - Prüfe auf Updates")
        print("  about            - Informationen über das Tool")
        print("  help             - Zeigt diese Hilfe-Seite")
        print("  exit             - Beendet das Tool")

    def help_get_bootloader(self):
        """
        Zeigt spezifische Hilfe für den 'get_bootloader' Befehl.
        """
        print("get_bootloader - Lädt den Bootloader herunter.")
        print("Verwendung: Geben Sie 'get_bootloader' ein, um den Bootloader herunterzuladen.")
        print("Weitere Informationen finden Sie in der offiziellen Dokumentation.")

    def help_get_eeprom(self):
        """
        Zeigt spezifische Hilfe für den 'get_eeprom' Befehl.
        """
        print("get_eeprom - Lädt das EEPROM herunter.")
        print("Verwendung: Geben Sie 'get_eeprom' ein, um das EEPROM herunterzuladen.")

    def do_show(self, line):
        """Show available modules"""
        all_modules()

    def do_set(self, line):
        """set options"""
        try:
            key, value = line.split(' ')
            print(key, value)
            self.parameters.update({key: value})
        except KeyError:
            print(f"*** Unknown Option! option not has value!")
        except ValueError:
            print(f"*** Option not has value!")
            print(f"*** Example : set host 127.0.0.1")
          
    def do_use(self, line):
        """Select module for modules"""
        if line in module_list():

            module = globals()[line]
            if hasattr(module, 'Main'):
                module = module.Main()
                module.prompt = f"rpi-tool > {line} > "
                module.cmdloop()
            else:
                print(f"*** Module `{module}` not has `Main` class!")

        else:
            print(f"*** Module {line} not found!")
                
    def do_options(self, line):
        """Show options of current module"""
        print("\n")
        print(f"{'Option':20}\t{'Value':20}")
        print(f"{'--'*8:<20}\t{'--'*8:<20}")
        for k,v in self.parameters.items():
            print(f"{k:20}\t{v:20}")
        print("\n")
        
    def do_back(self, *args):
        """go back one level"""
        return True

    def do_about(self, line):
        """About Us"""
        about()

    def do_update(self, line):
        """Check for update"""
        update(where="update_command")
        
    def do_exit(self, line):
        """exit websploit"""
        sys.exit(0)


    

    def complete_use(self, text, line, begidx, endidx):
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in completions if s.startswith(mline)]
    
    def complete_set(self, text, line, begidx, endidx):
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in self.completions if s.startswith(mline)]

    def default(self, line):
        cmd, arg, line = self.parseline(line)
        func = [getattr(self, n) for n in self.get_names() if n.startswith('do_' + cmd)]
        if func: # maybe check if exactly one or more elements, and tell the user
            func[0](arg)
        else:
            os.system(line)




    




def loop():
    try:
        RpiBootloaderTool().cmdloop()
    except KeyboardInterrupt:
        print("\nBye!")

if __name__ == '__main__':
    loop()

    