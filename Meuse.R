library(rgdal)
library(dplyr)
library(sf)
library(ggplot2)
library(sf)
library(rvest)
library(viridis)
library(ggrepel)
library(ggthemes)
library(sp)


soildata<-read.csv("C:\\Users\\Lenovo\\Downloads\\meuse.csv")
merged_data<-merge(shapefile,soildata,by="NAME_1")

plot_field<-"zinc"
plot(soildata$zinc)
abline(soildata$zic~soildata$copper)
data<-plot(merged_data,col=merged_data[[plot_field]])

options(scipen = 999)
pl <- ggplot(shapefile)
pl <- pl + geom_sf(aes(fill  = merged_data$zinc), alpha = 0.7)
pl <- pl + geom_sf_text(aes(label = NAME_1), size = 2, color = "black")
pl <- pl + ggthemes::theme_map()
pl <- pl + theme(legend.position = "left")
pl <- pl + labs(title = "India zinc map")
pl <- pl + scale_fill_viridis(option="magma")
pl

options(scipen = 999)
pl <- ggplot(shapefile)
pl <- pl + geom_sf(aes(fill  = merged_data$copper), alpha = 0.7)
pl <- pl + geom_sf_text(aes(label = NAME_1), size = 2, color = "black")
pl <- pl + ggthemes::theme_map()
pl <- pl + theme(legend.position = "left")
pl <- pl + labs(title = "India Copper map")
pl <- pl + scale_fill_viridis(option="magma")
pl

options(scipen = 999)
pl <- ggplot(shapefile)
pl <- pl + geom_sf(aes(fill  = merged_data$cadmium), alpha = 0.7)
pl <- pl + geom_sf_text(aes(label = NAME_1), size = 2, color = "black")
pl <- pl + ggthemes::theme_map()
pl <- pl + theme(legend.position = "left")
pl <- pl + labs(title = "India cadmium concentration map")
pl <- pl + scale_fill_viridis(option="magma")
pl

library(gstat) # loads package gstat
library(sp) # loads package sp

#open the help manual for state package using the ? operator
?gstat
?sp

#Press ctrl+L to clear the console

# Next we will use dataset 'meuse' available in the sp package

data(meuse) # For more details refer Burrough and McDonnell 1998

#Remove meuse

remove(meuse)

# Relaod meuse

data(meuse)

#Explore data structure
class(meuse) #result is data-frame- basically means tabular data in row-column format

#See in Environment that meuse has 155 observations (i.e., rows) across 14 variables (i.e., columns)

#Now let's View meuse - careful! capital V; or you can simply click on meuse
View(meuse)

#Dataset contains x,y location information; 4 heavy metals along floodplains of a river; and some covariates. More details in Burrough and McDonnell 1998


#Examine the first few rows of the data - i.e., Preview
head(meuse)

#Examine the column names of of the data
colnames(meuse)

#What is the dimension of these data? That is, how many rows and columns in these data?
dim(meuse)
nrow(meuse)
ncol(meuse)
#So a data frame is like a matrix

#Examine individual values in the data frame - meuse 
meuse[1,1]
meuse[1,5] # Note : [] operator

#Examine values from a specific column
meuse[1,"zinc"]

#Examine a specific column
meuse$zinc
head(meuse$zinc) #Note the $ operator


# Examine the class of a specific column (Note : $ operator)
# Note that all items within a column have to be the same type
class(meuse$zinc)
class(meuse$landuse)
var(meuse$zinc)
sd(meuse$zinc)

#Plot a histogram of zinc concentrations
hist(meuse$zinc)

library(gstat)
library(sp)

data(meuse)
class(meuse)

#make a copy of meuse
meuse.sp <- meuse # Note: <- operator is an 'equals' operator

# We now want to convert the tabular data frame to a spatial data frame
# The way to do this is to use a command called "coordinates" - let's use Help to learn more

?coordinates

coordinates(meuse.sp) <- (~x+y) # objects that start with a '~' operator in R is called a 'formula'. i.e., ~ is R formula operator

# Examine the type of meuse.sp variable
class(meuse.sp)

# Compare the class of meuse.sp with meuse
class(meuse)


#Examine the first few rows of the meuse.sp data - i.e., Preview
head(meuse.sp)

#Examine the column names of of the data
colnames(meuse.sp@data) # Note: if you run colnames(meuse.sp) the result will be NULL. Specifically, you are examining the data within the spatial data frame

