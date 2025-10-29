from tkinter import *
from tkinter import ttk, filedialog, messagebox, colorchooser
from pathlib import Path
import webbrowser
import configparser
import sys
from typing import Optional, Tuple

# -----------------------------
# Utility logic (CSS/video/color)
# -----------------------------
VIDEO_OPTIONS = {
    1: ("movie.mp4",   "Fireworks"),
    2: ("fortnite.mp4","Fortnite"),
    3: ("harry.mp4",   "Harry Potter"),
    4: ("pokemon.mp4", "Pokemon"),
    5: ("minecraft.mp4","Minecraft"),
}
COLORS = ["Blue", "Red", "Yellow", "Orange"]

# Responsive font size presets -> (min_px, vw, max_px)
HEADLINE_SIZES = {
    "Small":  (32, 5.5, 96),
    "Medium": (42, 7.0, 120),
    "Large":  (54, 8.0, 150),
    "XL":     (64, 9.0, 180),
}

# Fancy inner-text fonts: display -> (CSS family string, Google Fonts family or None)
FANCY_FONTS = {
    "Same as Title": (None, None),
    "Pacifico": ("'Pacifico', cursive", "Pacifico"),
    "Lobster": ("'Lobster', cursive", "Lobster"),
    "Great Vibes": ("'Great Vibes', cursive", "Great+Vibes"),
    "Dancing Script": ("'Dancing Script', cursive", "Dancing+Script:wght@700"),
    "Cinzel Decorative": ("'Cinzel Decorative', cursive", "Cinzel+Decorative:wght@700"),
    "Playfair Black": ("'Playfair Display', serif", "Playfair+Display:ital,wght@0,900;1,900"),
    "Bangers": ("'Bangers', cursive", "Bangers"),
    "Brush Script (local only)": ("'Brush Script MT', 'Brush Script Std', cursive", None),
}

# 9-point position presets for inner text
INNER_POS_PRESETS = [
    "Top Left","Top Center","Top Right",
    "Center Left","Center","Center Right",
    "Bottom Left","Bottom Center","Bottom Right"
]
POS_TO_PCT = {
    "Top Left": (10, 12), "Top Center": (50, 12), "Top Right": (90, 12),
    "Center Left": (10, 50), "Center": (50, 50), "Center Right": (90, 50),
    "Bottom Left": (10, 88), "Bottom Center": (50, 88), "Bottom Right": (90, 88),
}

def get_css(color: str, video_filename: str) -> str:
    if color == "Blue" and video_filename != "movie.mp4":
        return "Stylea.css"
    elif color == "Red" and video_filename != "movie.mp4":
        return "Styleb.css"
    elif color == "Yellow" and video_filename != "movie.mp4":
        return "Stylec.css"
    elif color == "Orange" and video_filename != "movie.mp4":
        return "Styled.css"
    if color == "Blue":
        return "Style.css"
    elif color == "Red":
        return "Style1.css"
    elif color == "Yellow":
        return "Style2.css"
    else:
        return "Style3.css"

def looks_like_url(path_str: str) -> bool:
    s = (path_str or "").lower().strip()
    return s.startswith("http://") or s.startswith("https://")

def hex_to_rgb_tuple(hex_color: str) -> Tuple[int,int,int]:
    hc = hex_color.strip().lstrip('#')
    if len(hc) == 3:
        hc = ''.join([c*2 for c in hc])
    try:
        r = int(hc[0:2], 16)
        g = int(hc[2:4], 16)
        b = int(hc[4:6], 16)
        return (r,g,b)
    except Exception:
        return (255,255,255)

def rgba_str(hex_color: str, a: float) -> str:
    r,g,b = hex_to_rgb_tuple(hex_color)
    return f"rgba({r},{g},{b},{a})"

# ---------- Font includes / resolution ----------
def resolve_inner_font(font_choice: str, local_font_path: str) -> Tuple[str, Optional[str], Optional[str]]:
    google_link_tag = None
    local_face_css = None
    inner_font_family = None
    if local_font_path:
        ext = local_font_path.split(".")[-1].lower()
        if ext in ("ttf", "otf", "woff", "woff2"):
            inner_font_family = "CustomInner"
            local_face_css = f"""
@font-face {{
  font-family: 'CustomInner';
  src: url('{local_font_path}');
  font-display: swap;
}}
"""
            return inner_font_family, google_link_tag, local_face_css
    if font_choice in FANCY_FONTS:
        inner_font_family, google_family = FANCY_FONTS[font_choice]
        if google_family:
            google_link_tag = f"<link href='https://fonts.googleapis.com/css2?family={google_family}&display=swap' rel='stylesheet'>"
    return inner_font_family, google_link_tag, local_face_css

