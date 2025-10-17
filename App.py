#Install python3
# sudo apt install python3 
#python3 -m tkinter


from tkinter import *
import webbrowser
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
chrome = config['location']['chrome']
html_location = config['htmlfile']['html']
root = Tk()
root.geometry("600x200")
room = IntVar()
room.set(1)
v = IntVar()
v.set(1)

happy = Entry(root, text="Happy Birthday")
happy.insert(END, 'Happy Birthday')
happy.pack()

e = Entry(root, width=15)
e.pack(ipady=8)

def getVariables():
    roomColor = ""
    if room.get() == 1:
        roomColor = "Blue"
    elif room.get() == 2:
        roomColor = "Red"
    elif room.get() == 3:
        roomColor = "Yellow"
    else:
        roomColor = "Orange"
    return f"{roomColor}.html"

def getColor():
    color = getVariables()
    color = color.replace('.html', '')
    return color
  

def getVideo():
    if v.get() == 2:
        videoName = "fortnite.mp4"
    elif v.get() == 3:
        videoName = "harry.mp4"
    elif v.get() == 4:
        videoName = "pokemon.mp4"  
    elif v.get() == 5:
        videoName = "minecraft.mp4"
    elif v.get() == 1:
        videoName = "movie.mp4"
    return videoName

def getCSS():
    css = ""
    color = getColor()
    video = getVideo()
    if color == "Blue" and video != "movie.mp4":
        css = "Stylea.css"
    elif color == "Red" and video != "movie.mp4":
        css = "Styleb.css"
    elif color == "Yellow" and video != "movie.mp4":
        css = "Stylec.css"
    elif color == "Orange" and video != "movie.mp4":
        css = "Styled.css"
    elif color == "Blue":
        css = "Style.css"
    elif color == "Red":
        css = "Style1.css"
    elif color == "Yellow":
        css = "Style2.css"
    else:
        css = "Style3.css"
    return css


def openWebpage():
    roomColor = getVariables()
    file = open(roomColor,'w')
    message = f"""<html><head><link rel='stylesheet' href='{getCSS()}'></head><body><img src='bg.png'>
    <h1>{happy.get()}</h1><video autoplay muted loop id='myVideo'>
    <source src={getVideo()} type='video/mp4'>Video not found</video>
    <div class='innertext'>{e.get()}</div></body></html>"""
    file.write(message)
    file.close()
    chrome_path = f'{chrome} %s'
    try:
        webbrowser.get(chrome_path).open_new(f"{html_location}{roomColor}")
    except:
        print("Could not find chrome location")
        print("Did you edit the config.ini file?")
        print("Using default browser")
        webbrowser.get('windows-default').open(roomColor)
root.title("🎉 Party Room Display 🎉")
Radiobutton(root, text="Blue", variable=room, value=1).pack(side = "left")
Radiobutton(root, text="Red", variable=room, value=2).pack(side = "left")
Radiobutton(root, text="Yellow", variable=room, value=3).pack(side = "left")
Radiobutton(root, text="Orange", variable=room, value=4).pack(side = "left")

Radiobutton(root, text="Fireworks", variable=v, value=1).pack(side = "right")
Radiobutton(root, text="Fortnite", variable=v, value=2).pack(side = "right")
Radiobutton(root, text="Harry Potter", variable=v, value=3).pack(side = "right")
Radiobutton(root, text="Pokemon", variable=v, value=4).pack(side = "bottom")
Radiobutton(root, text="Minecraft", variable=v, value=5).pack(side = "bottom")

myButton = Button(root, text="Make A Party", command=lambda: openWebpage())
myButton.pack(side=TOP)

root.mainloop()
