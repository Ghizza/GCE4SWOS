import os
import shutil
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox, ttk

MONOSPACE_FONTS = ("Consolas", "Cascadia Mono", "DejaVu Sans Mono",
                   "Liberation Mono", "Lucida Console")
FONT_SIZE = 10
SKILL_GAP = 9

# ============================================================================
# COLOR SCHEME
# ============================================================================

# --- General -----------------------------------------------------------------
APP_BG = "#CECACD"            # window, panels, boxes and the area behind the tabs
APP_FG = "#575279"            # normal text (labels, file name, team name...)
APP_FG_MUTED = "#797593"      # secondary text (hint line under the players table)
APP_FG_DISABLED = "#9893A5"   # text of disabled widgets

# --- Borders and 3D edges ----------------------------------------------------
BORDER = "#9893A5"            # outline of boxes, menus, table, scrollbar
EDGE_LIGHT = "#F4EDE8"        # light edge of raised parts (top/left bevel)
EDGE_DARK = "#DFDAD9"         # dark edge of raised parts (bottom/right bevel)

# --- Fields: dropdown menus, dropdown lists, table body -----------------------
FIELD_BG = "#F4EDE8"          # background: lighter than APP_BG, so fields stand out
FIELD_FG = "#575279"          # text
FIELD_BG_DISABLED = "#DFDAD9" # background of menus while no player is selected

# --- Selection: highlighted table row AND highlighted item in the dropdown lists
SELECT_BG = "#907AA9"
SELECT_FG = "#F4EDE8"

# --- Tabs (Club / Players) ---------------------------------------------------
TAB_ACTIVE_BG = "#B4637A"     # selected tab
TAB_ACTIVE_FG = "#F4EDE8"
TAB_IDLE_BG = "#DFDAD9"       # not selected tab
TAB_IDLE_FG = "#575279"
TAB_HOVER_BG = "#9893A5"      # not selected tab under the mouse

# --- Buttons -----------------------------------------------------------------
BUTTON_BG = "#286983"
BUTTON_FG = "#F4EDE8"
BUTTON_HOVER_BG = "#56949F"   # mouse over
BUTTON_PRESS_BG = "#575279"   # while clicking
BUTTON_BORDER = "#575279"
BUTTON_DISABLED_BG = "#DFDAD9"
BUTTON_DISABLED_FG = "#9893A5"
BUTTON_DISABLED_BORDER = "#CECACD"

# --- Players table header (#, N., Player, Country...) -------------------------
HEADING_BG = "#DFDAD9"
HEADING_FG = "#575279"
HEADING_HOVER_BG = "#CECACD"  # header under the mouse

# --- Dropdown menus: arrow button on the right -------------------------------
ARROW_BG = "#DFDAD9"
ARROW_BG_HOVER = "#CECACD"
ARROW_FG = "#575279"          # the little triangle

# --- Scrollbar of the players table ------------------------------------------
SCROLL_TROUGH = "#DFDAD9"     # the groove
SCROLL_THUMB = "#CECACD"      # the slider
SCROLL_THUMB_HOVER = "#9893A5"
SCROLL_ARROW = "#575279"      # the small arrows at the ends

# --- Kit preview (Club tab) --------------------------------------------------
PREVIEW_BG = "#F4EDE8"        # background of the preview box (matches the fields)
PREVIEW_BORDER = "#9893A5"    # frame of the preview box
PREVIEW_OUTLINE = "#575279"   # thin outline of shirt, shorts and socks

KIT_OFFSET = 0xDB9A
KIT_SIZE = 10
TEAM_NAME_OFFSET = KIT_OFFSET - 21
TEAM_NAME_LEN = 19

BALANCE_OFFSET = 0xD5DC
BALANCE_SIZE = 4
BALANCE_TARGET = 100_000_000

TRANSFER_COUNTERS = (
    (0xD876, "Season total:"),
    (0xD878, "Backup total:"),
    (0xD880, "Buys:"),
    (0xD882, "Sales:"),
)

STYLES = {
    0: "Plain",
    1: "Colored sleeves",
    2: "Vertical strips",
    3: "Horizontal strips",
}

COLORS = {
    0: ("Grey", "#B6B6B6"),
    1: ("White", "#FFFFFF"),
    2: ("Black", "#000000"),
    3: ("Orange", "#FF6D00"),
    4: ("Red", "#FF0000"),
    5: ("Blue", "#0000FF"),
    6: ("Maroon", "#6D0024"),
    7: ("Light blue", "#9292FF"),
    8: ("Green", "#00DF00"),
    9: ("Yellow", "#FFFF00"),
}

KIT_FIELDS = ["Style", "Primary color", "Secondary color", "Shorts", "Socks"]

PLAYERS_START = 0xDBCC
PLAYER_SIZE = 38
MAX_PLAYERS = 40

NATION_OFF = 0
NUMBER_OFF = 2
NAME_OFF = 3
NAME_FIELD_LEN = 23
ROLE_OFF = 26
HEALTH_OFF = 27
SKILLS_OFF = 28
VALUE_OFF = 32

SQUAD_COUNT_OFFSET = 0xE08C
SQUAD_LIST_OFFSET = 0xDB60
SQUAD_LIST_SIZE = 32

ROLE_MASK = 0xE0
SKIN_MASK = 0x18
HEALTH_MASK = 0xE0
DISCIPLINE_MASK = 0x1F
DISCIPLINE = {
    0: "Clean",
    1: "1 match ban",
    2: "2 matches ban",
    3: "3 matches ban",
    4: "Yellow card",
}

POSITIONS = {
    0: "G",
    1: "RB",
    2: "LB",
    3: "D",
    4: "RW",
    5: "LW",
    6: "M",
    7: "A",
}

