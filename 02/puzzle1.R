library(readtext)
script.dir <- dirname(sys.frame(1)$ofile)
data <- readtext(file.path(script.dir, "input.txt"))[1,2]
data_vec <- strsplit(data, "\n")[[1]]

data_vec <- strsplit(data_vec, 'x')
# data_vec will now be list of 1x3 character vectors

data_mat <- do.call(rbind, data_vec)
# this call converts list of 1000 vectors into a 1000x3 matrix
mode(data_mat) <- "integer"
# convert the matrix to integer type

sqFtNeeded <- function(dim_row){
  a <- dim_row[1]*dim_row[2]*2
  b <- dim_row[1]*dim_row[3]*2
  c <- dim_row[2]*dim_row[3]*2
  return( a + b + c +
         min(c(a, b, c)/2))
}

print(sum(apply(data_mat, 1, sqFtNeeded)))
# apply the function to each row (specified by 1) and print sum