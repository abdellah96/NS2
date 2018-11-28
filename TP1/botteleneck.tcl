#creation simulateur
set ns [new Simulator]


set Num_transmitters 3
set Num_receivers 3

set nf [open out.nam w]
$ns namtrace-all $nf




proc finish {} {
    global ns nf Num_transmitters
	  $ns flush-trace
  	close $nf
    exec nam out.nam &
    exit 0
  }

#Fichiers d'écriture des résultats des émetteurs
for { set i 1 } { $i <= $Num_transmitters } { incr i } {
	set (f-1-$i) [open out-1-$i.tr w]
}

#création des noeuds bottle neck
set (n-2-0) [$ns node]
set (n-1-0) [$ns node]

#création du lien bottle neck

$ns duplex-link $(n-2-0) $(n-1-0) 10Mb 5ms DropTail
$ns queue-limit $(n-2-0) $(n-1-0) 100
$ns duplex-link-op $(n-2-0) $(n-1-0) queuePos 0.5


puts "création des noeuds"
#créations des noeuds émetteurs
for { set i 1 } { $i <= $Num_transmitters } { incr i } {
	set (n-1-$i) [$ns node]
  $(n-1-$i) label "n-1-$i"
}
for { set i 1 } { $i <= $Num_receivers } { incr i } {
	set (n-2-$i) [$ns node]
  $(n-2-$i) label "n-2-$i"
}

#créations des liens clients - noeuds_bottleneck
for { set i 1 } { $i <= $Num_transmitters } { incr i } {
	$ns duplex-link $(n-1-0) $(n-1-$i) 5Mb 50ms DropTail
}


for {set j 1} { $j <= $Num_receivers } { incr j } {
		$ns duplex-link $(n-2-0) $(n-2-$j) 1Mb 10ms DropTail
}

set (transmit-1-1) [new Agent/TCP/Vegas]
$(transmit-1-1) set window_ 64
$(transmit-1-1) set packet_size_ 1500


#création des émetteurs TCP
for { set j 2 } { $j<= 3 } { incr j } {
    set (transmit-1-$j) [new Agent/TCP/Vegas]
    $(transmit-1-$j) set window_ 64
    $(transmit-1-$j) set packet_size_ 1500

}



puts "création des émetteurs TCP"
#création des récepteurs sink TCP
set (tcp_snk-1-1) [new Agent/TCPSink]
for { set j 2 } { $j<= $Num_transmitters } { incr j } {
  set (tcp_snk-1-$j) [new Agent/TCPSink]
}

puts "création des sinks TCP"


#Connections entre émetteurs-sinks TCP
for { set i 1 } { $i <=$Num_transmitters } { incr i } {
	$ns attach-agent $(n-1-$i) $(transmit-1-$i)
	$ns attach-agent $(n-2-$i) $(tcp_snk-1-$i)
	$ns connect $(transmit-1-$i) $(tcp_snk-1-$i)
}


proc record {transmit file} {
	global  Num_transmitters
	set ns_inst [Simulator instance]
	set time 0.1
	set cwnd [$transmit set cwnd_]
	set now [$ns_inst now]
	puts $file "$now [expr $cwnd ]"
	$ns_inst at [expr $now+$time] "record $transmit $file"
}

for { set i 1 } { $i <= $Num_transmitters } { incr i } {
	$ns at 0.1 "record $(transmit-1-$i) $(f-1-$i)"
}

for {set i 1} { $i<=$Num_transmitters } { incr i } {
	$ns at 0.0 "$(transmit-1-$i) send 40000000 "
 }
set file_d'att [$ns monitor-queue $(n-1-0) $(n-2-0)  [open f_a_droptail.tr w] 0.05]
[$ns link $(n-1-0) $(n-2-0)] queue-sample-timeout;


$ns at 50 "finish"
$ns run
