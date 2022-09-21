#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pygame
import os
import config
import tkinter
from tkinter.filedialog import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from mutagen.easyid3 import EasyID3
from tkinter.messagebox import *
from PIL import Image, ImageTk
from time import time
from mutagen.mp3 import MP3

SONG_END = pygame.USEREVENT + 1
pygame.init()
config.i=[]
config.d=0
config.a=''

    
def play_list():
    directory = askopenfilenames()
    for song in directory:
        config.i.append(song)
    return config.i
 
    
def check_music():
    for event in pygame.event.get():
          if event.type == SONG_END:
                next_song() 
    root.after(10, check_music)


def play_music():
    pygame.mixer.init()
    pygame.mixer.music.set_endevent(SONG_END)
    config.a=config.i[config.d]
    pygame.mixer.music.load(config.a)
    pygame.mixer.music.play()
    config.paused = False   
    listbox.delete(1)
    try:
        song = EasyID3(config.a)
        listbox.insert(1,song['title'])
    except:
        listbox.insert(1,"No file name found")
    root.after(10, check_music)
    update_pbar()
    
    
        
def pause():
    if (config.paused == True):
        pygame.mixer.music.unpause()
        config.paused= False
    elif (config.paused == False):
        pygame.mixer.music.pause()
        config.paused=True
def next_song():
    if (config.d<(len(config.i)-1)):
        config.d+=1
        play_music()
def prev_song():
    if (config.d>0):
        config.d-=1
        play_music()
        
def update_pbar():
    song = MP3(config.a)
    song_length = song.info.length
    pos= pygame.mixer.music.get_pos()/1000
    perc = (pos/song_length)*100
    progress_bar['value'] = perc
    root.after(100,update_pbar)

    
def exit():
    pygame.mixer.music.stop()
    os._exit(0)
    root.destroy()
    
root = Tk()
root.title('MP3 Player')
root.minsize(300,300)


image = Image.open(r"C:\Users\ekalv\Downloads\clef.ppm")
photo = ImageTk.PhotoImage(image)

label1 = Label(image=photo)
label1.image = photo
label1.pack()

listbox = Listbox(root, height = 3, width = 50)
listbox.pack()
listbox.insert(0, "now playing :")


progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=500)
progress_bar.pack()

pausebutton = tkinter.Button(root,command = pause, text='Pause')
pausebutton.pack()

playbutton=Button(root,command = play_music,text='Play')
playbutton.pack()


nextbutton = Button(root,command = next_song, text = 'Next')
nextbutton.pack()

previousbutton = Button(root,command = prev_song,text = 'Prev')
previousbutton.pack()

queuebutton=Button(root,command = play_list, text='Add to queue')
queuebutton.pack()

exitbutton=Button(root,command = exit, text='Exit')
exitbutton.pack()


root.mainloop()
