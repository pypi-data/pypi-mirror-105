from miRe2e import MiRe2e
import torch as tr
import numpy as np

# # check cuda predict on cpu
print("model with hsa")
model = MiRe2e()
test_fname = "examples/chr19_13836201_13836660_true.fa"
model.predict(test_fname)

# check cuda predict on gpu
model = MiRe2e(device="cuda")
model.predict(test_fname)

# check loading
print("model with animals")
model = MiRe2e(device="cuda", pretrained="animals")
print("no pretrain")
model = MiRe2e(device="cuda", pretrained="no")


