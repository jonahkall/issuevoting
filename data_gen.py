import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

num_voters = 10
num_issues = 8
num_candidates = 10
num_alpha_bases = 7 
num_beta_bases = 12 
num_trials = 10000

utilities = [0] * 4
kendall_tau = np.zeros((4,4))

for trial in xrange(num_trials):
	# first entry is unnormalized rule 1
	rule_1_scores = [0] * num_candidates
	plurality_scores = [0] * num_candidates
	borda_scores = [0] * num_candidates
	two_step_scores = [0] * num_candidates

	def normalize_and_fix_zeros(v):
		return [a/float(sum(v)) if a >= 0 else 0 for a in v]

	def max_ind(vec):
		maxi = 0
		m = vec[0]
		for i, a in enumerate(vec):
			if a > m:
				maxi = i
				m = a 
		return maxi

	basis_alphas = np.random.random((num_alpha_bases, num_issues))
	basis_betas = np.random.random((num_beta_bases, num_candidates))

	alphas = []
	betas = []

	beta_offsets = np.abs(np.random.normal(0, 0.10, (num_issues, num_candidates)))

	for i in xrange(num_voters):
		basis_alpha_ind = np.random.randint(num_alpha_bases)
		alpha = np.random.normal(basis_alphas[basis_alpha_ind], 0.08)

		# If any entries in alpha are negative, we will ignore them
		alpha = normalize_and_fix_zeros(alpha)
		alphas.append(alpha)

		# Now we need to generate our beta
		beta = []
		basis_beta_ind = np.random.randint(num_beta_bases)
		for j in xrange(num_issues):
			bjtmp = np.random.normal(basis_betas[basis_beta_ind], 0.08)
			bjtmp = normalize_and_fix_zeros(bjtmp)
			beta.append(bjtmp)
		beta = np.array(beta)
		beta += beta_offsets
		for j in xrange(num_issues):
			beta[j] = normalize_and_fix_zeros(beta[j])
		betas.append(beta)

	# First take care of plurality, borda, rule 1
	for i in xrange(num_voters):
		for j in xrange(num_issues):
			borda = np.argsort(betas[i][j])
			for k in xrange(num_candidates):
				rule_1_scores[k] += alphas[i][j] * betas[i][j][k]
				borda_scores[k] += alphas[i][j] * np.where(borda == k)[0][0]
			plurality_scores[max_ind(betas[i][j])] += alphas[i][j]

	# now two step
	# first aggregate alphas
	alpha_final = [0] * len(alphas[0])
	for alph in alphas:
		for j in xrange(len(alphas[0])):
			alpha_final[j] += alph[j]

	superbetas = np.zeros((num_candidates, num_issues))
	# now aggregate betas
	for i in xrange(num_voters):
		for j in xrange(num_issues):
			borda = np.argsort(betas[i][j])
			for k in xrange(num_candidates):
				superbetas[k][j] += np.where(borda == k)[0][0]
		
	for j in xrange(num_issues):
		for i in xrange(num_candidates):
			two_step_scores[i] += alpha_final[j] * superbetas[i][j]	

	rankings = [np.argsort(rule_1_scores), np.argsort(plurality_scores), np.argsort(borda_scores),np.argsort(two_step_scores)]

	#print "Rule 1 candidate ranking:", rankings[0]
	#print "Plurality candidate ranking:", rankings[1]
	#print "Borda ranking:", rankings[2]
	#print "Two step ranking:", rankings[3]

	# Calculate utilities
	utility_1 = 0
	utility_plurality = 0
	utility_borda = 0
	utility_two_step = 0

	for i in xrange(num_voters):

		for j in xrange(num_issues):
			#borda = np.argsort(betas[i][j])
			for k in xrange(num_candidates):
				utility_1 += alphas[i][j] * betas[i][j][k] * np.where(rankings[0] == k)[0][0]/num_candidates #scipy.stats.kendalltau(borda,rankings[0])[0] 
				utility_plurality += alphas[i][j] * betas[i][j][k] * np.where(rankings[1] == k)[0][0]/num_candidates #scipy.stats.kendalltau(borda, rankings[1])[0] 
				utility_borda += alphas[i][j] * betas[i][j][k] * np.where(rankings[2] == k)[0][0]/num_candidates #scipy.stats.kendalltau(borda, rankings[2])[0] 
				utility_two_step += alphas[i][j] * betas[i][j][k] * np.where(rankings[3] == k)[0][0]/num_candidates #scipy.stats.kendalltau(borda, rankings[3])[0] 

	#print "Rule 1 candidate utility:", utility_1 
	#print "Plurality candidate utility:", utility_plurality 
	#print "Borda utility:", utility_borda 
	#print "Two step utility:", utility_two_step 

	utilities[0] += utility_1
	utilities[1] += utility_plurality 
	utilities[2] += utility_borda
	utilities[3] += utility_two_step

	for i in xrange(4):
		for j in xrange(4):
			kendall_tau[i][j] += scipy.stats.kendalltau(rankings[i],rankings[j])[0]

print "Average utility", [u/num_trials for u in utilities]
print "Kendall-tau matrix\n", kendall_tau/num_trials


