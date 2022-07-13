# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# Base Color Selection                                                         ┃
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

# ───────────────────────────╮
# Define Fibonacci functions │
# ───────────────────────────╯

# Define a Fibonacci number generator
def fibnum(fibnum_index):
    fibseq = [0,1]
    for i in range(fibnum_index-1): fibseq.append(fibseq[-1] + fibseq[-2])
    return fibseq[-1]

# Define a fibstep generator
# ‣ a "fibstep" is the interval size on a scale with n equally spaced points,
#   where n is a Fibonacci number
def fibstep(fibnum_index): return 1/(fibnum(fibnum_index)-1)

# ───────────────────────╮
# Define other functions │
# ───────────────────────╯

# Define a decimal-to-percent function
def p(decimal): return decimal * 100

# Define functions to derive one base color attribute from another
def lightfn(sat): return (p(4) - 3 * sat  ) / 5  # lightness from saturation
def satfn(light): return (p(4) - 5 * light) / 3  # saturation from lightness

# ────────────────────────────────────────────────────────────────────────────╮
# Set saturation and lightness of three base colors, starting with saturation │
# ────────────────────────────────────────────────────────────────────────────╯

# Set saturation values
sat_base = [p(1+fibstep(10)),  # background
            p(1-fibstep(10)),  # highlighting
            p(0-fibstep( 6))]  # cursor

# Get lightness values
light_base = []
for i in range(len(sat_base)): light_base.append(lightfn(sat_base[i]))

# ──────────────────────────────────────────────────────────────────────────╮
# Set saturation and lightness of four base colors, starting with lightness │
# ──────────────────────────────────────────────────────────────────────────╯

# Calculate the golden ratio (phi)
phi = (1+5**(1/2))/2

# Set lightness values
light_base_add = [p(fibstep(6)),  # lowlighting
                  p(3**(-1/2)) ,  # visual selection
                  p(phi-1)     ,  # muted text
                  p(2**(-1/2)) ]  # normal text

# Get saturation values
for i in range(len(light_base_add)):
    light_base.append(light_base_add[i])
    sat_base.append(satfn(light_base_add[i]))

# ───────────────────────────────────────────╮
# Convert base colors from HSLuv to sRGB hex │
# ───────────────────────────────────────────╯

# Tamp overshot saturation values
for i in range(len(sat_base)):
    if sat_base[i] > 100: sat_base[i] = 100

# Convert colors, holding hue constant at "phyan" (360/phi)
from hsluv import hsluv_to_hex
hex_base = []
for i in range(len(sat_base)):
    hex_base.append(hsluv_to_hex([360/phi, sat_base[i], light_base[i]]))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# Syntax Color Selection                                                       ┃
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

# ──────────────────────────────────╮
# Set constants for hue calculation │
# ──────────────────────────────────╯

# Set corner hue values
# ‣ these values, calculated with hsluv.mac (github.com/hsluv/hsluv), mark the
#   corners of HSLuv color space where lightness = 100/phi
o =  22.11870935  # orange
g = 127.7150129   # green
b = 248.8902251   # blue
m = 307.7150129   # magenta

# Calculate length of each color space edge
go = g - o
bg = b - g
mb = m - b
om = o + (360 - m)

# ──────────────────────╮
# Calculate syntax hues │
# ──────────────────────╯

hue_synt = [m + om/2,  # magenta
            o       ,  # orange
            o + go/3,  # yellow
            g       ,  # green
            g + bg/2,  # cyan
            b       ,  # blue
            b + mb/2,  # purple
            o - om/4]  # red

# ─────────────────────────────────────────────╮
# Convert syntax colors from HSLuv to sRGB hex │
# ─────────────────────────────────────────────╯

# Set syntax saturation
sat_synt = p(1-fibstep(7))

# Convert main syntax colors, holding saturation and lightness constant
hex_synt = []
for i in range(len(hue_synt)-1):
    hex_synt.append(hsluv_to_hex([hue_synt[i], sat_synt, light_base[5]]))

# Add syntax colors that use different lightness values (dark red, light yellow)
hex_darkred = hsluv_to_hex([hue_synt[7], sat_synt, light_base[4]])
hex_lyellow = hsluv_to_hex([hue_synt[2], sat_synt, light_base[6]])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# Colortemplate File Generation - Part 1: Color Scheme for Vim                 ┃
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

# ──────────╮
# Set paths │
# ──────────╯

import os,sys
dirtop = os.path.split(os.path.abspath(os.path.dirname(sys.argv[0])))[0]
dirgen = dirtop + "/gen/"
dirsrc = dirtop + "/src/"
colortemplate_file = dirsrc + "rdy.colortemplate"

# ────────────────────────────────────╮
# Prepare to write colortemplate file │
# ────────────────────────────────────╯

