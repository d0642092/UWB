from turtle import *

x = 546
y = 248
A_offset = 200
B_offset = 400

name = ['anchor94','anchor95','anchor96','anchor99']
colors = ['red','blue','purple','green']
anchorPositions = [[0,0],[0,y],[x,0],[x,y]]
staticPoints = [[x + A_offset , -y],[x + A_offset , 0],[x + A_offset , y],[x + A_offset , 2*y],
                [x + B_offset , 2*y],[x + B_offset , y],[x + B_offset , 0],[x + B_offset , -y],
                [x , -y],[x , 2*y]]
staticPointsName = []
for i in range(1,11):
    staticPointsName.append("staticP_" + str(i))
print(staticPoints)


setworldcoordinates(-200,-500,1350,700)
penup()
right(90)
for i,point in enumerate(anchorPositions):
    color(colors[i])
    goto(point)
    stamp()
    forward(30)
    write(name[i], font=("Arial", 16, "normal"))

for i,point in enumerate(staticPoints):
    color('grey')
    goto(point)
    stamp()
    forward(30)
    write(staticPointsName[i],font=("Arial", 16, "normal"))

hideturtle()
done()


