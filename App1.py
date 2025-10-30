from tkinter import *
import webbrowser
from pathlib import Path

root = Tk()
root.geometry("600x250")
root.title("🎉 Party Room Display 🎉")

room = IntVar(value=1)
v = IntVar(value=1)

happy = Entry(root)
happy.insert(END, 'Happy Birthday')
happy.pack()

e = Entry(root, width=15)
e.pack(ipady=8)

def getVariables():
    if room.get() == 1:
        return "Blue.html"
    elif room.get() == 2:
        return "Red.html"
    elif room.get() == 3:
        return "Yellow.html"
    else:
        return "Orange.html"

def getColor():
    return getVariables().replace('.html', '')

def getVideo():
    match v.get():
        case 2: return "fortnite.mp4"
        case 3: return "harry.mp4"
        case 4: return "pokemon.mp4"
        case 5: return "minecraft.mp4"
        case _: return "movie.mp4"

def getCSS():
    color = getColor()
    video = getVideo()
    if color == "Blue" and video != "movie.mp4":
        return "Stylea.css"
    elif color == "Red" and video != "movie.mp4":
        return "Styleb.css"
    elif color == "Yellow" and video != "movie.mp4":
        return "Stylec.css"
    elif color == "Orange" and video != "movie.mp4":
        return "Styled.css"
    elif color == "Blue":
        return "Style.css"
    elif color == "Red":
        return "Style1.css"
    elif color == "Yellow":
        return "Style2.css"
    else:
        return "Style3.css"

def openWebpage():
    roomColor = getVariables()
    file_path = Path(__file__).parent / roomColor

    message = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>{happy.get()}</title>
  <link rel='stylesheet' href='{getCSS()}'>
</head>
<body>
  <img src='bg.png' alt='background'>
  <h1>{happy.get()}</h1>
  <video autoplay muted loop id='myVideo'>
    <source src="{getVideo()}" type='video/mp4'>Video not found
  </video>
  <div class='innertext'>{e.get()}</div>
</body>
</html>"""

    file_path.write_text(message, encoding="utf-8")
    webbrowser.open_new_tab(file_path.as_uri())

# ---- Layout controls ----
Radiobutton(root, text="Blue",   variable=room, value=1).pack(side="left")
Radiobutton(root, text="Red",    variable=room, value=2).pack(side="left")
Radiobutton(root, text="Yellow", variable=room, value=3).pack(side="left")
Radiobutton(root, text="Orange", variable=room, value=4).pack(side="left")

Radiobutton(root, text="Fireworks",   variable=v, value=1).pack(side="right")
Radiobutton(root, text="Fortnite",    variable=v, value=2).pack(side="right")
Radiobutton(root, text="Harry Potter",variable=v, value=3).pack(side="right")
Radiobutton(root, text="Pokemon",     variable=v, value=4).pack(side="bottom")
Radiobutton(root, text="Minecraft",   variable=v, value=5).pack(side="bottom")

myButton = Button(root, text="Make A Party", command=openWebpage)
myButton.pack(side=TOP, pady=10)

# ---- Add LTE logo in bottom-right corner ----
try:
    logo = PhotoImage(file="lte.jpg")  # Tkinter supports PNG/GIF best
except:
    from PIL import Image, ImageTk
    logo_img = Image.open("lte.gif")
    logo = ImageTk.PhotoImage(logo_img.resize((170, 40)))

logo_label = Label(root, image=logo)
logo_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)  # bottom-right corner

root.mainloop()
