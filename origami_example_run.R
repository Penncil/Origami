## This is the example code to run the origami function to create origami plor

source("origami_func.R")
library(fmsb)
library(plotrix)

#########################
######  data     ########
#########################
### ---------- Cluster 1 --------------
sample_data = read.csv("sample_data.csv")
colnames(sample_data)[c(2,4,6,8,10)] = ""
par(mfrow = c(1,1))
origami_func(sample_data,
            axistype=1 , 
            centerzero = TRUE,

            #custom polygon
            pcol=rgb(0.2,0.5,0.5,1),
            pfcol=rgb(0.2,0.5,0.5,0.1),
            plty = 1, # line type
            plwd= 2 ,

            #custom the grid
            cglcol="#000000",
            cglty=2,
            axislabcol="#808080",
            caxislabels=seq(0,1.2,by = 0.25),
            cglwd=0.1, 

            #custom labels
            vlcex=1.3,

            # point to mark
            full_point = NULL,
            point_col = rgb(186/255,6/255,80/255,0.9),
            point_pch = 17)





