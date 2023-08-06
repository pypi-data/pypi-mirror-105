from termcolor import cprint



def rc():
    """Entry point for the application script"""
    cprint("copy all rc files to places where they suppose to be", "red")
    rc_map = {
        "vimrc": "",
        "inputrc": "",
        "tmux.config": "",
    }
    for file_name, path in rc_map.items():
        pass


def debug_command():
    pass
