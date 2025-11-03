LaserTagBirthdayNames / Party Room Pages Builder

A simple desktop tool (Tkinter) that generates three Party Room HTML pages for your venue. Each page can display a video background, a big “Happy Birthday” title, a customizable guest name, and your LTE logo during playback—plus an end overlay that shows the logo and “Party Room N”.

Features

Generate three room pages: partyroom1.html, partyroom2.html, partyroom3.html

Per-room enable/disable toggle

Title (e.g., “Happy Birthday”) + Guest name field

Theme color selector (Blue/Red/Yellow/Orange → auto-CSS)

Media & Branding

Video background (default or per-room override; local file or URL)

Optional background image

Persistent bottom-right logo during playback

End overlay with centered logo + “Party Room N”

Typography & Layout

Responsive, clamp-based headline sizing (Small / Medium / Large / XL)

Fancy Guest fonts (Google Fonts presets + local font file support)

9-point position presets (Top/Center/Bottom × Left/Center/Right)

Pixel offset controls (X/Y)

Linked/unlinked Title & Inner color pickers

Readability Controls

Headline Outline (stroke + multi-shadow)

Readable Shadow (soft contrast glow)

Neon Glow

Pill Panel behind guest name

Top/Bottom Overlay gradients

Dim Video filter

Reliability & File Handling

Inline data-URI for local logo (bullet-proof rendering)

Tries inline data-URI for background image (fallback to file:///)

Local video paths auto-converted to file:///

Safe handling of HTTP(S) asset URLs

Controls & Automation

Auto-stop timer (minutes) → pause/reset video + show end overlay

Presets: High Contrast / Neon / Panel

Quick Open Room X buttons

Configuration

config.ini load/save of all UI state

Versioned config.example.ini; real config.ini in .gitignore

UI/UX

Clean Tkinter layout with per-room Advanced panel

Color buttons show actual hex with readable text

Clear success/warning dialogs

Dev & Packaging

Python 3.9+ with Tkinter

PyInstaller-friendly (one-file EXE)

Clean git workflow (feature branches, tags)

(Optional) Checklist version

 Generate partyroom1/2/3.html

 Per-room enable/disable

 Video override + background image

 Bottom-right logo + end overlay “Party Room N”

 Fancy guest fonts (Google/local)

 Position presets + offsets

 Readability (Outline, Shadow, Neon, Panel, Overlays, Dim)

 Auto-stop timer

 Inline logo (data-URI), robust asset paths

 config.ini state + config.example.ini

 PyInstaller build