ROLE_ORDER = ("G", "RB", "D", "LB", "RW", "M", "LW", "A")
ROLE_RANK = {code: ROLE_ORDER.index(label) for code, label in POSITIONS.items()}

SKINS = {
    0x00: "Dark hair",
    0x08: "Blonde hair",
    0x10: "Black",
}

HEALTH = {
    0x00: "Fit",
    0x20: "[\\] Minor injury",
    0x40: "[1] 1 match out",
    0x60: "[2] 2 matches out",
    0x80: "[3] 3 matches out",
    0xA0: "[4] 4 matches out",
    0xC0: "[?] Severe injury",
    0xE0: "[+] Season over",
}

SKILL_NAMES = ["PA", "VE", "HE", "TA", "CO", "SP", "FI"]

VALUES = [
    "£25K-", "£25K", "£30K", "£40K", "£50K", "£65K", "£75K", "£85K",
    "£100K", "£110K", "£130K", "£150K", "£160K", "£180K", "£200K", "£250K",
    "£300K", "£350K", "£450K", "£500K", "£550K", "£600K", "£650K", "£700K",
    "£750K", "£800K", "£850K", "£950K", "£1M", "£1.1M", "£1.3M", "£1.5M",
    "£1.6M", "£1.8M", "£1.9M", "£2M", "£2.25M", "£2.75M", "£3M", "£3.5M",
    "£4.5M", "£5M", "£6M", "£7M", "£8M", "£9M", "£10M", "£12M",
    "£15M", "£15M+",
]

NATIONS_TABLE = [
    (0x00, "ALB", "Albania"), (0x01, "AUT", "Austria"), (0x02, "BEL", "Belgium"),
    (0x03, "BUL", "Bulgaria"), (0x04, "CRO", "Croatia"), (0x05, "CYP", "Cyprus"),
    (0x06, "TCH", "Czech Republic"), (0x07, "DEN", "Denmark"), (0x08, "ENG", "England"),
    (0x09, "EST", "Estonia"), (0x0a, "FAR", "Faroe Islands"), (0x0b, "FIN", "Finland"),
    (0x0c, "FRA", "France"), (0x0d, "GER", "Germany"), (0x0e, "GRE", "Greece"),
    (0x0f, "HUN", "Hungary"), (0x10, "ISL", "Iceland"), (0x11, "ISR", "Israel"),
    (0x12, "ITA", "Italy"), (0x13, "LAT", "Latvia"), (0x14, "LIT", "Lithuania"),
    (0x15, "LUX", "Luxembourg"), (0x16, "MLT", "Malta"), (0x17, "HOL", "Holland"),
    (0x18, "NIR", "Northern Ireland"), (0x19, "NOR", "Norway"), (0x1a, "POL", "Poland"),
    (0x1b, "POR", "Portugal"), (0x1c, "ROM", "Romania"), (0x1d, "RUS", "Russia"),
    (0x1e, "SMR", "San Marino"), (0x1f, "SCO", "Scotland"), (0x20, "SLO", "Slovenia"),
    (0x21, "SWE", "Sweden"), (0x22, "TUR", "Turkey"), (0x23, "UKR", "Ukraine"),
    (0x24, "WAL", "Wales"), (0x25, "YUG", "Yugoslavia"), (0x26, "BLS", "Belarus"),
    (0x27, "SVK", "Slovakia"), (0x28, "ESP", "Spain"), (0x29, "ARM", "Armenia"),
    (0x2a, "BOS", "Bosnia Herzegovina"), (0x2b, "AZB", "Azerbaijan"), (0x2c, "GEO", "Georgia"),
    (0x2d, "SWI", "Switzerland"), (0x2e, "IRL", "Rep. of Ireland"), (0x2f, "MAC", "FYR Macedonia"),
    (0x30, "TRK", "Turkmenistan"), (0x31, "LIE", "Liechtenstein"), (0x32, "MOL", "Moldova"),
    (0x33, "CRC", "Costa Rica"), (0x34, "SAL", "El Salvador"), (0x35, "GUA", "Guatemala"),
    (0x36, "HON", "Honduras / Hong Kong"), (0x37, "BHM", "Bahamas"), (0x38, "MEX", "Mexico"),
    (0x39, "PAN", "Panama"), (0x3a, "USA", "USA"), (0x3b, "BAH", "Bahrain"),
    (0x3c, "NIC", "Nicaragua"), (0x3d, "BER", "Bermuda"), (0x3e, "JAM", "Jamaica"),
    (0x3f, "TRI", "Trinidad Tobago"), (0x40, "CAN", "Canada"), (0x41, "BAR", "Barbados"),
    (0x42, "ELS", "El Salvador (alt.)"), (0x43, "SVC", "St. Vincent/Grenadines"), (0x44, "ARG", "Argentina"),
    (0x45, "BOL", "Bolivia"), (0x46, "BRA", "Brazil"), (0x47, "CHL", "Chile"),
    (0x48, "COL", "Colombia"), (0x49, "ECU", "Ecuador"), (0x4a, "PAR", "Paraguay"),
    (0x4b, "SUR", "Surinam"), (0x4c, "URU", "Uruguay"), (0x4d, "VEN", "Venezuela"),
    (0x4e, "GUY", "Guyana"), (0x4f, "PER", "Peru"), (0x50, "ALG", "Algeria"),
    (0x51, "SAF", "South Africa"), (0x52, "BOT", "Botswana"), (0x53, "BFS", "Burkina Faso"),
    (0x54, "BUR", "Burundi"), (0x55, "LES", "Lesotho"), (0x56, "ZAI", "DR Congo (Zaire)"),
    (0x57, "ZAM", "Zambia"), (0x58, "GHA", "Ghana"), (0x59, "SEN", "Senegal"),
    (0x5a, "CIV", "Ivory Coast"), (0x5b, "TUN", "Tunisia"), (0x5c, "MLI", "Mali"),
    (0x5d, "MDG", "Madagascar"), (0x5e, "CMR", "Cameroon"), (0x5f, "CHD", "Chad"),
    (0x60, "UGA", "Uganda"), (0x61, "LIB", "Liberia"), (0x62, "MOZ", "Mozambique"),
    (0x63, "KEN", "Kenya"), (0x64, "SUD", "Sudan"), (0x65, "SWA", "Swaziland"),
    (0x66, "ANG", "Angola"), (0x67, "TOG", "Togo"), (0x68, "ZIM", "Zimbabwe"),
    (0x69, "EGY", "Egypt"), (0x6a, "TAN", "Tanzania"), (0x6b, "NIG", "Nigeria / Niger"),
    (0x6c, "ETH", "Ethiopia"), (0x6d, "GAB", "Gabon"), (0x6e, "SIE", "Sierra Leone"),
    (0x6f, "BEN", "Benin"), (0x70, "CON", "Congo"), (0x71, "GUI", "Guinea"),
    (0x72, "SRL", "Sri Lanka (alt.)"), (0x73, "MAR", "Morocco"), (0x74, "GAM", "Gambia"),
    (0x75, "MLW", "Malawi"), (0x76, "JAP", "Japan"), (0x77, "TAI", "Taiwan"),
    (0x78, "IND", "India / Indonesia"), (0x79, "BAN", "Bangladesh"), (0x7a, "BRU", "Brunei"),
    (0x7b, "IRA", "Iraq / Iran"), (0x7c, "JOR", "Jordan"), (0x7d, "SRI", "Sri Lanka"),
    (0x7e, "SYR", "Syria"), (0x7f, "KOR", "South Korea"), (0x80, "IRN", "Iran"),
    (0x81, "VIE", "Vietnam"), (0x82, "MLY", "Malaysia"), (0x83, "SAU", "Saudi Arabia"),
    (0x84, "YEM", "Yemen"), (0x85, "KUW", "Kuwait"), (0x86, "LAO", "Laos"),
    (0x87, "NKR", "North Korea"), (0x88, "OMA", "Oman"), (0x89, "PAK", "Pakistan"),
    (0x8a, "PHI", "Philippines"), (0x8b, "CHN", "China"), (0x8c, "SGP", "Singapore"),
    (0x8d, "MAU", "Mauritius"), (0x8e, "MYA", "Myanmar"), (0x8f, "PAP", "Papua New Guinea"),
    (0x90, "TAD", "Thailand"), (0x91, "UZB", "Uzbekistan"), (0x92, "QAT", "Qatar"),
    (0x93, "UAE", "United Arab Emirates"), (0x94, "AUS", "Australia"), (0x95, "NZL", "New Zealand"),
    (0x96, "FIJ", "Fiji"), (0x97, "SOL", "Solomon Islands"), (0x98, "CUS", "Custom"),
]
NATIONS = {code: (abbr, name) for code, abbr, name in NATIONS_TABLE}


