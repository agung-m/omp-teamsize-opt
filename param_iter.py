from itertools import combinations, combinations_with_replacement, permutations, product
import subprocess
import re
import sys


def log(filename, msg):
    with open(filename, 'a+') as logfile:
        logfile.write(msg)

def list_combinations(arr, n_com):
    return list(combinations_with_replacement(arr, n_com))
    #return list(combinations(arr, n_com))

def list_permutations(arr, n_com):
    return list(permutations(arr, n_com))

def list_products(arr, n_com):
    return list(product(arr, repeat=n_com))

def run_file():
    # Run compile
    #compile_cmd = ''
    #compile_params = ''
    #subprocess.call(compile_cmd, compile_params)
    # Run program
    #run_cmd = ''
    #run_params = ''
    #subprocess.call(compile_cmd, compile_params)
    run_cmd = './compile_run.sh'
  #  run_cmd = './compile.sh && ./run.sh'
    subprocess.call([run_cmd])

def has_duplicates(c):
    b = set(c)
    return len(b) < len(c)

def replace(orig_str, new_vals, find_patts):
    result = orig_str
    for i in range(len(find_patts)):
        result = re.sub(find_patts[i], r'\g<1>{}\g<2>'.format(new_vals[i]), result)
    return result

def combinations_eval(c, t_limit):
    return sum(c) == t_limit #and not has_duplicates(c)

#t_params = [48,52,56,60,64,68,72,76,80,84,88,92,96,100,104,108,112,116,120,124,128,132,136,140,144,148,152,156,160,164,168,172,176,180,184,188,192,196,200,204,208,212,216,220,224,228,232,236,240]
#t_limit = 288
#team_num = 2
t_params = [40,44,48,52,56,60,64,68,72,76,80,84,88,92,96,100,104,108,112,116,120,124,128,132,136]
t_limit = 288
team_num = 4
combinations_limit = 1000000000
logfile = "results-4teams.csv"

patts = [None] * 4
patts[0] = r'([\S\s]int THDS0=)\d{1,}(;)'
patts[1] = r'([\S\s]int THDS1=)\d{1,}(;)'
patts[2] = r'([\S\s]int THDS2=)\d{1,}(;)'
patts[3] = r'([\S\s]int THDS3=)\d{1,}(;)'
#pat_thds3 = r'(^\s?int THDS3=)\d{1,}(;)'

pattern = re.compile(r'\(([0-9])*,')

run_fname = './src/parallel/main.c'
src = open('./src/parallel/main-4teams.c', 'r')
#src = open('./evaluation-4teams.cpp', 'r')
tempstr = src.read()
src.close()

#c_list = list_combinations(t_params, team_num)
#c_list = list_permutations(t_params, team_num)
c_list = list_products(t_params, team_num)
#c_list = [[20,20,20,20],
#          [40,40,40,40],
#          [], ]
#print(c_list)
print("Evaluating {} combinations of params (limit={})..".format(len(c_list), combinations_limit))
clist2 = []
#n_eval = 0
for c in c_list:
   # print(c)
    if combinations_eval(c, t_limit) and len(clist2) <= combinations_limit:   # Check the limit of number of the threads
        #n_eval += 1
        clist2.append(c)
#print('# of combinations,{}\n'.format(len(clist2)))
log(logfile, "# of combinations, {}\n".format(len(clist2)))
#print(clist2)

for c in clist2:
    # replace the code with new vars
    result = replace(tempstr, c, patts)
    # save replaced text to new file
    # print(result)
    with open(run_fname, 'w') as fo:
        fo.write(result)
    log(logfile, "Combination, {}\n".format(c))
    #print('Combination, {}'.format(c))
    #sys.stdout.write('Combination, {}\n'.format(c))
    #print(c)
    #sys.stdout.flush()
    # Compile and run the program
    run_file()