#What is the dimension of these data? That is, how many rows and columns in these data?
dim(meuse.sp) # Note: same result for dim(meuse.sp@data)
nrow(meuse.sp) # Note: same result for dim(meuse.sp@data)
ncol(meuse.sp) # Note: same result for dim(meuse.sp@data)

#Examine individual values in the spatial data frame - meuse.sp 
meuse.sp[1,1]
meuse.sp[1,5] 
meuse.sp[2,5] # Note : [] operator
bubble(meuse.sp, "zinc", 
       col = c("#00ff0070","#00ff0099"),
       main = "Zinc concentration in parts per million")
install.packages("cowplot")
library(cowplot)
plot_grid(
  ggplot(meuse, aes(y = zinc, x = elev)) + geom_point(),
  ggplot(meuse, aes(y = log(zinc), x = elev)) + geom_point(),
  nrow = 1, ncol = 2)

plot_grid(
  ggplot(meuse, aes(y = zinc, x = dist)) + geom_point(),
  ggplot(meuse, aes(y = log(zinc), x = dist)) + geom_point(),
  ggplot(meuse, aes(y = log(zinc), x = sqrt(dist))) + geom_point(),
  nrow = 1, ncol = 3)








library(sp)
library(gstat)
class(meuse)
names(meuse)
coordinates(meuse) = ~x+y
class(meuse)
summary(meuse)
var(soildata)
coordinates(meuse)[1:5,]
bubble(meuse,"zinc",col=c("#00ff0088", "#00ff0088"), 
       main ="zinc concentration")

vgm1 <- variogram(log(zinc)~1, meuse)
fit.variogram(vgm1, vgm(1, "Sph", 240, 1))
fit.variogram(vgm1, vgm("Sph"))
plot(vgm1,fit.variogram(vgm1, vgm("Sph")))

# optimize the value of kappa in a Matern model, using ugly <<- side effect:
f = function(x) attr(m.fit <<- fit.variogram(vgm1, vgm(,"Mat",nugget=NA,kappa=x)),"SSErr")
optimize(f, c(0.1, 5))
plot(vgm1, m.fit)
# best fit from the (0.3, 0.4, 0.5. ... , 5) sequence:
(m <- fit.variogram(vgm1, vgm("Mat"), fit.kappa = TRUE))
attr(m, "SSErr")



#install.packages("spgwr")
library(spgwr)
#calculate kernel bandwidth
GWRbandwidth <- gwr.sel(soilobs$zinc ~ soilobs$dist +
                          soilobs$elev, data=soilobs, adapt =TRUE)

gwr.model = gwr(soilobs$zinc ~ soilobs$dist+soilobs$elev,
                data = soilobs, adapt=GWRbandwidth, hatmatrix=TRUE, se.fit=TRUE)
#print the results of the model
gwr.model

results <-as.data.frame(gwr.model$SDF)
names(results)

gwr.map <- cbind(soilobs, as.matrix(results))
#The variable names followed by the name of our original dataframe (i.e. OA.Census.Unemployed) are the
#coefficients of the model.
install.packages("spacetime")
library(spacetime)
library(sp)
library(gstat)
library(ggplot2)
library(leaflet)
library(maptools)
plot(gwr.map, fill = "zinc",title="QWR map")+tm_layout(legend.text.size = 0.7,
                                                      legend.title.size = 1.1, legend.position = c("right", "bottom"), frame = FALSE)
library(gstat)
library(sp)
data(meuse)
coordinates(meuse)=~x+y
lzn.vgm = variogram(log(zinc)~1, data=meuse)
lzn.vgm
lzn.fit = fit.variogram(lzn.vgm, model = vgm(1, "Sph", 900, 1))
lzn.fit
plot(lzn.vgm,lzn.fit)
lznr.vgm = variogram(log(zinc)~sqrt(dist), meuse)
lznr.fit = fit.variogram(lznr.vgm, model = vgm(1, "Exp", 300, 1))
lznr.fit
plot(lznr.vgm,lznr.fit)
plot(variogramLine(vgm(1, "Mat", 1, kappa = 4), 10), type = 'l')
lzn.fit=fit.variogram(lzn.vgm,model=vgm("Lin", slope = 0.1, nugget = 0.5))
plot(lzn.vgm,lzn.fit)
v0 = variogram(zinc~1, meuse)
fit.variogram(v0, vgm(c("Exp", "Mat", "Sph")))


library(rgdal)
library(rgeos)

