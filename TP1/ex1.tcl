
set ns [new Simulator]
set nf [open out.nam w]
$ns namtrace-all $nf

proc finish {} {
        global ns nf
        $ns flush-trace
        #Close the NAM trace file
        close $nf
        #Execute NAM on the trace file
        exec nam -a out.nam &
        exit 0
}

for {set i 0} {$i<6} {incr i} {
  set n($i) [$ns node]
}

for {set i 0} {$i < 2} {incr i} {
    for {set j 0} {$j < $i} {incr j} {
        $ns duplex-link $n($i) $n($j) 2mb 10ms DropTail
    }
}

for {set i 2} {$i <= 3} {incr i} {
    $ns duplex-link $n(0) $n($i) 2Mb 10ms DropTail
}

for {set i 4} {$i <= 5} {incr i} {
    $ns duplex-link $n(1) $n($i) 2Mb 10ms DropTail
}

for {set i 2} {$i <= 5} {incr i} {
    set udp($i) [new Agent/UDP]
    $ns attach-agent $n($i) $udp($i)
    set cbr($i) [new Application/Traffic/CBR]
    $cbr($i) set packetSize_ 500
    $cbr($i) set interval_ 0.005
    $cbr($i) attach-agent $udp($i)
}

for {
    set i 2} {$i <= 5} {incr i} {
    $ns at 0.5 "$cbr($i) start"
    $ns at 4.5 "$cbr($i) stop"
}

$ns at 5.0 finish

$ns run
