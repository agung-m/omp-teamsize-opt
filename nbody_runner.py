import subprocess
import re

class NBodyRunner:
    def __init__(self, workdir, num_teams, src_filename, temp_src_filename, run_script):
        self.workdir = workdir
        self.num_teams = num_teams
        self.main_src = self.workdir + '/' + src_filename
        self.run_script = self.workdir + '/' + run_script

        # Regex patterns
        self.patts = [None] * self.num_teams
        for i in range(0, self.num_teams):
            i_str = str(i)
            self.patts[i] = r'([\S\s]int THDS'+re.escape(i_str)+'=)\d{1,}(;)'
        #pattern = re.compile(r'\(([0-9])*,')

        orig_filename = self.workdir + '/' + temp_src_filename
        self.orig_src = open(orig_filename, 'r')
        self.orig_code = self.orig_src.read()

    def replace(self, orig_str, new_vals):
        result = orig_str
        for i in range(len(self.patts)):
            result = re.sub(self.patts[i], r'\g<1>{}\g<2>'.format(new_vals[i]), result)
        return result

    def modify_src(self, params):
        modified = self.replace(self.orig_code, params)
        with open(self.main_src, 'w') as fo:
            fo.write(modified)

    def execute_nbody(self, params):
        self.modify_src(params)
        command = [self.run_script]
        process = subprocess.run(command, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        # Get results from stdout, application is asummed to return the execution time
        exec_time = float(process.stdout)
        return exec_time

# Main program
if __name__ == "__main__":
    workdir = '.'
    num_teams = 4
    src_filename = "src/parallel/main.c"
    temp_src_filename = 'src/parallel/main-4teams.c'
    run_script = 'compile_run.sh'

    nbody_runner = NBodyRunner(workdir, num_teams, src_filename, temp_src_filename, run_script)
    nbody_runner.execute_nbody([15, 15, 15, 15])

#patts = [None] * 4
#patts[0] = r'([\S\s]int THDS0=)\d{1,}(;)'
#patts[1] = r'([\S\s]int THDS1=)\d{1,}(;)'
#patts[2] = r'([\S\s]int THDS2=)\d{1,}(;)'
#patts[3] = r'([\S\s]int THDS3=)\d{1,}(;)'

#pattern = re.compile(r'\(([0-9])*,')