def nation_label(code):
    if code in NATIONS:
        abbr, name = NATIONS[code]
        return f"{abbr} - {name}"
    return f"Unknown ({code:02X})"


def nation_abbr(code):
    return NATIONS[code][0] if code in NATIONS else f"{code:02X}?"


def role_labels(byte):
    return (POSITIONS[(byte & ROLE_MASK) >> 5],
            SKINS.get(byte & SKIN_MASK, f"Unknown ({byte & SKIN_MASK:02X})"))


def health_label(byte):
    return HEALTH[byte & HEALTH_MASK]


def discipline_label(value):
    return DISCIPLINE.get(value, f"{value:02X} (unknown)")


def value_text(code):
    return VALUES[code] if code < len(VALUES) else "unknown"


def value_label(code):
    return value_text(code)


def skill_real(nibble):
    return nibble & 0x07


def skill_flag(nibble):
    return bool(nibble & 0x08)


def decode_skills(four):
    nibbles = []
    for b in four:
        nibbles += [b >> 4, b & 0x0F]
    return nibbles[1:]


def encode_skills(old_four, real_values):
    old = []
    for b in old_four:
        old += [b >> 4, b & 0x0F]
    nibbles = [old[0]] + [(o & 0x08) | (v & 0x07) for o, v in zip(old[1:], real_values)]
    return bytes((nibbles[i] << 4) | nibbles[i + 1] for i in range(0, 8, 2))


