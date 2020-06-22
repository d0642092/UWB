import CalActualDis

time = 1
speed = 120
car = [100,100]
anchors = {"An0011": [0,0], "An0094": [50,50], "An0095": [50,-50], "An0096": [-50,-50], "An0099": [-50,50]}
direct = [0,-1]

for i in range(10):
    print(CalActualDis.calDis(time,speed,car,anchors,direct))