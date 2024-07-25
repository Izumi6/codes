# python program to solve:-
# 	- sop : sum of products ( A.B.C + A'.B' + B.C'  )
#	- pos : product of sums ( A+B+C . A'+B' . B+C'  )


# imports
import re
import sys
import argparse


# minimization techniques
def kmap():
	pass

def quine_mccluskey():
	pass


# standardization techniques
def standardize(nl, srp): 
	# exp > contains all vars
	# eg: `A.B + B.C` > `A.B.C + A.B.C' + A'.B.C`
	# steps:
	#	- find total vars
	# 	- divide grps
	#	- add missing var & apply distributive law
	# 	- remove duplicates
	
	# s1
	tv = total_vars(nl, 1)
	
	# s2 - `nl` 

	# s3
	std = []
	if nl[1][0] == '+':
		v1 = "."
		v2 = "+"
	else:
		v1 = "+"
		v2 = "."

	m = 1 # modified flag (1-not modified, 0-modified)
	std = recursive(nl, std, tv, v1, v2, m)

	# s4
	pair_up = []
	# pairing up list of seperate vars of `e` & `e`
	for n,e in enumerate(std):
		if n%2 == 0:
			# get total_vars
			etv = sorted(total_vars(str_to_list(e[0]), 0))
			pair_up.append([etv, e[0]])

	# remove duplicates
	std_exp = []
	added = []
	for p in pair_up:
		if p[0] not in added:
			std_exp.append(p[1])
			added.append(p[0])

	print("\n\t[#] Standard expression:", (''.join(x+f" {'+' if srp == 1 else '.'} " for x in std_exp)).strip(f" {'+' if srp == 1 else '.'} "), '\n')



# features support funcs

## kmaps
def neighbors():
	# x - ver to find neighbors; n - total number of vars
	# up    -> x-n (x>n)
	# down  -> x+n (x<n)
	# left  -> x-1
	# right -> x+1
	pass

def reassign():
	# 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 -> 0,1,3,2,4,5,7,6,12,13,15,14,8,9,11,10
	pass


def display_kmaps(func):
	# 
	# _________________
	# | 1 | 0 | 1 | 0 |
	# |———

	# vars - 2, 3, 4, 5, 6, 7 ...
	# corners (2) = 4 (const)
	# edges   (3) = 0, 4, 8, 16, 24, 
	# center  (4) = 0, 0, 4, 12, 36, 
	pass

def validate_kmaps(func):
	# checks:
	# - numbers should not repeat

	# table formation logic - rows-&-cols - 2^n
	# total number of vars (n)

	pass


## std
def recursive(nl, std, tv, v1, v2, m):
        for n,l in enumerate(nl):
            tmp = []
            m = 0
            if n%2 == 0:
                for t in tv:
                    if (t not in l and complement(t) not in l) and not m:
                        # distributive law
                        std.append([''.join(x for x in l) + v1 + t])
                        std.append([v2])
                        std.append([''.join(x for x in l) + v1 + complement(t)])
                                     
                        tmp.append(str_to_list([''.join(x for x in l) + v1 + t][0]))
                        tmp.append([v2])
                        tmp.append(str_to_list([''.join(x for x in l) + v1 + complement(t)][0]))
                        
                        m = 1

                    if m:
                     if len((''.join(x for x in tmp[0])).replace(".", '').replace("+", '').replace("'", '')) != len(tv):
                        std = recursive(tmp, [], tv, v1, v2, 0)
                        break
                        
            else: std.append(l)
        return std

def total_vars(nl, sod): # sod - single (0) or double (1)
	checked_vars = []
	for l in nl:
		if sod:
			for i in l:
				if i not in checked_vars and (i != '+' and i != '.'):
					if i.strip("'") not in checked_vars:
						checked_vars.append(i.strip("'"))
		else:
			if l not in checked_vars and (l != '+' and l != '.'):
				checked_vars.append(l)
	return checked_vars

def complement(c):
	if "'" in c: return c.strip("'")
	else: return c+"'"

def str_to_list(func):
	func_list = []
	for chr in func:
		if chr == "'":
			func_list[-1] += "'"
		else:
			func_list.append(chr)
	return func_list

def rm_duplicate_vars(nl):
	for l in nl:
		checked_vars = []
		for i in l:
			if i.strip("'") in checked_vars: return 1
			if  i != '+' and i != '.':
				checked_vars.append(i.strip("'"))
	return 0

def format_n_detect(v1, v2, nl):
	for l in nl:
		if (v1 in l and len(l) != 1) or (v2 in l and len(l) == 1): return 0

	# the even ones should be v1 (i.e. odd when start from zero)
	for n,i in enumerate(nl):
		if n%2 != 0 and i[0] != v1: return 0

	# remove duplicates () A.A.B + B.B' or A+A+B . B+B' )
	if rm_duplicate_vars(nl): return 0

	return 1

