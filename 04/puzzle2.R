library(digest)
input <- 'yzbqklnj'

i <- 0
while (TRUE){
  md5 <- digest(paste(input, i, sep=''), algo="md5", serialize=FALSE)
  if (substr(md5, 1, 6) == '000000') {
    print(paste(i, md5))
    break
  }
  i <- i + 1
}