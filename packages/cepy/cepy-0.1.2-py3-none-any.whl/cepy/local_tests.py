import sys
import doctest
sys.path.insert(1, '/media/data2/gidon_l/connect_embed/cepy_code/cepy')
import cepy as ce

doctest.testfile("ce.py")

doctest.testfile("embed_align.py")

#
# #Learn embeddings for a given connectome:
# import numpy as np
# import cepy as ce
# sc_group = ce.get_example('sc_group_matrix')
# ce_group = ce.CE(permutations=1, seed=1, num_walks=50)  # initiate the connectome embedding model
# ce_group.fit(sc_group)  # fit the model