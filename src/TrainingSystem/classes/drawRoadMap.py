import matplotlib.pyplot as plt

class DrawRoadmap():
    def __init__(self, root, anchorsX, anchorsY, figInfo, idealInfo):
        self.savePath = root+"img/"+figInfo["ImgName"]
        # Roadmap label
        fig = plt.figure()
        plt.ylim(ymin = figInfo["yLim"][0])
        plt.ylim(ymax = figInfo["yLim"][1])
        fig.set_size_inches(figInfo["Width"], figInfo["Height"])
        plt.title(figInfo["Title"])
        plt.plot(anchorsX, anchorsY, 'o')
        # ax = plt.gca()  # X Y space
        # ax.xaxis.set_major_locator(MultipleLocator(100))
        # ax.yaxis.set_major_locator(MultipleLocator(100))
        ## purple line, can change
        plt.plot(idealInfo["X"], idealInfo["Y"], idealInfo["Color"], label=idealInfo["Label"])
    def add_anchor_text(anchorsX, anchorsY):
        plt.text(anchorsX[0]+10, anchorsY[0]+10, "An0094")
        plt.text(anchorsX[1]+10, anchorsY[1]+10, "An0095")
        plt.text(anchorsX[2]+10, anchorsY[2]+10, "An0096")
        plt.text(anchorsX[3]+10, anchorsY[3]+10, "An0099")
        return None

    def add_roadmap(self, X, Y, color, label, width=None):
        plt.plot(X, Y, color, label=label, linewidth= width)  # 紫色的線，可以隨便改
        return None

    def show_roadmap(self, save, show):
        plt.legend(loc="best")
        if save:
            plt.savefig(self.savePath)
        if show:
            plt.show()
        return None