library(readtext)
library(stringr)
# script.dir <- dirname(sys.frame(1)$ofile)
data <- readtext("07/input.txt")[1,2]
instructions <- strsplit(data, "\n")[[1]]

wires <- list()
inst_list <- vector("list", length(instructions))

# process instructions into standardized list:
for (i in seq_along(instructions)) {
  d <- instructions[[i]]
  split_instr <- lapply(strsplit(d, '->'), str_trim)
  dest <- split_instr[[1]][length(split_instr[[1]])]
  inst <- strsplit(split_instr[[1]][1], ' ')[[1]]
  # print(inst)
  
  if ('NOT' %in% inst){
    inst_list[[i]] <- c(inp1=inst[2], op=inst[1], dest=dest)
  } else if ('AND' %in% inst | 'OR' %in% inst | 
             'LSHIFT' %in% inst | 'RSHIFT' %in% inst) {
    inst_list[[i]] <- c(inp1=inst[1], inp2=inst[3], op=inst[2], dest=dest)
  } else {
    inst_list[[i]] <- c(inp1=inst[1], op='EMIT', dest=dest)
  }
}

#' process a command from the instruction list
#' 
#' @param inst A named character vector with names "inp1", "op", 
#'             "dest", and (optionally) "inp2".
#'             "inp1" and "inp2" will be characters, representing
#'             either a position in wires, or a number
processInstruction <- function (inst){
  # convert inp1 and inp2 to numbers, fetching
  # their values from `wires`, as needed:
  if ( !is.na(as.numeric(inst['inp1'])) ) {
    inp1 <- as.numeric(inst['inp1'])
  } else {
    inp1 <- as.numeric(wires[inst['inp1']])
  }
  
  if ( 'inp2' %in% names(inst) ) {
    if ( !is.na(as.numeric(inst['inp2'])) ) {
      inp2 <- as.numeric(inst['inp2'])
    } else {
      inp2 <- as.numeric(wires[inst['inp2']])
    }
  }
         
  if (inst['op'] == 'EMIT') {
    # print(sprintf("Setting wires[%s] to %s", inst['dest'], inp1))
    wires[inst['dest']] <<- inp1
  } else if ( inst['op'] == 'NOT' ) {
    # bitwise NOT can result in negative, so AND it with 65535.
    # this will do nothing if positive, but wrap the int if negative
    val <- bitwAnd(bitwNot(inp1), 65535)
    # print(sprintf("Setting wires[%s] to %s", inst['dest'], val))
    wires[inst['dest']] <<- val
  } else if ( inst['op'] == 'AND' ) {
    val <- bitwAnd(inp1, inp2)
    # print(sprintf("Setting wires[%s] to %s", inst['dest'], val))
    wires[inst['dest']] <<- val
  } else if ( inst['op'] == 'OR' ) {
    val <- bitwOr(inp1, inp2)
    # print(sprintf("Setting wires[%s] to %s", inst['dest'], val))
    wires[inst['dest']] <<- val
  } else if ( inst['op'] == 'LSHIFT' ) {
    val <- bitwShiftL(inp1, inp2)
    # print(sprintf("Setting wires[%s] to %s", inst['dest'], val))
    wires[inst['dest']] <<- val
  } else if ( inst['op'] == 'RSHIFT' ) {
    val <- bitwShiftR(inp1, inp2)
    # print(sprintf("Setting wires[%s] to %s", inst['dest'], val))
    wires[inst['dest']] <<- val
  }
}

# run until all instructions are processed
while (TRUE){
  if (length(inst_list) == 0) break
  processed <- c()
  for (i in seq_along(inst_list)) {
    inst = inst_list[[i]]
    # we can run this instruction if inp1 (and inp2, if needed)
    # are defined in wires (i.e. in `names(wires)``) OR
    # if the input is a number
    if (inst['inp1'] %in% names(wires) || !is.na(as.numeric(inst['inp1']))){
      # check if input 2 is present and do same checks
      if (! 'inp2' %in% names(inst) || 
          (inst['inp2'] %in% names(wires) || 
           !is.na(as.numeric(inst['inp2'])))){
        # print(sprintf('Processing %s', paste0(inst, collapse=" ")))
        processInstruction(inst)
        processed <- c(processed, i)
      }
    }
  }
  inst_list <- inst_list[-processed]
}

wires <- wires[order(names(wires))]
print(sprintf('Value on wire a is %s', wires['a']))