library(readtext)
script.dir <- dirname(sys.frame(1)$ofile)
data <- readtext(file.path(script.dir, "input.txt"))[1,2]

data_vec <- strsplit(data, "")[[1]]
start <- 0
for (char in data_vec){
  if (char == '('){
    start <- start + 1
  } else {
    start <- start - 1
  }
}

print(start)