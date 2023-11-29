set terminal gif animate delay 100

set output 'exp-euler-fortran.gif'

stats 'output_1_2.dat' nooutput

set xrange [0:15]
set yrange [0:10]

do for [i=0:1260:50] {
    plot 'output_1_2.dat' u ($1==i?$2:1/0):3 w l
}