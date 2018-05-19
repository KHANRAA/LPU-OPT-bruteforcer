#!/usr/bin/python2.7

from random import shuffle

# add more keywords in og
og = ["opt2", "opt4", "opt5", "opt9", "opt10", "opt11", "opt16", "lpu", "reset", "password", "passcode", "upload",
      "odessa", "google", "tcs", "opt", "lovely", "exam", "test", "cisco", "login", "student", "redhat"]

# change filename
f = open('small.txt', 'w')

# add more special characters if needed
chars = ["@", "#"]

words = []

for _ in range(len(og)):
    # add to the beginning
    for x in range(len(chars)):
        words.append(og[_] + chars[x])

    # add to the end
    for x in range(len(chars)):
        words.append(chars[x] + og[_])

    # add at both ends
    for x in range(len(chars)):
        for y in range(len(chars)):
            words.append(chars[y] + og[_] + chars[x])

shuffle(words)

for _ in range(len(words)):
    f.write(words[_] + '\n')
