# -*- coding: utf-8 -*-
'''
This module provides you to compute difference sets between two
or three texts ported from GNU diff3.c written by R. Smith.

For users convenience, diff3lib includes small diff procedure
based on the P. Heckel's algorithm. On the other hands,
many other systems use the popular Least Common Sequence (LCS) algorithm.
The merits for each algorithm are case by case. In author's experience,
two algorithms generate almost same results for small local changes
in the text. In some cases, such as moving blocks of lines,
it happened quite differences in results.

MIZUTANI Tociyuki <tociyuki@gmail.com>.

Copyright (C) 2015 MIZUTANI Tociyuki

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2.
'''

from functools import cmp_to_key

def diff3(text0, text2, text1):
  """Calcurate three-way differences. This returns difference sets.

      range3_list = diff3lib.diff3(mytext, origial, yourtext)

  For example,

      range3_list = diff3lib.diff3(
          ['A', 'A', 'b', 'c', 'f', 'g', 'h', 'i', 'j', 'K', 'l', 'm',
           'n', 'O', 'p', 'Q', 'R', 's'],
          ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's'],
          ['a', 'b', 'c', 'd', 'f', 'j', 'K', 'l', 'M', 'n', 'o', 'p',
          '1', '2', 's', 't', 'u'])

  returns a following list:

      [
          ['0',  1, 2,  1, 1,  1, 1],
          ['A',  5, 4,  4, 4,  4, 5],
          ['1',  6, 8,  6, 5,  7, 9],
          ['2', 10,10,  7, 7, 11,11],
          ['1', 12,12,  9, 9, 13,13],
          ['0', 14,14, 11,11, 15,15],
          ['A', 16,17, 13,14, 17,18],
          ['1', 19,18, 16,17, 20,19],
      ]

  where

      case range3_list[i][0]
      when '0': changes by my text.
      when '1': changes by your text.
      when '2': changes from original text.
      when 'A': conflict!
      end

  line numbers start from 1.
  the three-way diff based on the GNU diff3(1)  GNU/diffutils/2.7/diff3.c

      Three way file comparison program (diff3) for Project GNU.
      Copyright (C) 1988, 1989, 1992, 1993, 1994 Free Software Foundation, Inc.
      Written by Randy Smith
  """

  range3_list = []
  range2_list = [diff(text2, text0), diff(text2, text1)]
  range3 = [None, 0,0,  0,0,  0,0]

  while len(range2_list[0]) > 0 or len(range2_list[1]) > 0:
    range2 = [[], []]
    if len(range2_list[0]) == 0:
      i = 1
    elif len(range2_list[1]) == 0:
      i = 0
    elif range2_list[0][0][1] <= range2_list[1][0][1]:
      i = 0
    else:
      i = 1
    j = i
    k = 1 - i
    a1_j = range2_list[j][0][2]
    range2[j].append(range2_list[j].pop(0))

    while len(range2_list[k]) > 0 and range2_list[k][0][1] <= a1_j + 1:
      a1_k = range2_list[k][0][2]
      range2[k].append(range2_list[k].pop(0))
      if a1_j < a1_k:
        a1_j = a1_k
        j, k = k, j
    lo2 = range2[i][0][1]
    hi2 = range2[j][-1][2]

    if len(range2[0]) > 0:
      lo0 = range2[0][0][3] - range2[0][0][1] + lo2
      hi0 = range2[0][-1][4] - range2[0][-1][2] + hi2
    else:
      lo0 = range3[2] - range3[6] + lo2
      hi0 = range3[2] - range3[6] + hi2
    if len(range2[1]) > 0:
      lo1 = range2[1][0][3] - range2[1][0][1] + lo2
      hi1 = range2[1][-1][4] - range2[1][-1][2] + hi2
    else:
      lo1 = range3[4] - range3[6] + lo2
      hi1 = range3[4] - range3[6] + hi2

    range3 = [None, lo0,hi0,  lo1,hi1,  lo2,hi2]

    if len(range2[0]) == 0:
      range3[0] = '1'
    elif len(range2[1]) == 0:
      range3[0] = '0'
    elif hi0 - lo0 != hi1 - lo1:
      range3[0] = 'A'
    else:
      range3[0] = '2'
      for d in range(hi0 - lo0 + 1):
        i0 = lo0 + d - 1
        i1 = lo1 + d - 1
        ok0 = i0 in range(len(text0))
        ok1 = i1 in range(len(text1))
        if ok0 ^ ok1 or (ok0 and text0[i0] != text1[i1]):
          range3[0] = 'A'
          break

    range3_list.append(range3)

  return range3_list

def diff(a, b):
  """The two-way diff based on the algorithm by P. Heckel.

      range2_list = diff3lib.diff(original, mytext)

  For example,

      range2_list = diff3lib.diff(
          ['a', 'b', 'c',           'f', 'g', 'h', 'i', 'j'],
          ['a', 'B', 'c', 'd', 'e', 'f',                'j'] )

  returns a following list:

      [
          ['c', 2,2, 2,2],  # 2c2    change
          ['a', 4,3, 4,5],  # 4a4,5  append
          ['d', 5,7, 7,6]   # 5,7d7  delete
      ]

  where line numbers start from 1.

      P. Heckel. ``A technique for isolating differences between files.''
      Communications of the ACM, Vol. 21, No. 4, page 264, April 1978.
  """

  uniqs = [[len(a), len(b)]]
  freqs = {}
  ap = {}
  bp = {}
  for i in range(len(a)):
    s = a[i]
    freqs[s] = freqs.setdefault(s, 0) + 2
    ap[s] = i
  for i in range(len(b)):
    s = b[i]
    freqs[s] = freqs.setdefault(s, 0) + 3
    bp[s] = i

  for (s, x) in freqs.items():
    if x == 5:
      uniq_pair = (ap[s], bp[s])
      uniqs.append(uniq_pair)
  freqs = ap = bp = None

  def cmpf(x, y):
    if x[0] < y[0] and x[1] < y[1]:
      return -1
    if x[0] == y[0] and x[1] == y[1]:
      return 0
    return +1

  uniqs.sort(key=cmp_to_key(cmpf))

  range2_list = []

  a1 = b1 = 0
  for a_uniq, b_uniq in uniqs:
    while a1 < len(a) and b1 < len(b) and a[a1] == b[b1]:
      a1 += 1
      b1 += 1
    if a_uniq < a1 or b_uniq < b1:
      continue
    a0 = a1
    b0 = b1
    a1 = a_uniq - 1
    b1 = b_uniq - 1
    while a0 <= a1 and b0 <= b1 and a[a1] == b[b1]:
      a1 -= 1
      b1 -= 1
    if a0 <= a1 and b0 <= b1:
      range2_list.append(['c', a0 + 1, a1 + 1, b0 + 1, b1 + 1])
    elif a0 <= a1:
      range2_list.append(['d', a0 + 1, a1 + 1, b0 + 1, b0])
    elif b0 <= b1:
      range2_list.append(['a', a0 + 1, a0, b0 + 1, b1 + 1])
    a1 = a_uniq + 1
    b1 = b_uniq + 1

  return range2_list

