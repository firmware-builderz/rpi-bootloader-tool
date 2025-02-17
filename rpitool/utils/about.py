import platform
from .version import version


def about():
    s_color = "\033[92m" if platform.system() != "Windows" else ""
    e_color = "\033[0m" if platform.system() != "Windows" else ""
    about = f"""{s_color}
    
            Raspberry Bootloader Download Tool
            Author  : hexzhen3x7
            Contact : hexzhen3x7@outlook.de
            Version : """ + version + """
            Project Github : https://github.com/websploit/websploit
            Other Projects : https://github.com/0x0ptim0us
            
    {e_color}"""
    print(about)