soil_data<-read.csv("C:\\Users\\Lenovo\\Downloads\\meuse.csv")
coordinates(soil_data) <- c("x", "y")
proj4string(soil_data) <- CRS("+init=epsg:28992")
Output_Area<- readOGR("C:\\Users\\Lenovo\\Downloads\\IND_adm\\IND_adm1.shp")
plot(Output_Area)
soilobs<-merge(Output_Area,soil_data,by.x="NAME_1",by.y="OBJECTID")
data<-plot(soilobs,col=soilobs[["zinc"]])
proj4string(soilobs) <- CRS("+init=epsg:28992")
library(tmap)
library(leaflet)
qtm(soilobs, fill = "zinc")
tm_shape(soilobs) + tm_fill("zinc")
library(RColorBrewer)
display.brewer.all()
# adds in layout, gets rid of frame
tm_shape(soilobs) + tm_fill("zinc", palette = "Reds",
                            style = "quantile", title = "Zinc concentration",n=5) +
  tm_borders(alpha=.4) +
  tm_compass() +
  tm_layout(legend.text.size = 0.7,
            legend.title.size = 1.1, legend.position = c("right", "bottom"), frame = TRUE)
# setting a colour palette
#tm_shape(soilobs) + tm_fill("zinc", palette = "-Greens")

# changing the intervals
#tm_shape(soilobs) + tm_fill("zinc", style = "quantile", palette = "Reds")
#tm_shape(soilobs) + tm_fill("zinc", style = "quantile", n = 7,
#                           palette = "Reds")
# includes a histogram in the legend
#tm_shape(soilobs) + tm_fill("zinc", style = "quantile", n = 5,
# palette = "Reds", legend.hist = TRUE)
# add borders


#spatial correlation
library(spdep)
#install.packages("spdep")
neighbours <- poly2nb(soilobs)
neighbours
plot(soilobs, border = 'lightgrey')
plot(neighbours, coordinates(soilobs), add=TRUE, col='red')

#geographical weighed regression
model <- lm(soilobs$zinc ~ soilobs$dist+soilobs$elev)
summary(model)

plot(model)
par(mfrow=c(2,2))
plot(model)

resids<-residuals(model)
map.resids <- cbind(soilobs, resids)
# we need to rename the column header from the resids file
# in this case its the 6th column of map.resids
names(map.resids)[6] <- "resids"
# maps the residuals using the quickmap function from tmap
library(tmap)
qtm(map.resids, fill = "resids")

#install.packages("spgwr")
library("spgwr")
#calculate kernel bandwidth
GWRbandwidth <- gwr.sel(soilobs$zinc ~ soilobs$dist +
                          soilobs$elev, data=soilobs, adapt =TRUE)

gwr.model = gwr(soilobs$zinc ~ soilobs$dist+soilobs$elev,
                data = soilobs, adapt=GWRbandwidth, hatmatrix=TRUE, se.fit=TRUE)
#print the results of the model
gwr.model

results <-as.data.frame(gwr.model$SDF)
names(results)

gwr.map <- cbind(soilobs, as.matrix(results))
#The variable names followed by the name of our original dataframe (i.e. OA.Census.Unemployed) are the
#coefficients of the model.
qtm(gwr.map, fill = "zinc",title="QWR map")+tm_layout(legend.text.size = 0.7,
                                                      legend.title.size = 1.1, legend.position = c("right", "bottom"), frame = FALSE)



library(sp)
library(raster)
library(gstat)
a<-read.csv("E://meuse.csv",header=TRUE)
plot(a$x,a$y)
hist(a$zinc)
l = seq(-3,3,by=0.25) # an array containing all lambdas I am going to test
d=array(data=a,dim=length(l)) # initialize d's (my metric for testing the quality of the transformation)

for (i in 1:length(l)) { # iterate through all elements i in l
  if (l[i] != 0) { # only in case l is not equal to 0
    tTF = (a$zinc^l[i]-1)/l[i] 
  } else { # if l is equal to zero -> log transform
    tTF = log(a$zinc) 
  }
  
  d[i] = (mean(a$zinc) - median(a$zinc))/IQR(a$zinc) # calculate the d for each transformed set
}
plot(l,d^2)
a$zinc = log(a$zinc)
hist(a$zinc)
par(mfrow = c(1,2))
plot(a$x,a$zinc)
plot(a$y,a$zinc)

library(geoR) 
a<-read.csv("E:\\meuse.csv",header=TRUE)
class(a)
View(a)
gtf = as.geodata(meuse, coords.col = 1:2, data.col=4) # translate the dataframe to a geodata object, use transformed tf
summary(gtf) # overview of the dataset
plot(gtf)






