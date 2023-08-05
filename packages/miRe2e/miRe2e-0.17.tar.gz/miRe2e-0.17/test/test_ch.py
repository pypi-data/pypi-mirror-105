from miRe2e import MiRe2e
import torch as tr
import numpy as np
import pickle
import pandas as pd
from miRe2e.get_error import get_error2d2

# Reproducibility --------------------------
tr.manual_seed(18)
tr.backends.cudnn.deterministic = True
tr.backends.cudnn.benchmark = False
np.random.seed(1)
# ------------------------------------------

# # check cuda predict on cpu
model = MiRe2e(device="cuda")

# completo
#test_fname = "/home/leandro/insync/miRe2e/src/data/chr19.fa"
#res = model.predict(test_fname)

# por partes
test_fname = "/home/leandro/insync/miRe2e/src/data/chr19_part1.fa"
pred_5_3, pred_3_5, ind = model.predict(test_fname)
print("Number of predictions", len(pred_5_3), len(pred_3_5), len(ind))

test_fname = "/home/leandro/insync/miRe2e/src/data/chr19_part2.fa"
pred_5_3_2, pred_3_5_2, ind_2 = model.predict(test_fname)
print("Number of predictions", len(pred_5_3_2), len(pred_3_5_2), len(ind_2))

# Reference file for ch19
ref = pd.read_csv("/home/leandro/insync/miRe2e/src/data/tag_chr19_all.csv")

ind = np.concatenate((ind, ind_2))
pred_5_3 = np.concatenate((pred_5_3, pred_5_3_2))
pred_3_5 = np.concatenate((pred_3_5, pred_3_5_2))

pickle.dump([pred_5_3, pred_3_5, ind], open("results_ch19_partes.pk", "wb"))
#pred_5_3, pred_3_5, ind = pickle.load(open("results_ch19_partes.pk", "rb"))



# Concatenate 5-3 and 3-5
idx = np.concatenate((ref["ind_5_3"], ref["ind_3_5"]))
ref = np.concatenate((ref["reference_5_3"], ref["reference_3_5"]))
pred = np.concatenate((pred_5_3, pred_3_5))

idx_pos = np.unique(idx[np.where(ref==1)])

# Account for overlapped windows with the same pre-mirna
del_pos = []
for j in idx_pos:
    pos = np.where(idx == j)[0]
    max_pos = pred[pos].max()
    max_id = pos[pred[pos].argmax()]
    pos = np.delete(pos, np.where(pos == max_id))
    del_pos = np.hstack((del_pos, pos))
del_pos = del_pos.astype(np.int64)
y_pred = np.delete(pred, del_pos)
y = np.delete(ref, del_pos)

start, step, end = 0.01, 0.01, 1.0
nn = int((end - start) / step)
th = np.hstack((np.linspace(start, end - step, nn),
                np.array([0.999, 0.9999, 0.99999, 0.999999,
                          0.9999995, 0.9999999])))
auroc, aucpr, f1max, premax, recmax, th, pre, rec = get_error2d2(y, y_pred, th,
                                                              testtime=False)

from matplotlib import pyplot as plt
import ipdb
ipdb.set_trace()

plt.plot(rec, pre)

