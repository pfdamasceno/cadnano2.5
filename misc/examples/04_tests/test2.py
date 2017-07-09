#REMOVE x-overs near the interface:
#1. Find non-circular staples (at surface)
#2. Calculate x-over distance
#  Create list of all x-overs
#  Iterate over them:
#       find their location (hasXoverAt)
#  Get opposite strand in the same vh
#      Find x-over for that strand (scaffold): idxs
#  IF x-overDist < x-overDistCutoff (21?):
#      delete x-over
#      reconnect staples


##############
# # Remove x-overs closer than 'dist' to the design's interface
# for staple in staple_oligos:
#     strand5p = staple.strand5p()
#     strand3p = strand5p.connection3p()
#     if strand3p: #is there a x-over ?
#         part.removeXover(strand5p, strand3p)

# OUTPUT
# p7560 = sequences['p7560']
# scaf_oligo.applySequence(p7560)
# doc.writeToFile('48hb_4.json')
#############

###################
# Naively break staples at xovers using greedy algorithm
min_split_len = 35  # break oligos longer than this
for staple in staple_oligos:
    unbroken_length = staple.length()
    strand_lengths = staple.getStrandLengths()
    split_idxs = []
    next_strand_len = 0
    num_bases_used = 0
    for nbases in strand_lengths:
        next_strand_len += nbases
        num_bases_used += nbases
        if min_split_len < next_strand_len and num_bases_used < unbroken_length:
            split_idxs.append(num_bases_used)
            next_strand_len = 0
    if split_idxs:
        staple.splitAtAbsoluteLengths(split_idxs)

p7560 = sequences['p7560']
scaf_oligo.applySequence(p7560)


doc.writeToFile('file_new.json')


oligos_sorted_by_length = sorted(oligos, key=lambda x: x.length(), reverse=True)

oligX = oligos_sorted_by_length[1]


oligos_sorted_by_length = sorted(oligos, key=lambda x: x.length(), reverse=True)

# non_circular_oligos are the difference between all oligos and those that are circular
circular_oligos = part.getCircularOligos()
non_circular_oligos = oligos.difference(circular_oligos)
non_circular_oligos_sorted_by_length = \
  sorted(non_circular_oligos, key=lambda x: x.length(), reverse=True)

# # Here we guess that the scaffold is simply the longest non-circular oligo
# longest_oligo = non_circular_oligos_sorted_by_length[0]
# staple_oligos = non_circular_oligos_sorted_by_length[1:]
