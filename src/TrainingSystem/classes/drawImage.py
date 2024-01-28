import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
class DrawImage():
    def init_image(index, imageTitle):
        fig = plt.figure(figsize=(10, 10))
        plt.subplots_adjust(hspace=0.4, wspace=0.3)
        plt.suptitle(imageTitle[index], fontsize=14)
        w = 13.66
        h = 6.71
        fig.set_size_inches(w, h)
        return 221

    def subimage_create(position, title, staticX, staticY, xSort ,staticPredict):
        # image create
        plt.subplot(position)
        ax = plt.gca() # X Y space
        ax.xaxis.set_major_locator(MultipleLocator(100))
        ax.yaxis.set_major_locator(MultipleLocator(100))

        plt.xticks(fontsize=7)
        plt.yticks(fontsize=7)
        plt.title(title)
        plt.xlabel("Measure Value (cm)")
        plt.ylabel("Actual Value (cm)")
        plt.scatter(staticX, staticY, s=20, color="red")
        plt.plot(xSort, staticPredict["linear"], "c", label="Linear",linewidth = 1)
        plt.plot(xSort, staticPredict["ridge"], "b", label="Ridge",linewidth = 1)
        plt.plot(xSort, staticPredict["lasso"], "y", label="Lasso",linewidth = 1)
        # plt.plot(xSort, staticPredict["svr"], "m", label="SVR", linewidth=1)
        plt.legend(loc="best")

    def save_and_show(imgPath, imgName):
        plt.show()
        plt.savefig(imgPath + imgName)
