reset
set terminal png
set output "bandwidth.png"

set title "Analysis"
set xlabel "Time (ms)"
set ylabel "Bandwidth (Mbps)"
set autoscale
plot "total.dat" using 1:3 title 'Bande passante' w l


