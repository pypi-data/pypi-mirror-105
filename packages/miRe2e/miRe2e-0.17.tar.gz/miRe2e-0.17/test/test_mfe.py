from miRe2e import MiRe2e
import torch as tr
import numpy as np
import pickle

# Reproducibility --------------------------
tr.manual_seed(18)
tr.backends.cudnn.deterministic = True
tr.backends.cudnn.benchmark = False
np.random.seed(1)
# ------------------------------------------

# # check cuda predict on cpu
model = MiRe2e(device="cuda")

fname_mfe = "/home/leandro/insync/miRe2e/src/data" \
            "/training_mfe_structure/mfe_seqs.fa"

model.fit_mfe(fname_mfe, batch_size=4092)