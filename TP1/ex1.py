#!/usr/bin/env python
#coding: utf-8

import sys
import getopt
import creationTcl


#on ecrit le script Tcl automatisé dans ex1.tcl
fichier = open("ex1.tcl","w")

# initialise notre simulation
creationTcl.initialiseTcl(fichier)

#On écrit la procédure Finish
creationTcl.finishProcedureTcl(fichier)

#On crée 104 nodes
creationTcl.createnodesTcl(fichier,6)

#On crée les liens duplexes d'une clique de quatre noeuds(p=4)
creationTcl.create_p_clique_duplex_link(fichier,2)

#25 noeuds[4-28] attachés au node0
creationTcl.create_star_duplexlinkTCL(fichier,2,3,0)

#25 noeuds[29-53] attachés au node1
creationTcl.create_star_duplexlinkTCL(fichier,4,5,1)

#creation des agents udp sur tous les noeuds[4-103] sauf la 4-clique
creationTcl.create_Nudp_Cbr_agent(fichier,2,5)

# Scénario de début et de fin de génération des paquets par cbr0
creationTcl.create_NUdp_Cbr_start_finish(fichier,2,5,0.5,4.5)

#Finish time at 5.0s
creationTcl.finishtimeTCL(fichier,5.0)

creationTcl.runTCL(fichier)