# --------- dynamic inline CSS (center alignment + per-room colors + fancy font + positioning) ----------
def make_inline_css(opts: dict, inner_font_family: Optional[str], local_face_css: Optional[str]) -> str:
    """Title uses title font; inner text uses fancy/selected font. Colors are per-room. Forces centered alignment for text; .innertext positioned via presets."""
    h_min, h_vw, h_max = HEADLINE_SIZES.get(opts.get("headline_size","Medium"), HEADLINE_SIZES["Medium"])

    title_font_stack = '"Anton", Impact, "Montserrat ExtraBold", sans-serif'
    inner_font_stack = inner_font_family or title_font_stack

    title_color = opts.get("title_color", "#FFFFFF") or "#FFFFFF"
    inner_color = opts.get("inner_color", "#FFFFFF") or "#FFFFFF"

    # Inner positioning
    pos_name = opts.get("inner_pos", "Center")
    x_pct, y_pct = POS_TO_PCT.get(pos_name, (50, 50))
    off_x = int(opts.get("inner_offset_x", 0))
    off_y = int(opts.get("inner_offset_y", 0))

    # transform to keep the label centered at the anchor point (except corners/edges adjust translate)
    # We'll always use translate(-50%,-50%) for consistency (works well visually).
    translate_css = "translate(-50%,-50%)"

    parts = []
    if local_face_css:
        parts.append(local_face_css)

    parts.append(f"""
/* Base layout + force center alignment */
html, body {{
  margin: 0; padding: 0; overflow: hidden; background: #000;
}}
body {{ text-align: center; }}

#myVideo {{ width: 100%; height: auto; display: block; }}

h1 {{
  font-family: {title_font_stack};
  font-weight: 800; text-transform: uppercase; letter-spacing: 1px;
  font-size: clamp({h_min}px, {h_vw}vw, {h_max}px);
  color: {title_color};
  text-align: center;
  margin: .25em 0 .15em;
}}

/* Positioned inner text */
.innertext {{
  position: fixed;
  left: calc({x_pct}% + {off_x}px);
  top: calc({y_pct}% + {off_y}px);
  transform: {translate_css};
  font-family: {inner_font_stack};
  font-weight: 800; text-transform: uppercase; letter-spacing: 1px;
  font-size: clamp({h_min}px, {h_vw}vw, {h_max}px);
  color: {inner_color};
  text-align: center;
  display: inline-block;
  margin: 0;
  z-index: 3;
}}
""")

    if opts.get("headline_outline"):
        parts.append("""
h1, .innertext { -webkit-text-stroke: 3px #000;
  text-shadow: 2px 2px 0 #000, -2px 2px 0 #000,
               2px -2px 0 #000, -2px -2px 0 #000,
               0 6px 16px rgba(0,0,0,.6); }
""")

    if opts.get("readable_shadow"):
        parts.append("""
h1, .innertext { text-shadow: 0 2px 10px rgba(0,0,0,.75); }
""")

    if opts.get("neon_glow"):
        parts.append(f"""
h1 {{
  text-shadow:
    0 0 10px {rgba_str(title_color, .9)},
    0 0 20px {rgba_str(title_color, .7)},
    0 0 35px {rgba_str(title_color, .5)};
}}
.innertext {{
  text-shadow:
    0 0 10px {rgba_str(inner_color, .9)},
    0 0 20px {rgba_str(inner_color, .7)},
    0 0 35px {rgba_str(inner_color, .5)};
}}
""")

    if opts.get("pill_panel"):
        parts.append("""
.innertext {
  background: rgba(0,0,0,.55);
  padding: .35em .7em;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0,0,0,.35);
  -webkit-backdrop-filter: blur(2px);
  backdrop-filter: blur(2px);
}
""")

    if opts.get("overlay"):
        parts.append("""
.overlay {
  position: fixed; inset: 0; pointer-events: none; z-index: 1;
  background:
    linear-gradient(to bottom, rgba(0,0,0,.55), rgba(0,0,0,0) 40%),
    linear-gradient(to top,    rgba(0,0,0,.45), rgba(0,0,0,0) 45%);
}
body > * { position: relative; z-index: 2; }
""")

    if opts.get("dim_video"):
        parts.append("""
#myVideo { filter: brightness(.85) contrast(1.05) saturate(1.05); }
""")

    return "<style>\n" + "\n".join(parts) + "\n</style>"

