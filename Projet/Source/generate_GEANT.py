#!/usr/bin/python

from scipy.stats import zipf
import matplotlib.pyplot as plt
import scipy.special as sps
import numpy as np
from random import shuffle
import random as rand

#generer la topplogie a partir d'un fichier topology et ecrire le code tcl dans output
def generate_topology_GEANT(topology,output):
    #liste des noueds du reseau
    network = []
	#lire chaque ligne du fichier topologie
    for line in topology.readlines():
		network_cut = line.split ()
		if network_cut[0] not in network:
			network.append(network_cut[0])
			output.write("set (n%s) [$ns node]\n" %network_cut[0])
		if network_cut[1] not in network:
			network.append(network_cut[1])
			output.write("set (n%s) [$ns node]\n" %network_cut[1])

		#Creation des liens duplex, de TR/file d'attente DropTail,SFQ,RED...
		output.write("$ns duplex-link $(n%s) $(n%s) %sMb %sms RED\n"
					%(network_cut[0], network_cut[1], network_cut[2], network_cut[3]))
		#gestion des files d'attentes
		output.write("$ns queue-limit $(n%s) $(n%s) 1000\n" %(network_cut[0],network_cut[1]))
		output.write("$ns duplex-link-op $(n%s) $(n%s) queuePos 0.5\n" %(network_cut[0],network_cut[1]))

		#setting du monitor queue: Avoir les informations utiles concernant les queues, les pertes
		output.write("set (traceq-%s-%s) [open queues/queue-%s-%s.tr w]\n" %( network_cut[0], network_cut[1],network_cut[0], network_cut[1]))
		output.write("set (queue-%s-%s) [$ns monitor-queue $(n%s) $(n%s)  $(traceq-%s-%s) 0.1]\n" %(network_cut[0], network_cut[1],network_cut[0], network_cut[1],network_cut[0], network_cut[1]))
		output.write("[$ns link $(n%s) $(n%s)] queue-sample-timeout\n" %(network_cut[0], network_cut[1]))

def stress_traffic_GEANT(traffic,output,ON,OFF,shape,nbr_flows_maxi):
    output.write("Agent/TCP set packetSize_ 1500\n")
    output.write("Agent/TCP set windowSize_ 75\n")
    output.write("Agent/UDP set packetSize_ 1500\n")

    for line in traffic.readlines():
        trafic_cut = line.split()
        Quantity = int(trafic_cut[2])

        rate = Quantity*0.8/300

        output.write("set (sudp%s-%s) [new Agent/UDP]\n" %(trafic_cut[0], trafic_cut[1]))
        output.write("$ns attach-agent $(n%s) $(sudp%s-%s)\n" %(trafic_cut[1], trafic_cut[0], trafic_cut[1]))
        output.write("set (udp%s-%s) [new Agent/UDP]\n" %(trafic_cut[0], trafic_cut[1]))
        output.write("$ns attach-agent $(n%s) $(udp%s-%s)\n" %(trafic_cut[0], trafic_cut[0], trafic_cut[1]))
        output.write("$ns connect $(udp%s-%s) $(sudp%s-%s)\n" %(trafic_cut[0], trafic_cut[1], trafic_cut[0], trafic_cut[1]))

        output.write("set (par%s-%s) [new Application/Traffic/Pareto]\n" %(trafic_cut[0], trafic_cut[1]))
        output.write("$(par%s-%s) set packetSize_ 1500\n" %(trafic_cut[0], trafic_cut[1]))
        output.write("$(par%s-%s) set burst_time_ %sms\n" %(trafic_cut[0], trafic_cut[1], ON))
        output.write("$(par%s-%s) set idle_time_ %sms\n" %(trafic_cut[0], trafic_cut[1], OFF))
        output.write("$(par%s-%s) set shape_ %s\n" %(trafic_cut[0], trafic_cut[1], shape))
        output.write("$(par%s-%s) set rate_ %s\n" %(trafic_cut[0], trafic_cut[1],rate))
        output.write("$(par%s-%s) attach-agent $(udp%s-%s)\n" %(trafic_cut[0], trafic_cut[1], trafic_cut[0], trafic_cut[1]))
        output.write("$ns at 0 \"$(par%s-%s) start\"\n" %(trafic_cut[0], trafic_cut[1]))
        output.write("$ns at 300 \"$(par%s-%s) stop\"\n\n" %(trafic_cut[0], trafic_cut[1]))


        #fichiers de trace de la cwnd et de la bw
    	#output.write("set (g-%s-%s) [open sinks/sink-%s-%s.tr w]\n"%(trafic_cut[0], trafic_cut[1],trafic_cut[0], trafic_cut[1]))
    	output.write("set (f-%s-%s) [open outs/flux_%s_%s.tr w]\n" %(trafic_cut[0], trafic_cut[1],trafic_cut[0], trafic_cut[1]))

        flows_TCP_Quantity = Quantity*10*0.2

        Zipf = Zipf_subdivision_to_flows(flows_TCP_Quantity,shape,nbr_flows_maxi,15000)
        shuffle(Zipf)
        nbr_flows = len(Zipf)
        #print(Zipf[0])



        for i in range(nbr_flows) :

            inst = int(rand.uniform(50,250))

            output.write("set (tcp%s-%s-%s) [new Agent/TCP]\n" %(trafic_cut[0], trafic_cut[1], i))
            output.write("$ns attach-agent $(n%s) $(tcp%s-%s-%s)\n" %(trafic_cut[0], trafic_cut[0], trafic_cut[1], i))
            output.write("set (stcp%s-%s-%s) [new Agent/TCPSink]\n" %(trafic_cut[0], trafic_cut[1], i))
            output.write("$ns attach-agent $(n%s) $(stcp%s-%s-%s)\n" %(trafic_cut[1], trafic_cut[0], trafic_cut[1], i))
            output.write("$ns connect $(tcp%s-%s-%s) $(stcp%s-%s-%s)\n" %(trafic_cut[0], trafic_cut[1], i, trafic_cut[0], trafic_cut[1], i))
            output.write("$ns at %s \"$(tcp%s-%s-%s) send %s\"\n\n" %(inst, trafic_cut[0], trafic_cut[1], i, Zipf[i]))

            #output.write("set (f-%s-%s-%s) [open outs/flux_%s_%s-%s.tr w]\n" %(trafic_cut[0], trafic_cut[1],i,trafic_cut[0], trafic_cut[1],i))

        output.write("$ns at 0 \"record $(tcp%s-%s-0) $(f-%s-%s) \"\n" %(trafic_cut[0], trafic_cut[1],trafic_cut[0], trafic_cut[1]))

