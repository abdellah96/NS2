#creation de l'objet simulator
set ns [new Simulator]


set num_transmitters 3
set num_receivers 3

#ouvrir le fichier de trace global
#set outputfile [open out.tr w]
#$ns trace-all $outputfile

#ouvrir le fichier de trace nam
set nf [open out.nam w]
$ns namtrace-all $nf


proc finish {} {
    global ns nf
	  $ns flush-trace
    #fermeture de fichiers de trace
    close $nf
    #close $outputfile
    #ececuter nam en fonction de la trace
    puts "nam se lance....."
    exec nam -a out.nam &
    exit 0
}

#creation des noeud emetteurs (bottle)
for {set i 1} {$i<=$num_transmitters} {incr i} {
  set n(b-$i) [$ns node]
}
#creation des noeud recepteurs (neck)
for {set i 1} {$i<=$num_receivers} {incr i} {
  set n(n-$i) [$ns node]
}
#creation des deux neuds de goulet d’étranglement
set nb [$ns node]
set nn [$ns node]

#creation des liens duplex emetteurs
for {set i 1} {$i<=$num_transmitters} {incr i} {
  $ns duplex-link $n(b-$i) $nb 100Mb 0.1ms DropTail
}
#creation des liens duplex recepteurs
for {set i 1} {$i<=$num_receivers} {incr i} {
  $ns duplex-link $n(n-$i) $nn 100Mb 0.1ms DropTail
}
#creation de lien de coeur
$ns duplex-link $nb $nn 100Mb 0.1ms DropTail
$ns duplex-link-op $nn $nb queuePos0.5

#definir les positions

$ns duplex-link-op $nb $n(b-1) orient left-down
$ns duplex-link-op $nb $n(b-2) orient left
$ns duplex-link-op $nb $n(b-3) orient left-up
$ns duplex-link-op $nn $n(n-1) orient right-down
$ns duplex-link-op $nn $n(n-2) orient right
$ns duplex-link-op $nn $n(n-3) orient right-up

#creation des agents TCP(TCPSink) / Couche transport
set tcp [new Agent/TCP]
set sink [new Agent/TCPSink]
for {set i 1} {$i<=$num_transmitters} {incr i} {
  $ns attach-agent $n(b-$i) $tcp
}
for {set i 1} {$i<=$num_receivers} {incr i} {
  $ns attach-agent $n(n-$i) $sink
}
#creation de FTP /couche applicative
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP

$ns connect $tcp $sink

$ns at 50 "finish"
$ns run
