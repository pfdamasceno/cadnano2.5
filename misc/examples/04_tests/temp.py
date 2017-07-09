strand
strand.idx3Prime
strand.conne

######
# For each vh, make a list of x-overs
# Calculate their distance to scaffold beginning
# Loop over all x-overs and if dist < 21 b, remove them
# Reconnect open x-overs
#
#



#for a normal origami, staples are: fwd in even strands, rev for odd strands
# vh_id = 3
# is_scaffold = vh_id % 2
# scaffold_oligo = part.getStrandSets(vh_id)[is_scaffold]
# staple_oligo = part.getStrandSets(vh_id)[not(is_scaffold)]
# for strand in staple_oligo:
#     if strand.isForward():
#         if strand.hasXoverAt(strand.idx5Prime()): #test 4 x-over at 5' end
#             print ("fwd",strand,strand.idx5Prime())
#             #Calculate distance
#     else: #strand.isReverse():
#         if myStrand.hasXoverAt(myStrand.idx3Prime()):
#             print("rev",strand,strand.idx5Prime())
