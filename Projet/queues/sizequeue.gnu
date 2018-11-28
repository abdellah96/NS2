reset
set terminal png
set output "size.png"

set title "Analysis"
set xlabel "Time (ms)"
set ylabel "Packets"
set autoscale
plot "queue-0-1.tr" using 1:5 title 'Size Queue' w l
