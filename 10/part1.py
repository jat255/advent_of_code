"""
--- Day 10: Balance Bots ---
You come upon a factory in which many robots are zooming around handing small microchips to each other.

Upon closer examination, you notice that each bot only proceeds when it has two microchips, and once it does, it gives each one to a different bot or puts it in a marked "output" bin. Sometimes, bots take microchips from "input" bins, too.

Inspecting one of the microchips, it seems like they each contain a single number; the bots must use some logic to decide what to do with each chip. You access the local control computer and download the bots' instructions (your puzzle input).

Some of the instructions specify that a specific-valued microchip should be given to a specific bot; the rest of the instructions indicate what a given bot should do with its lower-value or higher-value chip.

For example, consider the following instructions:

value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2

- Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a value-2 chip and a value-5 chip.
- Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and its higher one (5) to bot 0.
- Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and gives the value-3 chip to bot 0.
- Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in output 0.

In the end, output bin 0 contains a value-5 microchip, output bin 1 contains a value-2 microchip, and output bin 2 contains a value-3 microchip. In this configuration, bot number 2 is responsible for comparing value-5 microchips with value-2 microchips.

Based on your instructions, what is the number of the bot that is responsible for comparing value-61 microchips with value-17 microchips?
"""
import re
from typing import Dict, Tuple, Union

bot_regex = re.compile("bot (\d+)")
output_regex = re.compile("output (\d+)")
# %%

class Bot:
  def __init__(self, number: int):
    self.low_chip: Union[None, int] = None
    self.high_chip: Union[None, int] = None
    self.number: int = number
    
    # if int, the target is an output
    self.low_target: Union[None, Bot, int] = None 
    self.high_target: Union[None, Bot, int] = None 

  def __repr__(self):
    return f"Bot {self.number}: [{self.low_chip}, {self.high_chip}] -> [{self.low_target}, {self.high_target}]"

  def __str__(self):
    return f"Bot {self.number}"

  def is_full(self):
    return all([i is not None for i in [self.low_chip, self.high_chip]])

  def is_empty(self):
    return all([i is None for i in [self.low_chip, self.high_chip]])

  def add_chip(self, value: int):
    if self.is_full():
      raise ValueError(f"Bot {self.number} already has two chips")
    if self.is_empty():
      # assign as lower chip by default
      self.low_chip = value
    elif value < self.low_chip:
      self.high_chip = self.low_chip
      self.low_chip = value
    else:
      self.high_chip = value

  def do_transfer(self, outputs: Dict[int, int], inquiry: Tuple[int, int] = None):
    if any([i is None for i in [self.low_chip, self.high_chip]]):
      raise ValueError(f"Bot {self.number} does not have both inputs to do transfer; {repr(self)}")
    else:
      # print(f"do_transfer for {repr(self)}")
      if inquiry is not None:
        if self.low_chip == min(inquiry) and self.high_chip == max(inquiry):
          print(f"*** Bot {self.number} responsible for comparing chips {inquiry}")
      if isinstance(self.low_target, int):
        outputs[self.low_target] = self.low_chip    
      else:
        self.low_target.add_chip(self.low_chip)
        # print(f"{self.low_target} is now {repr(self.low_target)}")
      if isinstance(self.high_target, int):
        outputs[self.high_target] = self.high_chip
      else:
        self.high_target.add_chip(self.high_chip)
        # print(f"{self.high_target} is now {repr(self.high_target)}")
    self.low_chip = None
    self.high_chip = None

class Controller:
  def __init__(self, lines):
    self.bots: Dict[int, Bot] = {}
    self.outputs: Dict[int, int] = {}

    # create bots
    for l in lines:
      if l[0] == 'v': 
        # value setting line
        val = int((ll := l.split())[1])
        bot_num = int(ll[5])
        if bot_num not in self.bots:
          self.bots[bot_num] = Bot(bot_num)
        self.bots[bot_num].add_chip(val)
      elif l[0] == 'b':
        subject_bot_num = int((ll := l.split())[1])
        if subject_bot_num not in self.bots:
          self.bots[subject_bot_num] = Bot(subject_bot_num)
        
        low_target_type = ll[5]
        low_target_num = int(ll[6])
        high_target_type = ll[10]
        high_target_num = int(ll[11])

        if low_target_type == 'bot':
          if low_target_num not in self.bots:
            self.bots[low_target_num] = Bot(low_target_num)
        if high_target_type == 'bot':
          if high_target_num not in self.bots:
            self.bots[high_target_num] = Bot(high_target_num)
        
        self.bots[subject_bot_num].low_target = \
          low_target_num if low_target_type == 'output' else self.bots[low_target_num]
        self.bots[subject_bot_num].high_target = \
          high_target_num if high_target_type == 'output' else self.bots[high_target_num]

  def run_bots(self, inquiry: Tuple[int, int] = None):
    while any([i.is_full() for i in self.bots.values()]):
      for b in self.bots.values():
        if b.is_full():
          b.do_transfer(self.outputs, inquiry)

print("Test input")
with open('test_input.txt') as f:
  lines = [l.strip() for l in f.readlines()]
c = Controller(lines)
c.run_bots((5,2))
# for bk, bv in c.bots.items():
#   print(repr(bv))
print(c.outputs)
print()

print("Real input")
with open('input.txt') as f:
  lines = [l.strip() for l in f.readlines()]
c = Controller(lines)

# for bk, bv in c.bots.items():
#   if bv.number in [54, 107]:
#     print(repr(bv))

c.run_bots((61,17))
print(c.outputs)
print()

# 147