content = open(colortemplate_file, "w")
def wb(text): content.write(text)                  # write block of text
def wl(text): content.write(text + "\n")           # write line of text
def ws(): content.write("\n; " + "-" * 78 + "\n")  # write section break

# ────────────────────────────╮
# Write color scheme metadata │
# ────────────────────────────╯

wb("""colortemplate options: source_comment=0 timestamp=0

full name:  rdy
short name: rdy
author:     haystackandroid
website:    github.com/haystackandroid/vim-rdy
license:    bsd-2-clause-patent
neovim:     yes

background: any
variant:    gui 256

""")

# ─────────────────────────────╮
# Write color name assignments │
# ─────────────────────────────╯

wl("color: LOWL " + hex_base[3] + " 234")  # lowlighting
wl("color: BACK " + hex_base[0] + " 236")  # background
wl("color: HIGH " + hex_base[1] + " 237")  # highlighting
wl("color: VSEL " + hex_base[4] + "  67")  # visual selection
wl("color: MUTE " + hex_base[5] + " 247")  # muted text
wl("color: TEXT " + hex_base[6] + " 145")  # normal text
wl("color: CRSR " + hex_base[2] + " 254")  # cursor
wl("color: DRED " + hex_darkred + " 204")  # dark red
wl("color: MGNT " + hex_synt[0] + " 205")  # magenta
wl("color: ORNG " + hex_synt[1] + " 208")  # orange
wl("color: YLLW " + hex_synt[2] + " 178")  # yellow
wl("color: GREN " + hex_synt[3] + "  70")  # green
wl("color: CYAN " + hex_synt[4] + "  37")  # cyan
wl("color: BLUE " + hex_synt[5] + "  39")  # blue
wl("color: PRPL " + hex_synt[6] + " 141")  # purple
wl("color: LYLW " + hex_lyellow + " 178")  # light yellow
wl("")

# ───────────────────────────╮
# Configure highlight groups │
# ───────────────────────────╯
# ‣ define a set of visual styles
# ‣ assign each style to a set of highlight groups

highlight_group_sets = [

# Normal text: standard UI
["TEXT BACK", "ModeMsg", "Normal", "Terminal"],
["none none bold", "Conceal", "Title"],
["none none underline", "Underlined"],
["none HIGH", "ColorColumn", "Pmenu"],
["none HIGH underline", "StatusLineNC", "StatusLineTermNC", "TabLine",
    "TabLineFill", "WildMenu"],

# Muted text: recessed UI
["MUTE none", "EndOfBuffer", "LineNr", "SignColumn"],
["MUTE none bold", "FoldColumn", "Folded", "SpecialKey"],

# Lowlit text: emphasized UI
["none LOWL", "CursorColumn", "CursorLine", "CursorLineFold", "CursorLineSign"],
["MUTE LOWL", "CursorLineNr"],
["VSEL LOWL", "VisualNOS"],

# Reverse text: heavily emphasized UI
["VSEL LOWL reverse", "Visual"],
["TEXT LOWL reverse", "PmenuSel", "StatusLine", "StatusLineTerm", "TabLineSel",
    "ToolbarButton"],
["CRSR LOWL reverse", "Cursor"],

# Solid lines: UI borders/bars
["LOWL LOWL", "VertSplit"],
["HIGH HIGH", "PmenuSbar"],
["TEXT TEXT", "PmenuThumb", "ToolbarLine"],

# Magenta text: types
["MGNT none", "StorageClass", "Structure", "Type", "Typedef"],

# Orange text: statements, focused search matches
["ORNG none", "Conditional", "Exception", "Keyword", "Label", "Operator",
    "Repeat", "Statement"],
["ORNG LOWL reverse", "CurSearch", "IncSearch"],

# Yellow text: identifiers, changed lines (diff mode)
["YLLW none", "Function", "Identifier"],
["YLLW LOWL reverse", "DiffChange", "DiffChanged"],

# Green text: special elements, added lines (diff mode), continue prompts
["GREN none", "Debug", "Delimiter", "Special", "SpecialChar", "Tag"],
["GREN LOWL reverse", "DiffAdd", "DiffAdded", "MoreMsg", "Question"],

# Cyan text: constants, bracket matches
["CYAN none", "Boolean", "Character", "Constant", "Float", "Number", "String"],
["CYAN LOWL reverse", "MatchParen"],

# Blue text: meta-statements, directories, within-line changes (diff mode)
["BLUE none", "Define", "Include", "Macro", "PreCondit", "PreProc"],
["BLUE none bold", "Directory"],
["BLUE LOWL reverse", "DiffText"],

# Purple text: comments, nontext, todo keywords, warnings
["PRPL none", "Comment", "SpecialComment"],
["PRPL none bold", "NonText"],
["PRPL LOWL reverse", "Todo", "WarningMsg"],

# Dark red text: deleted lines (diff mode), errors
["DRED LOWL reverse", "DiffDelete", "DiffRemoved", "Error", "ErrorMsg"],

# Light yellow text: quickfix line, unfocused search matches
["LYLW LOWL reverse", "QuickFixLine", "Search"]]

