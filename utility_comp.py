import numpy as np
import matplotlib.pyplot as plt
import sys

# Column spec for election data:
# [0: unique voter id]
# [1:vote, 1 obama 2 romney]
# [2-7: issue importance, scale from 0 to 3]
# [8-13: who would handle issue better, 1 romney 2 obama]
# 3: romney/obama are equal, 9 is missing val

# Column spec for primary data:
# [0: unique voter id]
# [1: preferred nominee]
# [2-5: issue importances, 1 most important, 4 is least]
# [6-9: which candidate preferred on each issue]
# Notes: 1=Gingrich, 2=Huntsman, 3=Ron Paul, 4=Rick Perry, 5=Romney, 6=Santorum

# Unpack and parse the data from the files contianing the primary and
# election data.
primary_data = open('jan12_new.csv')
election_data = open('sept12_new.csv')

primary_votes = []
i = 0
for l in primary_data:
	if i != 0:
		primary_votes.append(map(lambda x: int(x.rstrip()), l.split(",")))
	i += 1

election_votes = []
i = 0
for l in election_data:
	if i != 0:
		election_votes.append(map(lambda x: int(x.rstrip()), l.split(",")))
	i += 1

# Rank the primary candidates according to our rule and plurality voting.
scores = [0] * 6
plurality_scores = [0] * 6
for vote in primary_votes:
	if 9 in vote or 8 in vote or 7 in vote:
		continue
	plurality_scores[vote[1]-1] += 1

	# Issue importances mapped to 0 - 3
	alpha = map(lambda x: 4 - x, vote[2:6])
	for j in xrange(len(vote[6:10])):
		scores[vote[6 + j] - 1] += alpha[j]

print "According to our voting rule:"
cand_dict = {1:'Gingrich',2:'Huntsman',3:'Paul',4:'Perry',5:'Romney',6:'Santorum'}
for k in cand_dict.keys():
	print "Candidate " + cand_dict[k] + " received: " + str(scores[k-1])
print "\n"

print "According to the plurality rule, the winners are:"
for k in cand_dict.keys():
	print "Candidate " + cand_dict[k] + " received: " + str(plurality_scores[k-1])

# Now that we have the scores, let's compute the total utility of everyone,
# where we are assuming that voter utility functions have the following form,
# where gamma is the normalized output from the voting rule:
# $u_i(\vec{\gamma}) = \sum_{j=1}^k \alpha_{ij}(\beta_{ij}\cdot \vec{\gamma})$

total_utility_our_rule = 0
total_utility_plurality_rule = 0

gamma_1 = [float(k)/sum(scores) for k in scores]
gamma_plurality = [float(k)/sum(plurality_scores) for k in plurality_scores]

for vote in primary_votes:
	if 9 in vote or 8 in vote or 7 in vote:
		continue
	utility_i_1 = 0
	utility_i_plurality = 0

	alpha = map(lambda x: 4 - x, vote[2:6])
	for j in xrange(len(vote[6:10])):
		utility_i_1 += alpha[j] * gamma_1[vote[6 + j] - 1]
		utility_i_plurality += alpha[j] * gamma_plurality[vote[6 + j] - 1]

	total_utility_our_rule += utility_i_1
	total_utility_plurality_rule += utility_i_plurality

print "Total utility under our rule:", total_utility_our_rule
print "Total utility under their rule:", total_utility_plurality_rule