class KitPanel(ttk.LabelFrame):
    def __init__(self, master, title):
        super().__init__(master, text=title, padding=10)
        self.style_names = [STYLES[i] for i in sorted(STYLES)]
        self.color_names = [COLORS[i][0] for i in sorted(COLORS)]
        self.vars = []

        for row, field in enumerate(KIT_FIELDS):
            ttk.Label(self, text=field + ":").grid(row=row, column=0, sticky="w", pady=3)
            var = tk.StringVar()
            values = self.style_names if row == 0 else self.color_names
            cb = ttk.Combobox(self, textvariable=var, values=values,
                              state="readonly", width=20)
            cb.grid(row=row, column=1, sticky="w", padx=(8, 0), pady=3)
            cb.bind("<<ComboboxSelected>>", lambda e: self.redraw())
            self.vars.append(var)

        self.canvas = tk.Canvas(self, width=140, height=190, bg=PREVIEW_BG,
                                highlightthickness=1, highlightbackground=PREVIEW_BORDER)
        self.canvas.grid(row=0, column=2, rowspan=6, padx=(18, 0))

    def set_values(self, five_bytes):
        for i, b in enumerate(five_bytes):
            names = self.style_names if i == 0 else self.color_names
            self.vars[i].set(names[b] if b < len(names) else "")
        self.redraw()

    def get_values(self):
        out = []
        for i, var in enumerate(self.vars):
            names = self.style_names if i == 0 else self.color_names
            out.append(names.index(var.get()))
        return out

    def redraw(self):
        c = self.canvas
        c.delete("all")
        try:
            style, prim, sec, shorts, socks = self.get_values()
        except ValueError:
            return
        col = lambda v: COLORS[v][1]
        outline = PREVIEW_OUTLINE

        body = (35, 15, 105, 95)
        c.create_rectangle(*body, fill=col(prim), outline=outline)

        if style == 2:
            w = (body[2] - body[0]) / 5
            for i in range(5):
                x0 = body[0] + i * w
                c.create_rectangle(x0, body[1], x0 + w, body[3],
                                   fill=col(prim if i % 2 == 0 else sec), outline="")
        elif style == 3:
            h = (body[3] - body[1]) / 6
            for i in range(6):
                y0 = body[1] + i * h
                c.create_rectangle(body[0], y0, body[2], y0 + h,
                                   fill=col(prim if i % 2 == 0 else sec), outline="")

        sleeve_col = col(sec) if style == 1 else col(prim)
        c.create_polygon(35, 15, 12, 38, 22, 62, 35, 50, fill=sleeve_col, outline=outline)
        c.create_polygon(105, 15, 128, 38, 118, 62, 105, 50, fill=sleeve_col, outline=outline)
        c.create_rectangle(*body, fill="", outline=outline)

        c.create_rectangle(40, 98, 100, 135, fill=col(shorts), outline=outline)
        c.create_rectangle(45, 138, 65, 180, fill=col(socks), outline=outline)
        c.create_rectangle(75, 138, 95, 180, fill=col(socks), outline=outline)


class SwosEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self._use_theme()
        self._apply_monospace_font()
        self._style_tabs()
        self._style_widgets()
        self.title("Ghizza's Career Editor For SWOS")
        self.resizable(False, False)

        self.file_path = None
        self.file_data = None
        self.players = []
        self._current_base = None

        top = ttk.Frame(self, padding=(12, 12, 12, 0))
        top.pack(fill="x")

        btn_row = ttk.Frame(top)
        btn_row.pack(anchor="center")

        BTN_WIDTH = 22

        ttk.Button(btn_row, text="Open .car file",
                   command=self.open_file, width=BTN_WIDTH).pack(side="left")

        self.save_btn = ttk.Button(btn_row, text="Save kit changes",
                                   command=self.save_file, state="disabled",
                                   width=BTN_WIDTH)
        self.save_btn.pack(side="left", padx=(10, 0))

        self.status = ttk.Label(self, text="No file loaded", anchor="w",
                                justify="left", padding=(12, 8))
        self.status.pack(fill="x")

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.notebook = nb

        club_label = "  Club   "
        players_label = " Players "
        self._tab_labels = (club_label, players_label)

        club = ttk.Frame(nb, padding=(0, 8))
        nb.add(club, text=club_label)
        players_tab = ttk.Frame(nb, padding=8)
        nb.add(players_tab, text=players_label)

        self._build_club_tab(club)
        self._build_players_tab(players_tab)

        nb.bind("<Configure>", lambda e, n=nb: self._center_notebook_tabs(n))

    def _use_theme(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        self.configure(background=APP_BG)

        style.configure(".", background=APP_BG, foreground=APP_FG, bordercolor=BORDER,
                        darkcolor=EDGE_DARK, lightcolor=EDGE_LIGHT, troughcolor=SCROLL_TROUGH,
                        selectbackground=SELECT_BG, selectforeground=SELECT_FG,
                        focuscolor=APP_FG, insertcolor=APP_FG)
        style.map(".",
                  background=[("disabled", APP_BG), ("active", EDGE_LIGHT)],
                  foreground=[("disabled", APP_FG_DISABLED)],
                  selectbackground=[("!focus", SELECT_BG)],
                  selectforeground=[("!focus", SELECT_FG)])

        style.configure("TLabelframe", background=APP_BG, bordercolor=BORDER,
                        lightcolor=EDGE_LIGHT, darkcolor=EDGE_DARK)
        style.configure("TLabelframe.Label", background=APP_BG, foreground=APP_FG)

    def _style_tabs(self):
        self._tab_font = tkfont.nametofont("TkDefaultFont").copy()
        self._tab_font.configure(weight="bold")
        self._tab_pad_x = 60
        self._tab_left_margin = None
        style = ttk.Style(self)
        style.configure("TNotebook", background=APP_BG, bordercolor=BORDER,
                        lightcolor=EDGE_LIGHT, darkcolor=EDGE_DARK, tabmargins=(0, 6, 0, 0))
        style.configure("TNotebook.Tab", font=self._tab_font,
                        padding=(self._tab_pad_x, 9),
                        background=TAB_IDLE_BG, foreground=TAB_IDLE_FG,
                        bordercolor=BORDER, lightcolor=EDGE_DARK, darkcolor=EDGE_DARK)
        style.map("TNotebook.Tab",
                  background=[("selected", TAB_ACTIVE_BG), ("active", TAB_HOVER_BG)],
                  foreground=[("selected", TAB_ACTIVE_FG), ("active", TAB_IDLE_FG)],
                  lightcolor=[("selected", EDGE_LIGHT)],
                  padding=[("selected", (self._tab_pad_x, 12))])

    def _center_notebook_tabs(self, nb):
        nb.update_idletasks()
        nb_w = nb.winfo_width()
        if nb_w <= 1:
            return
        total = sum(self._tab_font.measure(lbl) + 2 * self._tab_pad_x
                    for lbl in self._tab_labels)
        left = max(0, (nb_w - total) // 2)
        if left == self._tab_left_margin:
            return
        self._tab_left_margin = left
        ttk.Style(self).configure("TNotebook", tabmargins=(left, 6, 0, 0))

    def _style_widgets(self):
        style = ttk.Style(self)

        style.configure("TButton", font=self._tab_font, padding=(14, 6),
                        background=BUTTON_BG, foreground=BUTTON_FG,
                        bordercolor=BUTTON_BORDER, lightcolor=BUTTON_BG,
                        darkcolor=BUTTON_BG, focuscolor=BUTTON_FG)
        style.configure("Apply.TButton", padding=(14, 0))
        states = [("disabled", BUTTON_DISABLED_BG), ("pressed", BUTTON_PRESS_BG),
                  ("active", BUTTON_HOVER_BG)]
        style.map("TButton",
                  background=states, lightcolor=states, darkcolor=states,
                  foreground=[("disabled", BUTTON_DISABLED_FG)],
                  bordercolor=[("disabled", BUTTON_DISABLED_BORDER)])

        style.configure("TCombobox", fieldbackground=FIELD_BG, background=ARROW_BG,
                        foreground=FIELD_FG, arrowcolor=ARROW_FG, bordercolor=BORDER,
                        lightcolor=EDGE_LIGHT, darkcolor=EDGE_DARK, insertcolor=FIELD_FG)
        style.map("TCombobox",
                  fieldbackground=[("readonly", FIELD_BG), ("disabled", FIELD_BG_DISABLED)],
                  background=[("disabled", ARROW_BG), ("pressed", ARROW_BG_HOVER),
                              ("active", ARROW_BG_HOVER)],
                  foreground=[("disabled", APP_FG_DISABLED)],
                  arrowcolor=[("disabled", APP_FG_DISABLED)],
                  bordercolor=[("focus", SELECT_BG)],
                  lightcolor=[("focus", SELECT_BG)],
                  darkcolor=[("focus", SELECT_BG)],
                  selectbackground=[("readonly", SELECT_BG)],
                  selectforeground=[("readonly", SELECT_FG)])
        self.option_add("*TCombobox*Listbox.background", FIELD_BG)
        self.option_add("*TCombobox*Listbox.foreground", FIELD_FG)
        self.option_add("*TCombobox*Listbox.selectBackground", SELECT_BG)
        self.option_add("*TCombobox*Listbox.selectForeground", SELECT_FG)

        style.configure("Treeview", background=FIELD_BG, fieldbackground=FIELD_BG,
                        foreground=FIELD_FG, bordercolor=BORDER,
                        lightcolor=EDGE_LIGHT, darkcolor=EDGE_DARK)
        style.map("Treeview",
                  background=[("disabled", APP_BG), ("selected", SELECT_BG)],
                  foreground=[("disabled", APP_FG_DISABLED), ("selected", SELECT_FG)])
        style.configure("Treeview.Heading", background=HEADING_BG, foreground=HEADING_FG,
                        bordercolor=BORDER, lightcolor=EDGE_LIGHT, darkcolor=EDGE_DARK)
        style.map("Treeview.Heading", background=[("active", HEADING_HOVER_BG)])

        style.configure("TScrollbar", background=SCROLL_THUMB, troughcolor=SCROLL_TROUGH,
                        bordercolor=BORDER, lightcolor=EDGE_LIGHT, darkcolor=EDGE_DARK,
                        arrowcolor=SCROLL_ARROW)
        style.map("TScrollbar",
                  background=[("disabled", APP_BG), ("active", SCROLL_THUMB_HOVER)],
                  arrowcolor=[("disabled", APP_FG_DISABLED)])

    def _apply_monospace_font(self):
        available = {f.lower(): f for f in tkfont.families(self)}
        family = next((available[n.lower()] for n in MONOSPACE_FONTS if n.lower() in available),
                      tkfont.nametofont("TkFixedFont").actual("family"))
        for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont",
                     "TkCaptionFont", "TkSmallCaptionFont", "TkIconFont",
                     "TkTooltipFont", "TkFixedFont"):
            try:
                tkfont.nametofont(name).configure(family=family, size=FONT_SIZE)
            except tk.TclError:
                pass
        linespace = tkfont.nametofont("TkDefaultFont").metrics("linespace")
        ttk.Style(self).configure("Treeview", rowheight=linespace + 6)

    def _build_club_tab(self, club):
        bank = ttk.LabelFrame(club, text="Bank balance", padding=10)
        bank.pack(fill="x", pady=(0, 8))
        self.balance_label = ttk.Label(bank, text="-")
        self.balance_label.pack(side="left")
        self.balance_btn = ttk.Button(
            bank, text=f"Set to {self._fmt_money(BALANCE_TARGET)}",
            command=self.set_balance, state="disabled")
        self.balance_btn.pack(side="right")

        transfers = ttk.LabelFrame(club, text="Transfers", padding=10)
        transfers.pack(fill="x", pady=(0, 8))
        self.transfer_label = ttk.Label(transfers, text="-")
        self.transfer_label.pack(side="left")
        self.transfer_btn = ttk.Button(
            transfers, text="Reset transfer counters",
            command=self.reset_transfer_counters, state="disabled")
        self.transfer_btn.pack(side="right")

        self.kit1 = KitPanel(club, "First kit")
        self.kit1.pack(fill="x", pady=(0, 8))
        self.kit2 = KitPanel(club, "Second kit")
        self.kit2.pack(fill="x")
        self._set_kit_panels_enabled(False)

    @staticmethod
    def _fmt_money(value):
        return "£ " + f"{value:,}".replace(",", ".")

    def _read_balance(self):
        raw = self.file_data[BALANCE_OFFSET:BALANCE_OFFSET + BALANCE_SIZE]
        return int.from_bytes(raw, "little")

    def _refresh_balance(self):
        self.balance_label.config(text=f"Now: {self._fmt_money(self._read_balance())}")

    def _read_counter(self, offset):
        return int.from_bytes(self.file_data[offset:offset + 2], "little")

    def _refresh_transfers(self):
        parts = [f"{name} {self._read_counter(o)}" for o, name in TRANSFER_COUNTERS]
        self.transfer_label.config(text="Now: " + " | ".join(parts))

    def _set_kit_panels_enabled(self, enabled):
        state = "readonly" if enabled else "disabled"
        for panel in (self.kit1, self.kit2):
            for child in panel.winfo_children():
                if isinstance(child, ttk.Combobox):
                    child.config(state=state)

    def _build_players_tab(self, tab):
        cw = tkfont.nametofont("TkDefaultFont").measure("0")
        px = lambda chars: chars * cw + 16

        cols = (("n", "#", px(3), "center"),
                ("num", "N.", px(3), "center"),
                ("nome", "Player", px(22), "w"),
                ("naz", "Country", px(8), "center"),
                ("ruolo", "Role", px(5), "w"),
                ("pelle", "Skin & hair", px(12), "w"),
                ("salute", "Health", px(18), "w"),
                ("disc", "Discipline", px(14), "w"),
                ("valore", "Value", px(7), "w"))
        skill_cols = [(n.lower(), n, px(3), "w") for n in SKILL_NAMES]
        allcols = cols + tuple(skill_cols)

        frame = ttk.Frame(tab)
        frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(frame, columns=[c[0] for c in allcols],
                                 show="headings", height=14, selectmode="browse")
        skill_ids = {c[0] for c in skill_cols}
        for cid, head, width, anchor in allcols:
            self.tree.heading(cid, text=head, anchor="w" if cid in skill_ids else "center")
            self.tree.column(cid, width=width, minwidth=width, anchor=anchor, stretch=False)
        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self._on_player_select)
        ttk.Label(tab, text="Skill: real value 0-7. * = high bit set "
                            "(stored value 8-F), preserved.",
                  foreground=APP_FG_MUTED).pack(anchor="w", pady=(4, 0))

        edit = ttk.LabelFrame(tab, text="Selected player", padding=10)
        edit.pack(fill="x", pady=(8, 0))
        self.edit_frame = edit

        self.role_var = tk.StringVar()
        self.skin_var = tk.StringVar()
        self.health_var = tk.StringVar()
        self.disc_var = tk.StringVar()
        self.value_var = tk.StringVar()
        self.nation_var = tk.StringVar()
        self.skill_vars = {n: tk.StringVar() for n in SKILL_NAMES}
        self.edit_widgets = []

        def combo(row, label, var, values, width):
            ttk.Label(edit, text=label).grid(row=row, column=0, sticky="w", pady=3)
            cb = ttk.Combobox(edit, textvariable=var, values=values,
                              state="disabled", width=width)
            cb.grid(row=row, column=1, sticky="w", padx=8, pady=3)
            self.edit_widgets.append(cb)

        combo(0, "Role:", self.role_var, [POSITIONS[i] for i in sorted(POSITIONS)], 30)
        combo(1, "Skin & hair:", self.skin_var, [SKINS[k] for k in sorted(SKINS)], 30)
        combo(2, "Health:", self.health_var, [health_label(k) for k in sorted(HEALTH)], 30)
        combo(3, "Discipline:", self.disc_var, [DISCIPLINE[k] for k in sorted(DISCIPLINE)], 30)
        combo(4, "Value:", self.value_var, [value_label(c) for c in range(len(VALUES))], 30)
        nation_values = [nation_label(c) for c in sorted(NATIONS, key=lambda c: NATIONS[c][1])]
        combo(5, "Country:", self.nation_var, nation_values, 30)

        skills = ttk.LabelFrame(edit, text="Skill (0-7)", padding=6)
        skills.grid(row=0, column=2, rowspan=5, padx=(16, 0), sticky="n")
        for i, n in enumerate(SKILL_NAMES):
            ttk.Label(skills, text=n).grid(row=0, column=i, padx=SKILL_GAP)
            cb = ttk.Combobox(skills, textvariable=self.skill_vars[n], state="disabled",
                              values=[str(v) for v in range(8)], width=3)
            cb.grid(row=1, column=i, padx=SKILL_GAP, pady=2)
            self.edit_widgets.append(cb)

        self.apply_btn = ttk.Button(edit, text="Apply and save", style="Apply.TButton",
                                    command=self.apply_player, state="disabled")
        self.apply_btn.grid(row=5, column=2, padx=(16, 0), pady=3, sticky="nsew")
        self.player_msg = ttk.Label(edit, text="")
        self.player_msg.grid(row=6, column=0, columnspan=3, sticky="w", pady=(6, 0))

    def _squad_indices(self, n_records):
        d = self.file_data
        if SQUAD_COUNT_OFFSET >= len(d):
            return None
        count = d[SQUAD_COUNT_OFFSET]
        if not 0 < count <= SQUAD_LIST_SIZE:
            return None
        idx = list(d[SQUAD_LIST_OFFSET:SQUAD_LIST_OFFSET + count])
        if len(set(idx)) != count or any(i >= n_records for i in idx):
            return None
        return set(idx)

    def _load_players(self):
        self.players = []
        self._current_base = None
        data = self.file_data
        records = []
        for i in range(MAX_PLAYERS):
            base = PLAYERS_START + i * PLAYER_SIZE
            if base + PLAYER_SIZE > len(data):
                break
            raw = bytes(data[base + NAME_OFF:base + NAME_OFF + NAME_FIELD_LEN])
            raw = raw.split(b"\x00")[0]
            if not raw or not all(32 <= b < 127 for b in raw):
                break
            records.append((base, raw.decode("ascii"), data[base + NUMBER_OFF]))

        squad = self._squad_indices(len(records))
        if squad is None:
            self.players = records
            note = "squad list not valid, showing every record"
        else:
            self.players = [r for i, r in enumerate(records) if i in squad]
            note = f"{len(records) - len(self.players)} records not in the squad are hidden"
        self._sort_players()
        self._fill_table()
        for w in self.edit_widgets:
            w.config(state="disabled")
        self.apply_btn.config(state="disabled")
        self.edit_frame.config(text="Selected player")
        self.player_msg.config(text=f"{len(self.players)} players ({note}).")

    def _sort_players(self):
        d = self.file_data
        self.players.sort(key=lambda p: (ROLE_RANK[(d[p[0] + ROLE_OFF] & ROLE_MASK) >> 5], p[0]))

    def _fill_table(self):
        self.tree.delete(*self.tree.get_children())
        for i in range(len(self.players)):
            self._refresh_player_row(i, insert=True)

    def _refresh_player_row(self, i, insert=False):
        base, name, number = self.players[i]
        d = self.file_data
        role, skin = role_labels(d[base + ROLE_OFF])
        health = health_label(d[base + HEALTH_OFF])
        skills = decode_skills(d[base + SKILLS_OFF:base + SKILLS_OFF + 4])
        values = ((i + 1, number, name, nation_abbr(d[base + NATION_OFF]), role, skin, health,
                   discipline_label(d[base + HEALTH_OFF] & DISCIPLINE_MASK), value_text(d[base + VALUE_OFF]))
                  + tuple(f"{skill_real(v)}{'*' if skill_flag(v) else ''}" for v in skills))
        if insert:
            self.tree.insert("", "end", iid=str(i), values=values)
        else:
            self.tree.item(str(i), values=values)

    def _on_player_select(self, _event=None):
        sel = self.tree.selection()
        if not sel or self.file_data is None:
            return
        base = self.players[int(sel[0])][0]
        d = self.file_data
        self.edit_frame.config(text=f"Selected player: {self.players[int(sel[0])][1]}")
        role, skin = role_labels(d[base + ROLE_OFF])
        self.role_var.set(role)
        self.skin_var.set(skin if skin in SKINS.values() else "")
        self.health_var.set(health_label(d[base + HEALTH_OFF]))
        self.disc_var.set(discipline_label(d[base + HEALTH_OFF] & DISCIPLINE_MASK))
        self.value_var.set(value_label(d[base + VALUE_OFF]))
        self.nation_var.set(nation_label(d[base + NATION_OFF]))
        skills = decode_skills(d[base + SKILLS_OFF:base + SKILLS_OFF + 4])
        for n, v in zip(SKILL_NAMES, skills):
            self.skill_vars[n].set(str(skill_real(v)))
        for w in self.edit_widgets:
            w.config(state="readonly")
        self.apply_btn.config(state="normal")
        if base != self._current_base:
            self.player_msg.config(text="")
        self._current_base = base

    def apply_player(self):
        sel = self.tree.selection()
        if not sel or self.file_data is None:
            return
        i = int(sel[0])
        role_names = [POSITIONS[k] for k in sorted(POSITIONS)]
        skin_by_label = {v: k for k, v in SKINS.items()}
        health_by_label = {health_label(k): k for k in HEALTH}
        try:
            pos = role_names.index(self.role_var.get())
            skin = skin_by_label[self.skin_var.get()]
            health = health_by_label[self.health_var.get()]
            disc_by_label = {v: k for k, v in DISCIPLINE.items()}
            disc_text = self.disc_var.get()
            if disc_text in disc_by_label:
                disc = disc_by_label[disc_text]
            elif disc_text.endswith("(unknown)"):
                disc = None
            else:
                raise ValueError(disc_text)
            value_text_sel = self.value_var.get()
            value_by_label = {value_label(c): c for c in range(len(VALUES))}
            if value_text_sel in value_by_label:
                value = value_by_label[value_text_sel]
            elif value_text_sel == "unknown":
                value = self.file_data[self.players[i][0] + VALUE_OFF]
            else:
                raise ValueError(value_text_sel)
            nation_by_label = {nation_label(c): c for c in NATIONS}
            nation_text = self.nation_var.get()
            if nation_text in nation_by_label:
                nation = nation_by_label[nation_text]
            elif nation_text.startswith("Unknown"):
                nation = None
            else:
                raise ValueError(nation_text)
            skills = [int(self.skill_vars[n].get()) for n in SKILL_NAMES]
            if not all(0 <= v <= 7 for v in skills):
                raise ValueError("skill fuori scala")
        except (ValueError, KeyError):
            messagebox.showerror("Error", "Fill in all the player's fields.")
            return

        base, name = self.players[i][0], self.players[i][1]
        if disc is None:
            disc = self.file_data[base + HEALTH_OFF] & DISCIPLINE_MASK
        first, last = base + ROLE_OFF, base + VALUE_OFF + 1
        snapshot = bytes(self.file_data[first:last])
        d = self.file_data
        old_nation = d[base + NATION_OFF]

        d[base + ROLE_OFF] = (d[base + ROLE_OFF] & ~(ROLE_MASK | SKIN_MASK) & 0xFF) | (pos << 5) | skin
        d[base + HEALTH_OFF] = health | disc
        so = base + SKILLS_OFF
        d[so:so + 4] = encode_skills(d[so:so + 4], skills)
        d[base + VALUE_OFF] = value
        if nation is not None:
            d[base + NATION_OFF] = nation

        if self._write_file() is None:
            d[first:last] = snapshot
            d[base + NATION_OFF] = old_nation
            return
        order_before = [pl[0] for pl in self.players]
        self._sort_players()
        if [pl[0] for pl in self.players] != order_before:
            self._fill_table()
            new_i = next(k for k, pl in enumerate(self.players) if pl[0] == base)
            self.tree.selection_set(str(new_i))
            self.tree.see(str(new_i))
        else:
            self._refresh_player_row(i)
        new = bytes(d[first:last])
        self.player_msg.config(
            text=f"{name} - country 0x{base:X}: {old_nation:02X} -> "
                 f"{d[base + NATION_OFF]:02X}; bytes from 0x{first:X}: "
                 f"{snapshot.hex(' ').upper()} -> {new.hex(' ').upper()} (saved)")

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Select a .car file",
            filetypes=[("SWOS Career", "*.car *.CAR *.Car *.cAR"),
                       ("All files", "*.*")],
        )
        if not path:
            return

        if os.path.splitext(path)[1].lower() != ".car":
            if not messagebox.askyesno(
                "Non-standard extension",
                f"The selected file is not a .car file:\n\n{path}\n\nContinue anyway?",
            ):
                return

        try:
            with open(path, "rb") as f:
                data = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Unable to read file:\n{e}")
            return

        if len(data) < KIT_OFFSET + KIT_SIZE:
            messagebox.showerror(
                "Error",
                f"File is too short ({len(data)} bytes) to contain the kits "
                f"at offset 0x{KIT_OFFSET:X}. Not a valid SWOS save file.",
            )
            return

        block = data[KIT_OFFSET:KIT_OFFSET + KIT_SIZE]
        bad = [i for i, b in enumerate(block)
               if (b not in STYLES if i % 5 == 0 else b not in COLORS)]
        if bad:
            messagebox.showerror(
                "Error",
                "Unexpected byte values at kit offset:\n\n"
                f"{block.hex(' ').upper()}\n\n"
                "The file doesn't look like a SWOS save file. "
                "It was not loaded.",
            )
            return

        self.file_path = path
        self.file_data = bytearray(data)
        self.kit1.set_values(block[:5])
        self.kit2.set_values(block[5:])
        self._set_kit_panels_enabled(True)
        self.save_btn.config(state="normal")
        self.balance_btn.config(state="normal")
        self._refresh_balance()
        self.transfer_btn.config(state="normal")
        self._refresh_transfers()
        self._load_players()

        team = self._read_team_name(data)
        self.status.config(
            text=f"File: {os.path.basename(path)}  ({len(data)} bytes)\n"
                 f"Team: {team or '(unreadable name)'}"
        )

    @staticmethod
    def _read_team_name(data):
        raw = bytes(data[TEAM_NAME_OFFSET:TEAM_NAME_OFFSET + TEAM_NAME_LEN]).split(b"\x00")[0]
        return "".join(chr(b) if 32 <= b < 127 else "?" for b in raw).strip()

    def _write_file(self):
        backup = self.file_path + ".bak"
        try:
            if not os.path.exists(backup):
                shutil.copy2(self.file_path, backup)
            with open(self.file_path, "wb") as f:
                f.write(self.file_data)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to save file:\n{e}")
            return None
        return backup

    def save_file(self):
        if self.file_data is None:
            return
        try:
            new_block = bytes(self.kit1.get_values() + self.kit2.get_values())
        except ValueError:
            messagebox.showerror("Error", "Fill in all the fields before saving.")
            return

        self.file_data[KIT_OFFSET:KIT_OFFSET + KIT_SIZE] = new_block
        backup = self._write_file()
        if backup is None:
            return

        messagebox.showinfo(
            "Saved",
            f"Kits saved in:\n{self.file_path}\n\n"
            f"Bytes written: {new_block.hex(' ').upper()}\n"
            f"Copy of original: {os.path.basename(backup)}",
        )

    def set_balance(self):
        if self.file_data is None:
            return
        old = self._read_balance()
        new_bytes = BALANCE_TARGET.to_bytes(BALANCE_SIZE, "little")
        self.file_data[BALANCE_OFFSET:BALANCE_OFFSET + BALANCE_SIZE] = new_bytes
        backup = self._write_file()
        if backup is None:
            return
        self._refresh_balance()
        messagebox.showinfo(
            "Bank balance updated",
            f"Before: {self._fmt_money(old)}\n"
            f"Now: {self._fmt_money(BALANCE_TARGET)}\n\n"
            f"Bytes written at 0x{BALANCE_OFFSET:X}: {new_bytes.hex(' ').upper()}\n"
            f"Copy of original: {os.path.basename(backup)}",
        )

    def reset_transfer_counters(self):
        if self.file_data is None:
            return
        old = {o: bytes(self.file_data[o:o + 2]) for o, _ in TRANSFER_COUNTERS}
        for o, _ in TRANSFER_COUNTERS:
            self.file_data[o:o + 2] = b"\x00\x00"
        backup = self._write_file()
        if backup is None:
            for o, raw in old.items():
                self.file_data[o:o + 2] = raw
            return
        self._refresh_transfers()
        changes = "\n".join(
            f"0x{o:X} ({name}): {int.from_bytes(old[o], 'little')} -> 0"
            for o, name in TRANSFER_COUNTERS)
        messagebox.showinfo(
            "Transfer counters reset",
            f"{changes}\n\nCopy of original: {os.path.basename(backup)}",
        )


def enable_hidpi():
    import sys
    if sys.platform != "win32":
        return
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def main():
    enable_hidpi()
    SwosEditor().mainloop()


if __name__ == "__main__":
    main()
