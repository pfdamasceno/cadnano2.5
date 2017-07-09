#!/usr/bin/env python3
# export_legacy_json.py
# Pablo F. Damasceno, 2017-07-05
# modified from SD example
# BSD-3 open-source license

# This code assumes your scaffold is the longest non-circular staple !!

import argparse
from datetime import datetime
from os import path
import sys
import cadnano
from cadnano.document import Document
from cadnano.data.dnasequences import sequences

# User input choices
xover_buffer_length = 7 #number of bases from the interface before start xovers

# Read design
app = cadnano.app()
doc = app.document = Document()
doc.readFile('48hb.json');
part = doc.activePart()

vhs_list = list(part.getIdNums())  # convert set to list of vhs

for vh_id in vhs_list:
    # for each strandSet, we have both scaffold and staple
    # for traditional origami, scaffold is fwd for even vh
    is_scaffold = vh_id % 2
    scaffold_strandSet = part.getStrandSets(vh_id)[is_scaffold]
    staple_strandSet = part.getStrandSets(vh_id)[not(is_scaffold)]
    scaffold_interfaces = (scaffold_strandSet.indexOfLeftmostNonemptyBase(),\
                           scaffold_strandSet.indexOfRightmostNonemptyBase())

    # remove xovers that are within 'xover_buffer_length' from interface
    for strand in staple_strandSet:
        if strand.hasXoverAt(strand.idx5Prime()): #test 4 x-over at 5' end
            xover_to_interf_dist = (strand.idx5Prime() - scaffold_interfaces[0],\
                                  - strand.idx5Prime() + scaffold_interfaces[1])
            if xover_to_interf_dist[0] < xover_buffer_length or \
               xover_to_interf_dist[1] < xover_buffer_length:
                # temp_list.append(strand.idx5Prime())
                if is_scaffold:
                    part.removeXover(strand.connectionLow(),strand)
                else:
                    part.removeXover(strand.connectionHigh(),strand)
        if strand.hasXoverAt(strand.idx3Prime()):
            xover_to_interf_dist = (strand.idx3Prime() - scaffold_interfaces[0],\
                                  - strand.idx3Prime() + scaffold_interfaces[1])
            if xover_to_interf_dist[0] < xover_buffer_length or \
               xover_to_interf_dist[1] < xover_buffer_length:
                if is_scaffold:
                    part.removeXover(strand,strand.connectionHigh())
                else:
                    part.removeXover(strand,strand.connectionLow())

    # now combine oligos that were broken from xover removal
    oldStrand = strand
    for strand in staple_strandSet:
        strand.merge(strand.idx5Prime())
    while oldStrand != strand: #repeat the strand merge until it cant be done
        oldStrand = strand
        for strand in staple_strandSet:
            strand.merge(strand.idx5Prime())

# do one last pass to ensure oligos are properly connected
for vh_id in vhs_list:
    is_scaffold = vh_id % 2
    scaffold_strandSet = part.getStrandSets(vh_id)[is_scaffold]
    staple_strandSet = part.getStrandSets(vh_id)[not(is_scaffold)]
    for strand in staple_strandSet:
        strand.merge(strand.idx5Prime())


doc.writeToFile('48hb_1.json')