# Set the seed for reproducibility
set.seed(123)

# Split the data into 70% training and 30% testing
# Assuming you have a SpatialPointsDataFrame called soil_data
# train_indices is a vector of row indices for the training data

# Get the row names or IDs of the soil_data
row_names <- row.names(meuse)

# Subset the row names or IDs based on train_indices
train_row_names <- row_names[train_indices]

# Subset the training data
training_data <- meuse[train_row_names, ]

# Subset the testing data
testing_data <- meuse[!(row_names %in% train_row_names), ]
# Fit Ordinary Kriging model
ok_model <- gstat(formula = zinc ~ 1, data = training_data, model = vgm(1, "Sph", 100))

# Fit Universal Kriging model
uk_model <- gstat(formula = zinc ~ x + y, data = training_data, model = vgm(1, "Sph", 100))

# Predict using the OK model
ok_predictions <- predict(ok_model, testing_data)

# Predict using the UK model
uk_predictions <- predict(uk_model, testing_data)

# Assuming you have predicted values in ok_predictions and uk_predictions
# and testing_data is a SpatialPointsDataFrame with a column named "zinc"

ok_predictions <-  ok_predictions$var1.pred
plot(ok_predictions)

uk_predictions <- uk_predictions$var1.pred
plot(uk_predictions)

# Convert the predicted values to numeric
ok_predictions <- as.numeric(ok_predictions)
uk_predictions <- as.numeric(uk_predictions)

# Assuming you have ok_predictions and observed_values as numeric vectors

# Align the vectors by removing any excess elements
n <- min(length(ok_predictions), length(observed_values))
ok_predictions <- ok_predictions[1:n]
observed_values <- observed_values[1:n]

n <- min(length(uk_predictions), length(observed_values))
uk_predictions <- uk_predictions[1:n]
observed_values <- observed_values[1:n]


# Calculate the RMSE
ok_rmse <- sqrt(mean((ok_predictions - observed_values) ^ 2))
uk_rmse <- sqrt(mean((uk_predictions - observed_values) ^ 2))
coordinates(meuse.grid)<-~x+y

library(plyr)
library(dplyr)
library(gstat)
library(raster)
library(ggplot2)
install.packages("car")
library(car)
install.packages("classInt")
library(classInt)
install.packages("RStoolbox")
library(RStoolbox)
install.packages("spatstat")
library(spatstat)
install.packages("dismo")
library(dismo)
install.packages(c("fields","gridExtra"))
library(fields)
library(gridExtra)


UK<-krige(zinc~x+y, 
          loc=training_data, # Data frame
          newdata=meuse.grid,      # Prediction grid
          model = lzn.fit)       # fitted varigram model
summary(UK)
k1<-1/0.2523339                                   
UK$UK.pred <-((UK$var1.pred *0.2523339+1)^k1)
UK$UK.var <-((UK$var1.var *0.2523339+1)^k1)
summary(UK)
library(raster)
UK.pred<-rasterFromXYZ(as.data.frame(UK)[, c("x", "y", "UK.pred")])
UK.var<-rasterFromXYZ(as.data.frame(UK)[, c("x", "y", "UK.var")])
plot(UK.pred)
plot(UK.var)
library(ggplot2)
library(raster)
library(sp)
p1<-plot(UK.pred, geom_raster = TRUE,main="Universal kriging predictions") +
  scale_fill_gradientn("", colours = c("orange", "yellow", "green",  "sky blue","blue"))+
  theme_bw()+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        axis.title.y=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank())+
  ggtitle("UK Predicted SOC")+
  theme(plot.title = element_text(hjust = 0.5))

ggplot(data = meuse.grid) +
  geom_raster(aes(x = x, y = y, fill = uk.pred)) +
  scale_fill_gradient(low = "blue", high = "red") +
  labs(title = "Universal Kriging Predictions")

p2<-plot(UK.var,main="Universal kriging Variance",geom_raster = TRUE) +
  scale_fill_gradientn("", colours = c("blue",  "green","yellow", "orange"))+
  theme_bw()+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        axis.title.y=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank())+
  ggtitle("UK Predition Variance")+
  theme(plot.title = element_text(hjust = 0.5))

grid.arrange(p1, p2, ncol = 2)  # Multiplot 

# Print the RMSE
cat("OK RMSE:", ok_rmse, "\n")
cat("UK RMSE:", uk_rmse, "\n")

# Print the RMSE values
print(paste("OK RMSE:", ok_rmse))
print(paste("UK RMSE:", uk_rmse))





