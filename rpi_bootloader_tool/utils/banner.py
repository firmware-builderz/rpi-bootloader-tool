from .version import version


def logo():

    return f"""\033[92m
     ____  ____ ___    _____           _ 
    |  _ \|  _ \_ _|  |_   _|__   ___ | |   |   \033[95m Welcome to RPI-Tool \033[92m
    | |_) | |_) | |_____| |/ _ \ / _ \| |   |   \033[95m Version : {version} \033[92m
    |  _ <|  __/| |_____| | (_) | (_) | |   |   \033[95m https://github.com/firmware-builderz/rpi-bootloader-tool \033[92m
    |_| \_\_|  |___|    |_|\___/ \___/|_|   |   \033[95m Author : hexzhen3x7 \033[92m
    
    
    \033[0m
    """