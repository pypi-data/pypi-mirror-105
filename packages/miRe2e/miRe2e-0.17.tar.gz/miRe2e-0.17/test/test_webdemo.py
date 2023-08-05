from miRe2e import MiRe2e
from matplotlib import pyplot as plt


for model_name in ["animals", "hsa"]:
    for test_fname in ["examples/chr19_13836201_13836660_true.fa",
                       "examples/chr19_12003600_12004200_false.fa"]:

        model = MiRe2e(mfe_model_file=f"models-{model_name}/mfe.pkl",
                      predictor_model_file=f"models-"
                                           f"{model_name}/predictor.pkl",
                      structure_model_file=f"models-"
                                           f"{model_name}/structure.pkl")

        scores_5_3, scores_3_5, index = model.predict(test_fname)

        pos = [int(i.split("-")[1]) for i in index]  # use the start index to plot

        plt.figure(figsize=(15, 7))
        plt.subplot(2, 1, 1)
        plt.plot(pos, scores_5_3, "*-")
        plt.ylabel("pre-miRNA score")
        plt.title("5'-3'")

        plt.subplot(2, 1, 2)
        plt.plot(pos, scores_3_5, "*-")
        plt.title("3'-5'")

        plt.xlabel("Position [pb]")
        plt.ylabel("pre-miRNA score")
        plt.tight_layout()
        plt.suptitle(model_name + " " + test_fname)

plt.show()