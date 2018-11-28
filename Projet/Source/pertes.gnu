reset
set terminal png
set output "pertes.png"

set title "Analysis"
set xlabel "Time (ms)"
set ylabel "Packets"
set autoscale
plot "total.dat" using 1:2 title 'Pertes' w l
