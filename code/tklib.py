import tkinter as tk
from typing import Literal
from PIL import Image, ImageTk

darkMode:bool = False
debug:bool = False

NUMS = list('3456789abc')
global i
i = 0

def pack(part:tk.Widget, padx:int=25, pady:int=25, side:Literal['left', 'right', 'top', 'bottom']=None) -> None:
    """Packs a subclass of tk.Widget with predefined values to ease padding etc. If tklib.darkMode is True the Widget background gets turned dark
    
    Args:
        part (tk.Widget): The Widget to pack
        padx (int, optional): Defaults to 25.
        pady (int, optional): Defaults to 25.
        side (Literal['left', 'right', 'top', 'bottom'], optional): Defaults to None.
    """
    if darkMode: part.configure(bg='#101010')
    global i
    if darkMode and debug: part.configure(bg='#x0x0x0'.replace('x', NUMS[i])); i += 1
    part.pack(padx=padx, pady=pady, side=side)
    
def root(title:str='', imagePath:str=None) -> tk.Tk:
    """Easyer way to create a root. If tklib.darkMode is True, the background is turned black.

    Args:
        title (str, optional): The title of the window. Defaults to ''.
        image (tk.PhotoImage, optional): The icon of the window. Defaults to None.

    Returns:
        tk.Tk: The generated window.
    """
    
    r = tk.Tk()
    r.title(title)
    if imagePath: r.iconphoto(True, tk.PhotoImage(master=r, file=imagePath))
    
    if darkMode: r.configure(bg='#101010')
    
    else: r.iconphoto(True, ImageTk.PhotoImage(Image.new('RGBA', (1, 1), (0, 0, 0, 255))))
    return r

def fullscreen(root:tk.Tk) -> None:
    """Fullscreens the window

    Args:
        root (tk.Tk): The window to fullscreen.
    """
    root.attributes('-fullscreen', True)
