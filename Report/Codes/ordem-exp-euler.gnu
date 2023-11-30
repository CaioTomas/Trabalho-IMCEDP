reset

set terminal wxt enhanced dashed

set terminal epslatex color standalone
set output 'ordem-exp-euler.tex'

unset key
set grid

f(x) = a*x*x

fit f(x) 'ordem-exp-euler.dat' u 1:(abs($5 - 0.63222941839548519)) via a

set xlabel '$\Delta x$'
set ylabel '$|\mathrm{erro}|$'

plot 'ordem-exp-euler.dat' u 1:(abs($5 - 0.63222941839548519)) w p pt 5 notitle, f(x) w l

set terminal wxt
replot