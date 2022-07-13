let g:airline#themes#rdy#palette = {}

let s:LOWL = ['#002833', 234]
let s:HIGH = ['#023846', 237]
let s:TEXT = ['#a2afb6', 145]
let s:DRED = ['#f84770', 204]
let s:GREN = ['#28ac28', 70]
let s:BLUE = ['#3399f6', 39]

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