## `A.B + B.C` | `A+B . B+C`
def validate_std(func, nl):
	# sop        > X(no space).(no space)X(space)+(continued)
	# 		     - 	X(no space).(no space)X
	# 		     - 	(space)+(space)
	# pos        > X(no space)+(no space)X(space).(continued)
	# 		     - 	X(no space)+(no space)X
	# 		     - 	(space).(space)
	# complement > X'


	# LVL1 - chars

	allowlist = [".", "+", " ", "'"]
	prev_chr = ' '

	for char in func:
		# checking if given chr is alphabet or not
		is_alpha = re.search(r'([A-Z])', char)
		
		# (only allowed chars present
		if not char in allowlist and not is_alpha: return 0
		# no alphabets side-by-side
		if not prev_chr in allowlist and is_alpha: return 0
		# `'` should be always after `X`
		if char == "'" and not re.search(r'([A-Z])', prev_chr): return 0		

		# updating prev_chr
		prev_chr = char
		


	# LVL2 - format (+ detect)

	# variations
	# 	X .    X' .
	#	X' .   X' +
	# 	X.	   X'.
	#	X.	   X+

	if len(nl)%2 != 0:
		if nl[1][0] == '+': # sop (heuristically)
			if format_n_detect("+", ".", nl): return 1

		elif nl[1][0] == '.': # pos (heuristically)
			if format_n_detect(".", "+", nl): return 2

		else: return 0

	# for single - products in sop & sums in pos
	elif len(nl) == 1:
		if "." in nl[0] and not "+" in nl[0]: return 1
		elif "+" in nl[0] and not "." in nl[0]: return 2

	# if len(nl) == 2 
	else: return 0


# main support funcs

## `AB+BC` | `(A+B)(B+C)`
def converter():
	pass

## banner
def banner():
	# 3D mirror effect program logo
	print('''
                                         |\\‾‾\\
            ------- ------- -------      | \\  \\       ------- ------- -------
            |       |     | |     |      |  \\__\\      |     | |     | |     
            |-----| |     | |------      |  |  |      |------ |     | |-----|
                  | |     | |            |  |  |      |       |     |       |    
            ------- ------- |            |  |  |      |       ------- -------
                                         |  |  |
     ------------------------------------\\--|--|------------------------------------
                                          \\ |  |                                          
    ---------------------------------------\\|__|----------------------------------''')


# main
def main():
	# banner / logo
	banner()

	# cli args
	parser = argparse.ArgumentParser()
	parser.add_argument('-m', '--mode', help='Select a mode (1. Standard Expression; 2. Kmaps; 3. Quine Mc Cluskey)')
	parser.add_argument('-f', '--func', help='Enter expression / notations')
	parser.add_argument('-n', '--notation', help='Select notation symbol (1. Σm; 2. πM)')
	args = parser.parse_args()

	# options
	try:
		mode = int(args.mode) if args.mode else int(input("\n\t------------------------------------------\n\t1. Standardize given expression\n\t2. Minimize using KMAPS method\n\t3. Minimize using QUINE MC CLUSKEY method\n\t------------------------------------------\n\t[+] Enter your choice: "))
		if mode > 3 and mode < 1: raise Exception
	except:
		print("\t[!] Invalid choice")
		exit()

	# calling funcs
	if mode == 1:
		func = args.func.upper() if args.func else input("\n\t[+] Enter expression: ").upper()

		# list by space + nested list
		nl = [ str_to_list(L) for L in re.split(r' ', func) ]

		# validate
		sop_or_pos = validate_std(func, nl)
		# 0 = invalid, 1 = sop, 2 = pos
		if not sop_or_pos:
			print("\t[!] Invalid expression")
			exit()
		
		# standardize
		standardize(nl, sop_or_pos)

	elif mode == 2: 
		func = args.func.upper() if args.func else input("\n\t[+] Enter notations: ").upper()

		# validate
		no_of_vars = validate_kmaps(func)

		try:
			# summation or pi
			sum_or_pi = int(args.notation) if args.notation else int(input("\n\t------------------------------------------\n\t1. Σm : Summation (minterms)\n\t2. πM : Pi (maxterms)\n\t------------------------------------------\n\t[+] Enter your choice: "))
			if mode > 2 and mode < 1: raise Exception
		except:
			print("\t[!] Invalid choice")
			exit()

		# minimization using kmaps
		kmaps()

	elif mode == 3: quine_mc_cluskey(nl)
		

	



# run main 
if __name__ == '__main__':
	main()
