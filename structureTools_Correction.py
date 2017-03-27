#!/usr/bin/env python

import math, string





def computeDist_dico(d_res1, d_res2, mode = "atom") :
    """res1, res2 are dico corresponding to residue 1 and residue 2 respectively """

    if mode == "atom" :
        minval = 1000000
        for atom1 in d_res1["atomlist"] :
            coord1 = [d_res1[atom1]["x"], d_res1[atom1]["y"], d_res1[atom1]["z"]]
            for atom2 in d_res2["atomlist"] :
                coord2 = [d_res2[atom2]["x"], d_res2[atom2]["y"], d_res2[atom2]["z"]]
                dist = distancePoints((coord1[0], coord1[1], coord1[2]),(coord2[0],coord2[1], coord2[2]))
                if minval > dist :
                    minval = dist

    elif mode == "center" : # computes the distance between the CM of the 2 given residues
        dPDBtmp = {}
        dPDBtmp["reslist"] = ["res1", "res2"]
        dPDBtmp["res1"] = d_res1
        dPDBtmp["res2"] = d_res2

        centerMassOfResidue(dPDBtmp)
        minval = distancePoints((dPDBtmp["res1"]["XCM"],dPDBtmp["res1"]["YCM"],dPDBtmp["res1"]["ZCM"]),(dPDBtmp["res2"]["XCM"],dPDBtmp["res2"]["YCM"],dPDBtmp["res2"]["ZCM"]))
        
    return minval


def extractContactResidues(matdist, seuil) :
    """from a distance matrix (matdist), returns pairs of residues in contacts (seuil) in a list of lists """

    contacts = []
    for i in range(len(matdist[0])) :
        for j in range (i+1, len(matdist[0])) :
            if matdist[i][j] <= seuil :
                      contacts.append([i, j])

    return contacts






def distancePoints((x1,y1,z1),(x2,y2,z2)):
    """Computes the distance between the two sets of coordinates
       input: 2 tuples with the corresponding coordinates 
       output: distance"""

    x = (x1-x2)
    y = (y1-y2)
    z = (z1-z2)
    return math.sqrt(x*x+y*y+z*z)



def centerMassOfResidue(dPDB, all = True, reslist = False):
    """Calculates the center of mass of each residue contained in dPDB (all = True & reslist = False) or a 
       subset of residues given in the residue list (["12_A", "13_A", "27_A"])"""

    if all == True :
        reslist = dPDB["reslist"]
    
        
    for res in reslist :        
        x = y = z = 0.0
        
        # looping over the current residue atoms
        for atom in dPDB[res]["atomlist"] :
            x +=dPDB[res][atom]["x"]
            y +=dPDB[res][atom]["y"]
            z +=dPDB[res][atom]["z"]
            
        Xcm = float(x)/len(dPDB[res]["atomlist"]) 
        Ycm = float(y)/len(dPDB[res]["atomlist"])
        Zcm = float(z)/len(dPDB[res]["atomlist"])
        dPDB[res]["XCM"] = Xcm
        dPDB[res]["YCM"] = Ycm
        dPDB[res]["ZCM"] = Zcm
        


def parsePDBMultiChains(infile) :

    # lecture du fichier PDB 
    f = open(infile, "r")
    lines = f.readlines()
    f.close()


    # var init
    chaine = True
    firstline = True
    prevres = None
    dPDB = {}
    dPDB["reslist"] = []
    dPDB["chains"] = []
    
    # parcoure le PDB   
    for line in lines :
        if line[0:4] == "ATOM" :
            chain = line[21]
            if not chain in dPDB["chains"] :
                dPDB["chains"].append(chain)
                dPDB[chain] = {}
                dPDB[chain]["reslist"] = []
            curres = "%s"%(line[22:26]).strip()
            if not curres in dPDB[chain]["reslist"] :
                dPDB[chain]["reslist"].append(curres)
                dPDB[chain][curres] = {}
                dPDB[chain][curres]["resname"] = string.strip(line[17:20])
                dPDB[chain][curres]["atomlist"] = []
            atomtype = string.strip(line[12:16])
            dPDB[chain][curres]["atomlist"].append(atomtype)
            dPDB[chain][curres][atomtype] = {}
            #print "cures ", curres
            #print dPDB[chain][curres]
 
            dPDB[chain][curres][atomtype]["x"] = float(line[30:38])
            dPDB[chain][curres][atomtype]["y"] = float(line[38:46])
            dPDB[chain][curres][atomtype]["z"] = float(line[46:54])
            dPDB[chain][curres][atomtype]["id"] = line[6:11].strip()

    return dPDB