# Spellcheck undercurls
spell_template = "Spell{} none none g=undercurl s={} t=undercurl"
spell_colors = [["Bad"  , "MGNT"],  # magenta: misspellings
                ["Cap"  , "BLUE"],  # blue: missing capitalizations
                ["Local", "CYAN"],  # cyan: foreign spellings
                ["Rare" , "PRPL"]]  # purple: rare words

# ───────────────────────╮
# Write highlight groups │
# ───────────────────────╯

for i in range(2): wl("term colors: BACK MGNT GREN YLLW BLUE PRPL CYAN TEXT")
wl("")
for group_set in highlight_group_sets:
    for group in group_set[1:]:
        wl("".join([group.ljust(17), group_set[0]]))
    wl("")
for color in spell_colors:
    wl("".join([spell_template.format(color[0].ljust(11),color[1])]))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# Colortemplate File Generation - Part 2: Color Schemes for Other Software     ┃
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

ws()

# ────────────────────────────────────╮
# Write Xresources configuration file │
# ────────────────────────────────────╯

wb("""
auxfile terminal/rdy.Xresources
*background:  @guiBACK
*foreground:  @guiTEXT
*cursorColor: @guiCRSR
*color0:      @guiBACK
*color8:      @guiBACK
*color1:      @guiMGNT
*color9:      @guiMGNT
*color2:      @guiGREN
*color10:     @guiGREN
*color3:      @guiYLLW
*color11:     @guiYLLW
*color4:      @guiBLUE
*color12:     @guiBLUE
*color6:      @guiCYAN
*color14:     @guiCYAN
*color5:      @guiPRPL
*color13:     @guiPRPL
*color7:      @guiTEXT
*color15:     @guiTEXT
endauxfile
""")

ws()

# ────────────────────────────────────────────╮
# Write Alacritty terminal configuration file │
# ────────────────────────────────────────────╯

wb("""
auxfile terminal/rdy.alacritty.yml
colors:
  primary:
    background:        '@guiBACK'
    dim_foreground:    '@guiMUTE'
    foreground:        '@guiTEXT'
    bright_foreground: '@guiCRSR'
  dim:
    black:             '@guiLOWL'
    red:               '@guiMGNT'
    green:             '@guiGREN'
    yellow:            '@guiYLLW'
    blue:              '@guiBLUE'
    magenta:           '@guiPRPL'
    cyan:              '@guiCYAN'
    white:             '@guiMUTE'
  normal:
    black:             '@guiBACK'
    red:               '@guiMGNT'
    green:             '@guiGREN'
    yellow:            '@guiYLLW'
    blue:              '@guiBLUE'
    magenta:           '@guiPRPL'
    cyan:              '@guiCYAN'
    white:             '@guiTEXT'
  bright:
    black:             '@guiMUTE'
    red:               '@guiMGNT'
    green:             '@guiGREN'
    yellow:            '@guiYLLW'
    blue:              '@guiBLUE'
    magenta:           '@guiPRPL'
    cyan:              '@guiCYAN'
    white:             '@guiCRSR'
  cursor:
    text:              '@guiBACK'
    cursor:            '@guiCRSR'
  search:
    matches:
      foreground:      '@guiBACK'
      background:      '@guiLYLW'
    focused_match:
      foreground:      '@guiBACK'
      background:      '@guiORNG'
  hints:
    start:
      foreground:      '@guiLOWL'
      background:      '@guiDRED'
    end:
      foreground:      '@guiDRED'
      background:      '@guiLOWL'
  selection:
    text:              '@guiBACK'
    background:        '@guiMUTE'
endauxfile
""")

ws()

# ─────────────────────────────────────╮
# Write vim-airline configuration file │
# ─────────────────────────────────────╯

