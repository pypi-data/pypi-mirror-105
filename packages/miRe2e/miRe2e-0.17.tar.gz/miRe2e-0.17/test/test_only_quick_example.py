# Import the module
from miRe2e import MiRe2e

# Create an instance. Pre-trained weights are download by default. New model
# weights can be given as well (see source documentation)
model = MiRe2e()
filename = "examples/chr19_13836201_13836660_true.fasta"
scores_5_3, scores_3_5, index = model.predict(filename, batch_size=4096)
print(scores_5_3[:3])
print(index[:3])