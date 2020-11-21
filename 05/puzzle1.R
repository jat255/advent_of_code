library(readtext)
script.dir <- dirname(sys.frame(1)$ofile)
data <- readtext(file.path(script.dir, "input.txt"))[1,2]
data_vec <- strsplit(data, "\n")[[1]]


isNice <- function(str){
  letters <- strsplit(str, "")[[1]]
  threeVowels <- FALSE
  doubleLetter <- FALSE
  
  vowels <- 0
  for (i in seq(nchar(str))) {
    if (substr(str,i,i) %in% c("a","e","i","o","u")) vowels <- vowels + 1
    if (doubleLetter | substr(str,i,i) == substr(str,i+1,i+1)){
      doubleLetter <- TRUE
    }
  }
  if (vowels > 2) threeVowels <- TRUE
  
  badLetters <- FALSE
  for (s in c('ab', 'cd', 'pq', 'xy')){
    if (grepl(s, str, fixed=TRUE)){
      badLetters <- TRUE
      break
    }
  }
  
  return( threeVowels & doubleLetter & ! badLetters )
}

matches <- 0
for (str in data_vec){
  if (isNice(str)) matches <- matches + 1
}

print(matches)