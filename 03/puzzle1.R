library(readtext)
library(tibble)
script.dir <- dirname(sys.frame(1)$ofile)
data <- readtext(file.path(script.dir, "input.txt"))[1,2]
data_vec <- strsplit(data, "")[[1]]

df <- tibble(x = 0, y = 0)

for (char in data_vec){
  cur_x <- tail(df, n=1)$x
  cur_y <- tail(df, n=1)$y
  if (char == '^') {
    cur_y <- cur_y + 1
  } else if (char == 'v') {
    cur_y <- cur_y - 1
  } else if (char == '>') {
    cur_x <- cur_x + 1
  } else {
    cur_x <- cur_x - 1
  }
  df <- df %>% add_row(x=cur_x, y=cur_y)
}

unique_pos <- unique(df)
print(nrow(unique_pos))