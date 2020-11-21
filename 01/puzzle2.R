library(readtext)
script.dir <- dirname(sys.frame(1)$ofile)
data <- readtext(file.path(script.dir, "input.txt"))[1,2]

data_vec <- strsplit(data, "")[[1]]
floor <- 0
turns <- 0
for (char in data_vec){
  if (char == '('){
    floor <- floor + 1
  } else {
    floor <- floor - 1
  }
  turns <- turns + 1
  if (floor < 0){
    break
  }
}

print(c(floor, turns))