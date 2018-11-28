# -*-coding:Utf-8 -*
import sys
import getopt

def initialiseTcl(fichier):
    fichier.write(
"""
set ns [new Simulator]
set nf [open out.nam w]
$ns namtrace-all $nf
"""
)

def finishProcedureTcl(fichier):
    fichier.write(
"""
proc finish {} {
        global ns nf
        $ns flush-trace
        #Close the NAM trace file
        close $nf
        #Execute NAM on the trace file
        exec nam -a out.nam &
        exit 0
}
"""
)
def createnodesTcl(fichier,n):
    fichier.write(
"""
for {set i 0} {$i<"""+str(n)+"""} {incr i} {
  set n($i) [$ns node]
}
"""
)

def create_p_clique_duplex_link(fichier,p):
    fichier.write(
"""
for {set i 0} {$i < """+str(p)+"""} {incr i} {
    for {set j 0} {$j < $i} {incr j} {
        $ns duplex-link $n($i) $n($j) 2mb 10ms DropTail
    }
}
"""
)

def create_star_duplexlinkTCL(fichier,firstnode,lastnode,center):
    fichier.write (
"""
for {set i """+str(firstnode)+"""} {$i <= """+str(lastnode)+"""} {incr i} {
    $ns duplex-link $n("""+str(center)+""") $n($i) 2Mb 10ms DropTail
}
"""
)

def create_Nudp_Cbr_agent(fichier,firstnode,lastnode):
    fichier.write (
"""
for {set i """+str(firstnode)+"""} {$i <= """+str(lastnode)+"""} {incr i} {
    set udp($i) [new Agent/UDP]
    $ns attach-agent $n($i) $udp($i)
    set cbr($i) [new Application/Traffic/CBR]
    $cbr($i) set packetSize_ 500
    $cbr($i) set interval_ 0.005
    $cbr($i) attach-agent $udp($i)
}
"""
)

def create_NUdp_Cbr_start_finish(fichier,firstnode,lastnode,starttime,finishtime):
    fichier.write(
"""
for {
    set i """+str(firstnode)+"""} {$i <= """+str(lastnode)+"""} {incr i} {
    $ns at """+str(starttime)+""" "$cbr($i) start"
    $ns at """+str(finishtime)+ """ "$cbr($i) stop"
}
"""
)


def finishtimeTCL(fichier,finishtime):
    fichier.write(
"""
$ns at """+str(5.0)+""" finish
"""
)

def runTCL(fichier):
    fichier.write(
"""
$ns run
"""
)
