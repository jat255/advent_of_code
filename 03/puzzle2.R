library(readtext)
library(tibble)
script.dir <- dirname(sys.frame(1)$ofile)
data <- readtext(file.path(script.dir, "input.txt"))[1,2]
data_vec <- strsplit(data, "")[[1]]

df <- tibble(x = 0, y = 0)

santa_x <- 0
santa_y <- 0
robo_x <- 0
robo_y <- 0
turn <- 1

for (char in data_vec){
  if (turn %% 2 == 1) {
    if (char == '^') {
      santa_y <- santa_y + 1
    } else if (char == 'v') {
      santa_y <- santa_y - 1
    } else if (char == '>') {
      santa_x <- santa_x + 1
    } else {
      santa_x <- santa_x - 1
    }  
    df <- df %>% add_row(x=santa_x, y=santa_y)
    
  } else {
    if (char == '^') {
      robo_y <- robo_y + 1
    } else if (char == 'v') {
      robo_y <- robo_y - 1
    } else if (char == '>') {
      robo_x <- robo_x + 1
    } else {
      robo_x <- robo_x - 1
    }  
    df <- df %>% add_row(x=robo_x, y=robo_y)
  }
  turn <- turn + 1
}

unique_pos <- unique(df)
print(nrow(unique_pos))