def Zipf_subdivision_to_flows(quantity,shape,nbr_flows_max,Xmin):
    flows = []
    i=0
    z=0
    nbr_flows = 0
    nbr_flows = int(rand.uniform(nbr_flows_max/2,nbr_flows_max))
    while(len(flows) < nbr_flows):
        z=zipf.rvs(shape)
        if z < nbr_flows:
            flows.append(z)
        i=i+1
    (nbrs, intervals) = np.histogram(flows,bins=nbr_flows)

    flows = []
    for l in nbrs:
        if l*int(quantity/(nbr_flows))+1 < Xmin:
            flows.append(Xmin)
        else:
            flows.append(l*int(quantity/(nbr_flows))+1)

    i=0
    total=0
    #fd = open(str(quantity)+".txt", "w")
    for i in range(nbr_flows):
        total = total + flows[i]
        #fd.write("%s %s\n" %(i,flows[i]))
    flows[0]= flows[0]-(total-quantity)
    return flows




topology =  open("topo.top","r")
traffic  =  open("traff.traf","r")
output   =  open("GEANT.tcl","w")


output.write("set ns [new Simulator]\n")
output.write("set f1 [open traceall.tr w]\n")
output.write("$ns trace-all $f1\n")

output.write("set loss [open losses.tr w]\n\n")



output.write("proc finish {} {\n")
output.write("    global ns loss f1\n")
output.write("    $ns flush-trace\n")
#output.write("    close $loss\n")
output.write("    close $f1\n")
output.write("    exit 0\n")
output.write("}\n\n")

"""
output.write("Node instproc getidnode {} {\n")
output.write("\t$self instvar id_\n    return \"$id_\"\n}\n\n")

output.write("proc record {i j} {\n")
output.write("\tglobal ns n monitor_queue loss\n")
output.write("\tset now [$ns now]\n")
output.write("\tset from_node [$(n$i) getidnode]\n")
output.write("\tset to_node [$(n$j) getidnode]\n")
output.write("\tset lossi-j [$(monitor_queue$i-$j) set pdrops_]\n")
output.write("\tset lossj-i [$(monitor_queue$j-$i) set pdrops_]\n")
output.write("\tset departurei-j [$(monitor_queue$i-$j) set pdepartures_]\n")
output.write("\tset departurej-i [$(monitor_queue$j-$i) set pdepartures_]\n")
output.write("\tputs $loss \"$i $j [expr $lossi-j + $lossj-i2] [expr $departurei-j + $departurej-i]\"\n")
output.write("}\n\n")
"""

generate_topology_GEANT(topology,output)

stress_traffic_GEANT(traffic,output,500,500,1.01,300)

#fonction record enregistrement de la bandwidth et de la cwnd
output.write("proc record {tcp_src  file_src } { \n")
output.write("\tset ns_inst [Simulator instance] \n")
output.write("\tset time 0.1\n")
output.write("\tset cwnd [$tcp_src set cwnd_]\n")
#output.write("\tset bw [$tcp_snk set bytes_]\n")
output.write("\tset now [$ns_inst now]\n")
output.write("\tputs $file_src \"$now [expr $cwnd ]\"\n")
#output.write("\tputs $file_snk \"$now [expr $bw ]\"\n")
output.write("\t$ns_inst at [expr $now+$time] \"record $tcp_src $file_src \"\n")
output.write("}\n")



output.write("$ns at 300 \"finish\"\n")
output.write("$ns run\n")

#print Zipf_subdivision_to_flows(1250491,1.01,300,15)

topology.close()
traffic.close()
output.close()
