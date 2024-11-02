# region imports

import tkinter as tk
from tkinter import messagebox as tkmsg
import tklib

import lib as spy

import settingslib as slib

from urllib.request import urlopen
from PIL import Image, ImageTk, ImageDraw

import unicodedata

import os
import subprocess

import re

# endregion


class App:
    def __init__(self):
        self.settings = slib.Settings('settings.json', False)
        
        self.FONTBIG = (self.settings('font.bigfont.font'), self.settings('font.bigfont.size'))
        self.FONTSMALL = (self.settings('font.smallfont.font'), self.settings('font.smallfont.size'))
        self.FONTMINI = (self.settings('font.minifont.font'), self.settings('font.minifont.size'))
        
        tklib.darkMode = self.settings('debug.darkMode')
        tklib.debug = self.settings('debug.debug')
        
        self.root = tklib.root('SpotiPy Focus Mode', self.settings('images.appicon'))
        self.root.tk.call('tk', 'scaling', self.settings('window.scaling'))
        if self.settings('window.fullscreen'): tklib.fullscreen(self.root)
        
        # region mainFrame
        self.mainFrame = tk.Frame(self.root)
        tklib.pack(self.mainFrame, side='left')
        
        self.progressLabel = tk.Label(self.mainFrame)
        self.progressLabel.configure(fg=self.settings('font.minifont.color'), font=self.FONTMINI, justify='right', width=self.settings('font.minifont.limit'))
        tklib.pack(self.progressLabel, pady=5, padx=0)
        
        self.imageLabel = tk.Label(self.mainFrame, border=0)
        tklib.pack(self.imageLabel, side='top')
        
        
        self.subFrame = tk.Frame(self.mainFrame)
        tklib.pack(self.subFrame, side='left')
        
        self.artistLabel = tk.Label(self.subFrame)
        self.artistLabel.configure(fg=self.settings('font.smallfont.color'), font=self.FONTSMALL, justify='left', width=self.settings('font.smallfont.limit'))
        tklib.pack(self.artistLabel, pady=10)
        
        self.songLabel = tk.Label(self.subFrame)
        self.songLabel.configure(fg=self.settings('font.bigfont.color'), font=self.FONTBIG, justify='left', width=self.settings('font.bigfont.limit'))
        tklib.pack(self.songLabel, pady=10)
        # endregion
        
        # region controlFrame
        self.controlFrame = tk.Frame(self.root)
        tklib.pack(self.controlFrame)
        
        # images for buttons
        self.pauseImage = tk.PhotoImage(file=self.settings('images.pause'))
        self.playImage = tk.PhotoImage(file=self.settings('images.play'))
        self.skipImage = tk.PhotoImage(file=self.settings('images.skip'))
        self.settingsImage = tk.PhotoImage(file=self.settings('images.settings'))
        
        # pause button
        self.pauseButton = tk.Button(self.controlFrame, command=spy.playpause)
        self.pauseButton.config(border=0, image=self.pauseImage)
        tklib.pack(self.pauseButton, padx=10, side='left')
        
        # skip button
        self.skipButton = tk.Button(self.controlFrame, command=spy.next)
        self.skipButton.config(border=0, image=self.skipImage)
        tklib.pack(self.skipButton, padx=10, side='left')
        
        self.settingsButton = tk.Button(self.controlFrame, command=self.changesettings)
        self.settingsButton.config(border=0, image=self.settingsImage)
        tklib.pack(self.settingsButton, padx=10, side='left')
        # endregion
        
        
        self.update_all()
        
        self.root.mainloop()
        
    def update_all(self):
        # update
        self.current = spy.update()
        
        # calc progress
        progress_ms = self.current['progress_ms']
        duration_ms = self.current['item']['duration_ms']
        if duration_ms > 0:
            progress = round(progress_ms/duration_ms*self.settings('features.album_image.size'))
        else:
            progress = 0
            
        # progress label
        ps = progress_ms // 1000
        pm, ps = divmod(ps, 60)
        ds = duration_ms // 1000
        dm, ds = divmod(ds, 60)
        
        pm, ps, dm, ds = str(pm).zfill(2), str(ps).zfill(2), str(dm).zfill(2), str(ds).zfill(2)
        
        self.progressLabel.configure(text=self.settings('lang.progress').format(pm=pm, ps=ps, dm=dm, ds=ds))
        
        # process image (load & progress)
        self.image = self.load_image(self.current['item']['album']['images'][0]['url'], progress)
        
        # song name
        self.songName = self.remove_accents(f'{self.current["item"]["name"]} {"" if self.current["is_playing"] else self.settings('lang.paused')}')
        self.songName = re.sub(self.settings('re.feat'), '', self.songName.lower())
        self.songLabel.configure(text=self.songName)
        
        # artist name(s)
        self.artistName = self.remove_accents(f'{self.settings('lang.artist_split').join(\
            [artist['name']\
                for artist in self.current['item']['artists']])}')
        self.artistLabel.configure(text=self.artistName)
        
        # pause button
        if self.current['is_playing']:
            self.pauseButton.configure(image=self.pauseImage)
        else:
            self.pauseButton.configure(image=self.playImage)
        
        # save image
        self.imageLabel.configure(image=self.image)
        
        # rerun
        self.root.after(self.settings('features.wait_repeat'), self.update_all)

    def changesettings(self):
        os.system(f'python {self.settings("features.settings_editor")}')
        restart = tkmsg.askyesno(self.settings('lang.reload.title'), self.settings('lang.reload.message'))
        if restart:
            subprocess.Popen(['python', self.settings('features.main_file')])
            self.root.destroy()
            exit()


    def load_image(self, url:str, progress:int) -> tk.PhotoImage:
        ais = self.settings('features.album_image.size')
        
        if url == 'DEFAULT':
            image = Image.open(self.settings('images.default'))
        else:
            image = Image.open(urlopen(url))
        image.resize((ais, ais))
        image = self.progress_image(image, progress)
        image = self.add_corners(image, self.settings('features.album_image.rounding'))
        return ImageTk.PhotoImage(image=image)

    def progress_image(self, image:Image.Image, progress:int) -> Image.Image: 
        width = self.settings('features.album_image.progress_width')
        ais = self.settings('features.album_image.size')
        new_image = Image.new('RGB', (ais, ais), (255, 0, 0))
        new_image.paste(image, (0, 0))
        
        draw = ImageDraw.Draw(new_image, 'RGBA')
        
        # draw
        draw.rectangle(((ais-width, 0), (ais, progress)),
                    tuple(self.settings('features.album_image.progress_color'))) # right
          
        return new_image
    
    def add_corners(self, im, rad):
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im
    
    def remove_accents(self, text) -> str:
        normalized_text = unicodedata.normalize('NFD', text)
        return ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn')

    
App()
