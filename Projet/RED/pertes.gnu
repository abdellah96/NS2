reset
set terminal png
set output "pertes.png"

set title "Analysis"
set xlabel "Time (ms)"
set ylabel "Packets"
set autoscale
plot "queue-0-1.tr" using 1:11 title 'Pertes' w l
