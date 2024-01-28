rm(list=ls())
library(readxl)
p2<-read_excel("D:\\Code\\Python\\UWB_IEEE\\Data\\2020-09-08_東門\\outdoor_static_5m.xlsx",sheet="Point2")
p5<-read_excel("D:\\Code\\Python\\UWB_IEEE\\Data\\2020-09-08_東門\\outdoor_static_5m.xlsx",sheet="Point5")
p2<-p2[c(-1,-2,-3)]
p5<-p5[c(-1,-2,-3)]
# 2 5 10 13 <- 412.3

range<-cbind(p2[c(1,4)],p5[c(7,10)])
range<-range[-1,]
range

An94<-range$An0094
An95<-range$An0095
An96<-range$An0096
An99<-range$An0099

An94<-as.numeric(An94)
An95<-as.numeric(An95)
An96<-as.numeric(An96)
An99<-as.numeric(An99)


t94<-table(An94)
t95<-table(An95)
t96<-table(An96)
t99<-table(An99)
t94
t95
t96
t99
t94<-t94[-1]
t95<-t95[-1]
t96<-t96[-1]
t99<-t99[-1]


par(mfrow=c(2,2),oma=c(3,0,2,0)) # oma = c(up,right,down,left)
barplot(t94,main = "Anchor 1",col="gray",xlab = "Distance(cm)",border = "black",cex.main=1.0)
abline(v=3,lty=2,col="red",lwd=2)
text(4.2,15,"Actual",col="red")
text(4.2,13,"412cm",col="blue")
barplot(t95,main = "Anchor 2",col="gray",xlab = "Distance(cm)",border = "black",cex.main=1.0,xlim=c(-1,length(t95)+1))
abline(v=-1,lty=2,col="red",lwd=2)
text(0.2,17,"Actual",col="red")
text(0.2,14.5,"412cm",col="blue")
barplot(t96,main = "Anchor 3",col="gray",xlab = "Distance(cm)",border = "black",cex.main=1.0,ylim=c(0,28))
abline(v=6.5,lty=2,col="red",lwd=2)
text(7.5,25,"Actual",col="red")
text(7.5,22.5,"412cm",col="blue")
barplot(t99,main = "Anchor 4",col="gray",xlab = "Distance(cm)",border = "black",cex.main=1.0,xlim=c(-1,length(t99)))
abline(v=-1,lty=2,col="red",lwd=2)
text(1.2,15,"Actual",col="red")
text(1.2,13,"412cm",col="blue")
mtext("Data measurement in parking lot", outer = TRUE, cex = 1.5)

