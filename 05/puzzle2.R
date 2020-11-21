library(readtext)
script.dir <- dirname(sys.frame(1)$ofile)
data <- readtext(file.path(script.dir, "input.txt"))[1,2]
data_vec <- strsplit(data, "\n")[[1]]


isNice <- function(str){
  pairRepeat <- FALSE
  letterBracket <- FALSE
  
  for (i in seq(nchar(str))) {
    if (! pairRepeat){
      if (grepl(substr(str,i,i+1), substr(str,i+2,nchar(str)))){
        pairRepeat <- TRUE
        # print(paste('found pairRepeat', substr(str,i,i+1)))
      } 
    } 

    if (! letterBracket) {
      if (substr(str,i,i) == substr(str,i+2,i+2)){
        letterBracket <- TRUE
        # print(paste('found letterBracket', substr(str,i,i+2)))
      } 
    }
  }
  
  return( pairRepeat & letterBracket )
}

matches <- 0
for (str in data_vec){
  if (isNice(str)) matches <- matches + 1
}

print(matches)