def build_html(title_text: str, inner_text: str, css_file: str,
               bg_src: Optional[str], video_file: str,
               style_opts: dict, font_head_extra: str,
               inner_font_family: Optional[str],
               local_face_css: Optional[str]) -> str:
    overlay_div = "<div class='overlay'></div>\n" if style_opts.get("overlay") else ""
    bg_tag = f"  <img src='{bg_src}' alt='background'>\n" if bg_src else ""
    inline_css = make_inline_css(style_opts, inner_font_family, local_face_css)
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>{title_text}</title>
  <link rel='stylesheet' href='{css_file}'>
  {font_head_extra}
  {inline_css}
</head>
<body>
{overlay_div}{bg_tag}  <h1>{title_text}</h1>
  <video autoplay muted loop id='myVideo'>
    <source src="{video_file}" type='video/mp4'>Video not found
  </video>
  <div class='innertext'>{inner_text}</div>
</body>
</html>"""

# -----------------------------
# RoomFrame: one room's controls
# -----------------------------
class RoomFrame(ttk.LabelFrame):
    def __init__(self, master, room_index: int, **kwargs):
        super().__init__(master, text=f"Room {room_index}", padding=10, **kwargs)
        self.room_index = room_index

        # Enable checkbox
        self.enabled = BooleanVar(value=True)
        ttk.Checkbutton(self, text="Include this room", variable=self.enabled).grid(row=0, column=0, columnspan=12, sticky="w", pady=(0,6))

        # Title
        ttk.Label(self, text="Title:").grid(row=1, column=0, sticky="e")
        self.title_entry = ttk.Entry(self, width=28)
        self.title_entry.insert(END, "Happy Birthday")
        self.title_entry.grid(row=1, column=1, columnspan=11, sticky="we", padx=5, pady=2)

        # Inner text
        ttk.Label(self, text="Inner text (Name):").grid(row=2, column=0, sticky="e")
        self.inner_entry = ttk.Entry(self, width=28)
        self.inner_entry.grid(row=2, column=1, columnspan=11, sticky="we", padx=5, pady=2)

        # Color radios
        ttk.Label(self, text="Color:").grid(row=3, column=0, sticky="e")
        self.color = StringVar(value="Blue")
        col_frame = ttk.Frame(self); col_frame.grid(row=3, column=1, columnspan=11, sticky="w")
        for c in COLORS:
            ttk.Radiobutton(col_frame, text=c, value=c, variable=self.color).pack(side="left", padx=(0,6))

        # Video radios
        ttk.Label(self, text="Video:").grid(row=4, column=0, sticky="e")
        self.video_sel = IntVar(value=1)
        vid_frame = ttk.Frame(self); vid_frame.grid(row=4, column=1, columnspan=11, sticky="w")
        for val, (_, label) in VIDEO_OPTIONS.items():
            ttk.Radiobutton(vid_frame, text=label, value=val, variable=self.video_sel).pack(side="left", padx=(0,6))

        # Background image path
        ttk.Label(self, text="Background image:").grid(row=5, column=0, sticky="e")
        self.bg_var = StringVar(value="")
        ttk.Entry(self, textvariable=self.bg_var, width=40).grid(row=5, column=1, columnspan=10, sticky="we", padx=5, pady=2)
        ttk.Button(self, text="Browse…", command=self.browse_bg).grid(row=5, column=11, sticky="w")

        # Video override path
        ttk.Label(self, text="Video override:").grid(row=6, column=0, sticky="e")
        self.video_override_var = StringVar(value="")
        ttk.Entry(self, textvariable=self.video_override_var, width=40).grid(row=6, column=1, columnspan=10, sticky="we", padx=5, pady=2)
        ttk.Button(self, text="Browse…", command=self.browse_video).grid(row=6, column=11, sticky="w")

        # ---- Style toggles ----
        ttk.Label(self, text="Style:").grid(row=7, column=0, sticky="e")
        self.headline_outline = BooleanVar(value=True)
        self.neon_glow = BooleanVar(value=False)
        self.readable_shadow = BooleanVar(value=True)
        self.pill_panel = BooleanVar(value=False)
        self.overlay = BooleanVar(value=True)
        self.dim_video = BooleanVar(value=False)

        style_frame = ttk.Frame(self); style_frame.grid(row=7, column=1, columnspan=11, sticky="w")
        ttk.Checkbutton(style_frame, text="Headline Outline", variable=self.headline_outline).pack(side="left", padx=6)
        ttk.Checkbutton(style_frame, text="Neon Glow", variable=self.neon_glow).pack(side="left", padx=6)
        ttk.Checkbutton(style_frame, text="Readable Shadow", variable=self.readable_shadow).pack(side="left", padx=6)
        style_frame2 = ttk.Frame(self); style_frame2.grid(row=8, column=1, columnspan=11, sticky="w", pady=(2,6))
        ttk.Checkbutton(style_frame2, text="Pill Panel (inner text)", variable=self.pill_panel).pack(side="left", padx=6)
        ttk.Checkbutton(style_frame2, text="Top/Bottom Overlay", variable=self.overlay).pack(side="left", padx=6)
        ttk.Checkbutton(style_frame2, text="Dim Video", variable=self.dim_video).pack(side="left", padx=6)

        # Preset buttons
        preset_frame = ttk.Frame(self); preset_frame.grid(row=9, column=1, columnspan=11, sticky="w", pady=(0,6))
        ttk.Button(preset_frame, text="Preset: High Contrast", command=self.preset_high_contrast).pack(side="left", padx=4)
        ttk.Button(preset_frame, text="Preset: Neon", command=self.preset_neon).pack(side="left", padx=4)
        ttk.Button(preset_frame, text="Preset: Panel", command=self.preset_panel).pack(side="left", padx=4)

        # ---- Font size (title drives both) ----
        ttk.Label(self, text="Headline Size:").grid(row=10, column=0, sticky="e")
        self.headline_size = StringVar(value="Medium")
        self.headline_combo = ttk.Combobox(self, textvariable=self.headline_size, values=list(HEADLINE_SIZES.keys()), state="readonly", width=10)
        self.headline_combo.grid(row=10, column=1, sticky="w", padx=5, pady=(0,6))

        # ---- Fancy font for inner text ----
        ttk.Label(self, text="Inner Text Font:").grid(row=10, column=2, sticky="e")
        self.inner_font_choice = StringVar(value="Pacifico")
        self.inner_font_combo = ttk.Combobox(self, textvariable=self.inner_font_choice, values=list(FANCY_FONTS.keys()), state="readonly", width=22)
        self.inner_font_combo.grid(row=10, column=3, sticky="w", padx=5, pady=(0,6))

        ttk.Label(self, text="Local font (optional):").grid(row=11, column=0, sticky="e")
        self.inner_font_local = StringVar(value="")
        ttk.Entry(self, textvariable=self.inner_font_local, width=40).grid(row=11, column=1, columnspan=10, sticky="we", padx=5, pady=2)
        ttk.Button(self, text="Browse…", command=self.browse_local_font).grid(row=11, column=11, sticky="w")

        # ---- Title / Inner colors + link toggle + swatches ----
        ttk.Label(self, text="Title Color:").grid(row=12, column=0, sticky="e")
        self.title_color = StringVar(value="#FFFFFF")
        # tk.Button so we can set bg/fg (ttk.Button can't)
        self.title_color_btn = Button(self, text=self.title_color.get(), command=self.pick_title_color, width=12)
        self.title_color_btn.grid(row=12, column=1, sticky="w", padx=5, pady=(2,6))

        ttk.Label(self, text="Inner Color:").grid(row=12, column=2, sticky="e")
        self.inner_color = StringVar(value="#FFFFFF")
        self.inner_color_btn = Button(self, text=self.inner_color.get(), command=self.pick_inner_color, width=12)
        self.inner_color_btn.grid(row=12, column=3, sticky="w", padx=5, pady=(2,6))

        self.link_colors = BooleanVar(value=True)
        ttk.Checkbutton(self, text="Same color for Title & Inner", variable=self.link_colors,
                        command=self._refresh_color_buttons).grid(row=12, column=4, sticky="w", padx=8)

        # ---- Inner text position controls ----
        ttk.Label(self, text="Inner Position:").grid(row=13, column=0, sticky="e")
        self.inner_pos = StringVar(value="Center")
        self.inner_pos_combo = ttk.Combobox(self, textvariable=self.inner_pos, values=INNER_POS_PRESETS,
                                            state="readonly", width=16)
        self.inner_pos_combo.grid(row=13, column=1, sticky="w", padx=5, pady=(2,6))

        ttk.Label(self, text="Offset X (px):").grid(row=13, column=2, sticky="e")
        self.inner_off_x = StringVar(value="0")
        ttk.Entry(self, textvariable=self.inner_off_x, width=8).grid(row=13, column=3, sticky="w", padx=5)

        ttk.Label(self, text="Offset Y (px):").grid(row=13, column=4, sticky="e")
        self.inner_off_y = StringVar(value="0")
        ttk.Entry(self, textvariable=self.inner_off_y, width=8).grid(row=13, column=5, sticky="w", padx=5)

        # Expand grid
        for i in range(12):
            self.columnconfigure(i, weight=1)

        # Initial UI sync
        self._refresh_color_buttons()

    # ---- presets
    def preset_high_contrast(self):
        self.headline_outline.set(True); self.readable_shadow.set(True)
        self.neon_glow.set(False); self.pill_panel.set(False)
        self.overlay.set(True); self.dim_video.set(True)
        self.inner_color.set("#FFFFFF")
        if self.link_colors.get(): self.title_color.set("#FFFFFF")
        self._refresh_color_buttons()

    def preset_neon(self):
        self.headline_outline.set(False); self.readable_shadow.set(True)
        self.neon_glow.set(True); self.pill_panel.set(False)
        self.overlay.set(True); self.dim_video.set(True)
        self.inner_color.set("#7FFF00")
        if self.link_colors.get(): self.title_color.set("#7FFF00")
        self._refresh_color_buttons()

    def preset_panel(self):
        self.headline_outline.set(False); self.readable_shadow.set(True)
        self.neon_glow.set(False); self.pill_panel.set(True)
        self.overlay.set(True); self.dim_video.set(False)
        self.inner_color.set("#FFFFFF")
        if self.link_colors.get(): self.title_color.set("#FFFFFF")
        self._refresh_color_buttons()

    # ---- file pickers
    def browse_bg(self):
        path = filedialog.askopenfilename(
            title="Choose background image",
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif;*.webp"), ("All files", "*.*")]
        )
        if path:
            self.bg_var.set(path)

    def browse_video(self):
        path = filedialog.askopenfilename(
            title="Choose video file",
            filetypes=[("MP4 Video", "*.mp4"), ("All files", "*.*")]
        )
        if path:
            self.video_override_var.set(path)

    def browse_local_font(self):
        path = filedialog.askopenfilename(
            title="Choose font file (.ttf/.otf/.woff/.woff2)",
            filetypes=[("Font files", "*.ttf;*.otf;*.woff;*.woff2"), ("All files", "*.*")]
        )
        if path:
            self.inner_font_local.set(path)

    # ---- color pickers
    def pick_title_color(self):
        if self.link_colors.get():
            return self.pick_inner_color()
        initial = self.title_color.get() or "#FFFFFF"
        color_tuple = colorchooser.askcolor(color=initial, title="Pick Title Color")
        if color_tuple and color_tuple[1]:
            self.title_color.set(color_tuple[1].upper())
            self._refresh_color_buttons()

    def pick_inner_color(self):
        initial = self.inner_color.get() or "#FFFFFF"
        color_tuple = colorchooser.askcolor(color=initial, title="Pick Inner (Name) Color")
        if color_tuple and color_tuple[1]:
            hexval = color_tuple[1].upper()
            self.inner_color.set(hexval)
            if self.link_colors.get():
                self.title_color.set(hexval)
            self._refresh_color_buttons()

    def _apply_btn_color(self, btn: Button, hexval: str):
        # Choose foreground for legibility
        r,g,b = hex_to_rgb_tuple(hexval)
        brightness = (r*299 + g*587 + b*114) / 1000
        fg = "#000000" if brightness > 155 else "#FFFFFF"
        btn.config(text=hexval, bg=hexval, activebackground=hexval, fg=fg, activeforeground=fg)

    def _refresh_color_buttons(self):
        if self.link_colors.get():
            self.title_color.set(self.inner_color.get())
            self.title_color_btn.config(state="disabled")
        else:
            self.title_color_btn.config(state="normal")
        # update swatches & text
        self._apply_btn_color(self.inner_color_btn, self.inner_color.get())
        self._apply_btn_color(self.title_color_btn, self.title_color.get())

    # ---- state IO
    def get_state(self):
        return {
            "enabled": str(self.enabled.get()),
            "title": self.title_entry.get(),
            "inner": self.inner_entry.get(),
            "color": self.color.get(),
            "video": str(self.video_sel.get()),
            "bg": self.bg_var.get(),
            "video_override": self.video_override_var.get(),
            "headline_outline": str(self.headline_outline.get()),
            "neon_glow": str(self.neon_glow.get()),
            "readable_shadow": str(self.readable_shadow.get()),
            "pill_panel": str(self.pill_panel.get()),
            "overlay": str(self.overlay.get()),
            "dim_video": str(self.dim_video.get()),
            "headline_size": self.headline_size.get(),
            "inner_font_choice": self.inner_font_choice.get(),
            "inner_font_local": self.inner_font_local.get(),
            "title_color": self.title_color.get(),
            "inner_color": self.inner_color.get(),
            "link_colors": str(self.link_colors.get()),
            "inner_pos": self.inner_pos.get(),
            "inner_offset_x": self.inner_off_x.get(),
            "inner_offset_y": self.inner_off_y.get(),
        }

    def set_state(self, state: dict):
        try:
            if "enabled" in state: self.enabled.set(str(state["enabled"]).lower() == "true")
            if "title" in state: self.title_entry.delete(0, END); self.title_entry.insert(0, state["title"])
            if "inner" in state: self.inner_entry.delete(0, END); self.inner_entry.insert(0, state["inner"])
            if "color" in state and state["color"] in COLORS: self.color.set(state["color"])
            if "video" in state:
                v = int(state["video"])
                if v in VIDEO_OPTIONS: self.video_sel.set(v)
            if "bg" in state: self.bg_var.set(state["bg"])
            if "video_override" in state: self.video_override_var.set(state["video_override"])
            for k in ("headline_outline","neon_glow","readable_shadow","pill_panel","overlay","dim_video"):
                if k in state: getattr(self, k).set(str(state[k]).lower()=="true")
            if "headline_size" in state and state["headline_size"] in HEADLINE_SIZES:
                self.headline_size.set(state["headline_size"])
            if "inner_font_choice" in state and state["inner_font_choice"] in FANCY_FONTS:
                self.inner_font_choice.set(state["inner_font_choice"])
            if "inner_font_local" in state:
                self.inner_font_local.set(state["inner_font_local"])
            if "title_color" in state and state["title_color"]:
                self.title_color.set(state["title_color"])
            if "inner_color" in state and state["inner_color"]:
                self.inner_color.set(state["inner_color"])
            if "link_colors" in state:
                self.link_colors.set(str(state["link_colors"]).lower()=="true")
            if "inner_pos" in state and state["inner_pos"] in INNER_POS_PRESETS:
                self.inner_pos.set(state["inner_pos"])
            if "inner_offset_x" in state:
                self.inner_off_x.set(state["inner_offset_x"])
            if "inner_offset_y" in state:
                self.inner_off_y.set(state["inner_offset_y"])
            self._refresh_color_buttons()
        except Exception:
            pass  # keep defaults

    def build_and_write(self, out_dir: Path, filename: str) -> Optional[Path]:
        if not self.enabled.get():
            return None

        title = (self.title_entry.get() or "Happy Birthday").strip()
        inner = self.inner_entry.get().strip()

        # Resolve video
        video_override = self.video_override_var.get().strip()
        video_file: Optional[str] = None
        if video_override:
            if looks_like_url(video_override):
                video_file = video_override
            else:
                vp = Path(video_override)
                if vp.exists() or (out_dir / video_override).exists():
                    video_file = video_override
        if not video_file:
            video_file = VIDEO_OPTIONS.get(self.video_sel.get(), ("movie.mp4", ""))[0]

        css_file = get_css(self.color.get(), Path(video_file).name if not looks_like_url(video_file) else video_file)

        # Background image (optional)
        bg_input = self.bg_var.get().strip()
        bg_src: Optional[str] = None
        if bg_input:
            if looks_like_url(bg_input):
                bg_src = bg_input
            else:
                bp = Path(bg_input)
                if bp.exists() or (out_dir / bg_input).exists():
                    bg_src = bg_input

        # Fancy font for inner name
        font_choice = self.inner_font_choice.get()
        local_font = self.inner_font_local.get()
        inner_font_family, google_link_tag, local_face_css = resolve_inner_font(font_choice, local_font)
        font_head_extra = google_link_tag or ""

        # Style + colors (link enforced)
        title_color = self.title_color.get()
        inner_color = self.inner_color.get()
        if self.link_colors.get():
            title_color = inner_color

        # parse offsets safely
        try:
            offx = int(self.inner_off_x.get())
        except Exception:
            offx = 0
        try:
            offy = int(self.inner_off_y.get())
        except Exception:
            offy = 0

        style_opts = {
            "headline_outline": self.headline_outline.get(),
            "neon_glow": self.neon_glow.get(),
            "readable_shadow": self.readable_shadow.get(),
            "pill_panel": self.pill_panel.get(),
            "overlay": self.overlay.get(),
            "dim_video": self.dim_video.get(),
            "headline_size": self.headline_size.get(),
            "title_color": title_color,
            "inner_color": inner_color,
            "inner_pos": self.inner_pos.get(),
            "inner_offset_x": offx,
            "inner_offset_y": offy,
        }

        html = build_html(title, inner, css_file, bg_src, video_file,
                          style_opts, font_head_extra, inner_font_family, local_face_css)
        out_dir.mkdir(parents=True, exist_ok=True)
        file_path = out_dir / filename
        file_path.write_text(html, encoding="utf-8")
        return file_path

# -----------------------------
# Main App with config.ini + open buttons
# -----------------------------
class PartyRoomBuilder(Tk):
    def __init__(self):
        super().__init__()
        self.title("🎉 Party Room Pages Builder (3 Rooms) 🎉")
        self.geometry("1100x860")

        # Config paths
        self.app_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).parent)).resolve()
        self.config_path = self.app_dir / "config.ini"
        self.config = configparser.ConfigParser()

        # Output folder selector
        path_frame = ttk.LabelFrame(self, text="Output Folder", padding=10)
        path_frame.pack(fill="x", padx=10, pady=10)

        self.output_var = StringVar()
        default_dir = str(Path(__file__).parent.resolve())
        self.output_var.set(default_dir)

        ttk.Label(path_frame, text="Folder:").grid(row=0, column=0, sticky="e")
        ttk.Entry(path_frame, textvariable=self.output_var).grid(row=0, column=1, sticky="we", padx=6)
        ttk.Button(path_frame, text="Browse…", command=self.choose_folder).grid(row=0, column=2, padx=4)
        path_frame.columnconfigure(1, weight=1)

        # Rooms
        rooms_frame = ttk.Frame(self)
        rooms_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))
        self.room1 = RoomFrame(rooms_frame, 1)
        self.room2 = RoomFrame(rooms_frame, 2)
        self.room3 = RoomFrame(rooms_frame, 3)
        self.room1.grid(row=0, column=0, sticky="nsew", padx=(0,6))
        self.room2.grid(row=0, column=1, sticky="nsew", padx=6)
        self.room3.grid(row=0, column=2, sticky="nsew", padx=(6,0))
        for i in range(3):
            rooms_frame.columnconfigure(i, weight=1)

        # Buttons (build + open 1/2/3 + save)
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=(0,12))

        ttk.Button(btn_frame, text="Create Selected Rooms", command=self.create_files).pack(side="left")
        ttk.Separator(btn_frame, orient="vertical").pack(side="left", fill="y", padx=8)
        ttk.Button(btn_frame, text="Open Room 1", command=lambda: self.open_specific_out(1)).pack(side="left")
        ttk.Button(btn_frame, text="Open Room 2", command=lambda: self.open_specific_out(2)).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Open Room 3", command=lambda: self.open_specific_out(3)).pack(side="left")
        ttk.Button(btn_frame, text="Save Settings Now", command=self.save_config).pack(side="right")

        self.created_paths: dict[int, Path] = {}

        ttk.Label(
            self,
            text="Tip: Use 'Inner Position' + offsets to place the name anywhere. Color buttons show live hex + swatch.",
            foreground="#444"
        ).pack(padx=10, pady=(0,10), anchor="w")

        self.load_config()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---- Config handling ----
    def load_config(self):
        if not self.config_path.exists():
            return
        try:
            self.config.read(self.config_path, encoding="utf-8")
            general = self.config.get("general", "output_dir", fallback="")
            if general:
                self.output_var.set(general)
            for idx, room in enumerate((self.room1, self.room2, self.room3), start=1):
                sect = f"room{idx}"
                if self.config.has_section(sect):
                    state = {
                        "enabled": self.config.get(sect, "enabled", fallback="True"),
                        "title": self.config.get(sect, "title", fallback="Happy Birthday"),
                        "inner": self.config.get(sect, "inner", fallback=""),
                        "color": self.config.get(sect, "color", fallback="Blue"),
                        "video": self.config.get(sect, "video", fallback="1"),
                        "bg": self.config.get(sect, "bg", fallback=""),
                        "video_override": self.config.get(sect, "video_override", fallback=""),
                        "headline_outline": self.config.get(sect, "headline_outline", fallback="True"),
                        "neon_glow": self.config.get(sect, "neon_glow", fallback="False"),
                        "readable_shadow": self.config.get(sect, "readable_shadow", fallback="True"),
                        "pill_panel": self.config.get(sect, "pill_panel", fallback="False"),
                        "overlay": self.config.get(sect, "overlay", fallback="True"),
                        "dim_video": self.config.get(sect, "dim_video", fallback="False"),
                        "headline_size": self.config.get(sect, "headline_size", fallback="Medium"),
                        "inner_font_choice": self.config.get(sect, "inner_font_choice", fallback="Pacifico"),
                        "inner_font_local": self.config.get(sect, "inner_font_local", fallback=""),
                        "title_color": self.config.get(sect, "title_color", fallback="#FFFFFF"),
                        "inner_color": self.config.get(sect, "inner_color", fallback="#FFFFFF"),
                        "link_colors": self.config.get(sect, "link_colors", fallback="True"),
                        "inner_pos": self.config.get(sect, "inner_pos", fallback="Center"),
                        "inner_offset_x": self.config.get(sect, "inner_offset_x", fallback="0"),
                        "inner_offset_y": self.config.get(sect, "inner_offset_y", fallback="0"),
                    }
                    for k in ("enabled","headline_outline","neon_glow","readable_shadow","pill_panel","overlay","dim_video"):
                        state[k] = "True" if str(state[k]).lower()=="true" else "False"
                    if state["headline_size"] not in HEADLINE_SIZES: state["headline_size"] = "Medium"
                    if state["inner_font_choice"] not in FANCY_FONTS: state["inner_font_choice"] = "Pacifico"
                    if state["inner_pos"] not in INNER_POS_PRESETS: state["inner_pos"] = "Center"
                    room.set_state(state)
        except Exception as e:
            messagebox.showwarning("Config", f"Could not load config.ini:\n{e}")

    def save_config(self):
        try:
            if not self.config.has_section("general"):
                self.config.add_section("general")
            self.config.set("general", "output_dir", self.output_var.get().strip())

            for idx, room in enumerate((self.room1, self.room2, self.room3), start=1):
                sect = f"room{idx}"
                if not self.config.has_section(sect):
                    self.config.add_section(sect)
                state = room.get_state()
                for k, v in state.items():
                    self.config.set(sect, k, v)

            with (self.config_path).open("w", encoding="utf-8") as f:
                self.config.write(f)
        except Exception as e:
            messagebox.showerror("Config", f"Could not save config.ini:\n{e}")

    # ---- App behaviors ----
    def choose_folder(self):
        folder = filedialog.askdirectory(title="Choose output folder")
        if folder:
            self.output_var.set(folder)

    def create_files(self):
        out_dir = Path(self.output_var.get().strip()) if self.output_var.get().strip() else Path(__file__).parent
        self.created_paths.clear()

        mapping = [
            (self.room1, 1, "partyroom1.html"),
            (self.room2, 2, "partyroom2.html"),
            (self.room3, 3, "partyroom3.html"),
        ]
        for room_frame, idx, filename in mapping:
            file_path = room_frame.build_and_write(out_dir, filename)
            if file_path:
                self.created_paths[idx] = file_path

        self.save_config()

        if self.created_paths:
            msg = "Created:\n" + "\n".join(f"Room {i}: {p}" for i, p in self.created_paths.items())
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showwarning("No Rooms Selected", "No rooms were selected to create. Please check at least one room.")

    def open_specific_out(self, room_idx: int):
        out_dir = Path(self.output_var.get().strip()) if self.output_var.get().strip() else Path(__file__).parent
        expected = out_dir / f"partyroom{room_idx}.html"
        if expected.exists():
            webbrowser.open_new_tab(expected.as_uri())
        else:
            messagebox.showinfo("Not Found", f"partyroom{room_idx}.html was not found in:\n{out_dir}\n\nCreate files first.")

    def on_close(self):
        self.save_config()
        self.destroy()

if __name__ == "__main__":
    app = PartyRoomBuilder()
    app.mainloop()