wb("""
auxfile autoload/airline/themes/rdy.vim
let g:airline#themes#rdy#palette = {}

let s:LOWL = ['@guiLOWL', @term256LOWL]
let s:HIGH = ['@guiHIGH', @term256HIGH]
let s:TEXT = ['@guiTEXT', @term256TEXT]
let s:DRED = ['@guiDRED', @term256DRED]
let s:GREN = ['@guiGREN', @term256GREN]
let s:BLUE = ['@guiBLUE', @term256BLUE]

let s:nrm1 = [s:LOWL[0], s:TEXT[0], s:LOWL[1], s:TEXT[1]]
let s:nrm2 = [s:TEXT[0], s:HIGH[0], s:TEXT[1], s:HIGH[1]]
let s:insr = [s:LOWL[0], s:GREN[0], s:LOWL[1], s:GREN[1]]
let s:visl = [s:LOWL[0], s:BLUE[0], s:LOWL[1], s:BLUE[1]]
let s:rplc = [s:LOWL[0], s:DRED[0], s:LOWL[1], s:DRED[1]]
let s:inac = [s:TEXT[0], s:HIGH[0], s:TEXT[1], s:HIGH[1]]

let g:airline#themes#rdy#palette.normal =
  \ airline#themes#generate_color_map(s:nrm1 , s:nrm2 , s:nrm2)

let g:airline#themes#rdy#palette.insert =
  \ airline#themes#generate_color_map(s:insr , s:nrm2 , s:nrm2)

let g:airline#themes#rdy#palette.visual =
  \ airline#themes#generate_color_map(s:visl , s:nrm2 , s:nrm2)

let g:airline#themes#rdy#palette.replace =
  \ airline#themes#generate_color_map(s:rplc , s:nrm2 , s:nrm2)

let g:airline#themes#rdy#palette.inactive =
  \ airline#themes#generate_color_map(s:inac , s:inac , s:inac)

if !get(g:, 'loaded_ctrlp', 0)
  finish
endif

let g:airline#themes#rdy#palette.ctrlp =
  \ airline#extensions#ctrlp#generate_color_map(s:nrm2, s:nrm1, s:nrm2 )
endauxfile
""")

ws()

# ───────────────────────────────────────╮
# Write lightline.vim configuration file │
# ───────────────────────────────────────╯

wb("""
auxfile autoload/lightline/colorscheme/rdy.vim
let s:LOWL = ['@guiLOWL', @term256LOWL]
let s:HIGH = ['@guiHIGH', @term256HIGH]
let s:TEXT = ['@guiTEXT', @term256TEXT]
let s:DRED = ['@guiDRED', @term256DRED]
let s:ORNG = ['@guiORNG', @term256ORNG]
let s:GREN = ['@guiGREN', @term256GREN]
let s:BLUE = ['@guiBLUE', @term256BLUE]
let s:PRPL = ['@guiPRPL', @term256PRPL]

let s:p = { 'normal' : {} , 'inactive': {} , 'insert'  : {} ,
          \ 'replace': {} , 'visual'  : {} , 'tabline' : {} }

let s:p.normal.left     = [[s:LOWL, s:TEXT], [s:LOWL, s:TEXT]]
let s:p.normal.middle   = [[s:TEXT, s:HIGH]]
let s:p.normal.right    = [[s:LOWL, s:TEXT], [s:LOWL, s:TEXT]]

let s:p.inactive.left   = copy(s:p.normal.middle)
let s:p.inactive.middle = copy(s:p.normal.middle)
let s:p.inactive.right  = copy(s:p.normal.middle)

let s:p.insert.left     = [[s:LOWL, s:GREN], [s:LOWL, s:GREN]]
let s:p.insert.right    = [[s:LOWL, s:GREN], [s:LOWL, s:GREN]]

let s:p.visual.left     = [[s:LOWL, s:BLUE], [s:LOWL, s:BLUE]]
let s:p.visual.right    = [[s:LOWL, s:BLUE], [s:LOWL, s:BLUE]]

let s:p.replace.left    = [[s:LOWL, s:DRED ], [s:LOWL, s:DRED ]]
let s:p.replace.right   = [[s:LOWL, s:DRED ], [s:LOWL, s:DRED ]]

let s:p.tabline.left    = copy(s:p.normal.middle)
let s:p.tabline.tabsel  = [[s:LOWL, s:TEXT]]
let s:p.tabline.right   = copy(s:p.normal.middle)

let s:p.normal.error    = [[s:DRED, s:LOWL]]
let s:p.normal.warning  = [[s:PRPL, s:LOWL]]

let g:lightline#colorscheme#rdy#palette = lightline#colorscheme#flatten(s:p)
endauxfile
""")

content.close()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# File Management                                                              ┃
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

# ───────────────╮
# Generate files │
# ───────────────╯

import subprocess
subprocess.run(["vim", "-c", "Colortemplate", colortemplate_file, "-c", "q"])

# ───────────────────────────────────────────────╮
# Move generated files to (clean) directory /gen │
# ───────────────────────────────────────────────╯

subprocess.run(["rm", "-r", dirgen])
subprocess.run(["mkdir", "-p", dirgen + "templates/"])
subprocess.run(["mv", colortemplate_file, dirgen + "templates/"])
for subdir in ["autoload/", "colors/", "terminal/"]:
    subprocess.run(["mv", dirsrc + subdir, dirgen])

# ───────────────────────────────────────────────────╮
# Create symlinks for Vim plugin directory structure │
# ───────────────────────────────────────────────────╯

for subdir in ["autoload", "colors"]:
    subprocess.run(["ln", "-srf", dirgen + subdir, dirtop])
