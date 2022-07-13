let s:LOWL = ['#002833', 234]
let s:HIGH = ['#023846', 237]
let s:TEXT = ['#a2afb6', 145]
let s:DRED = ['#f84770', 204]
let s:ORNG = ['#f96829', 208]
let s:GREN = ['#28ac28', 70]
let s:BLUE = ['#3399f6', 39]
let s:PRPL = ['#ac7df6', 141]

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
