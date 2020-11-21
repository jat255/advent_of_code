library(readtext)
library('plot.matrix')

script.dir <- dirname(sys.frame(1)$ofile)
data <- readtext(file.path(script.dir, "input.txt"))[1,2]
data_vec <- strsplit(data, "\n")[[1]]

lights <- matrix(FALSE, nrow=1000, ncol=1000)

for (instr in data_vec){
  words <- strsplit(instr, ' ')[[1]]
  # if length of words is 4, we toggle
  if (length(words) == 4){
    start <- strsplit(words[[2]], ',')
    start_x <- as.numeric(start[[1]][1])
    start_y <- as.numeric(start[[1]][2])
    
    end <- strsplit(words[[4]], ',')
    end_x <- as.numeric(end[[1]][1])
    end_y <- as.numeric(end[[1]][2])
    
    lights[start_x:end_x, start_y:end_y] <- !lights[start_x:end_x, start_y:end_y]
  } else if (words[[2]] == 'on'){
    # if second word is "on", we turn on  
    start <- strsplit(words[[3]], ',')
    start_x <- as.numeric(start[[1]][1])
    start_y <- as.numeric(start[[1]][2])
    
    end <- strsplit(words[[5]], ',')
    end_x <- as.numeric(end[[1]][1])
    end_y <- as.numeric(end[[1]][2])
    
    lights[start_x:end_x, start_y:end_y] <- TRUE
  } else {
    # otherwise we turn off 
    start <- strsplit(words[[3]], ',')
    start_x <- as.numeric(start[[1]][1])
    start_y <- as.numeric(start[[1]][2])
    
    end <- strsplit(words[[5]], ',')
    end_x <- as.numeric(end[[1]][1])
    end_y <- as.numeric(end[[1]][2])
    
    lights[start_x:end_x, start_y:end_y] <- FALSE
  }
}

par(mar=c(0, 0, 0, 0))
image(lights, useRaster=TRUE, axes=FALSE)
print(paste('Number of lights on is', sum(lights)))