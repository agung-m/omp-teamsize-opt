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
        # Convert to python list to ensure compatibility
        params = params.tolist()
        print("- [NBodyRunner] team sizes: {}".format(params))
        self.modify_src(params)
        command = [self.run_script]
        #process = subprocess.run(command, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        # subprocess call for Python 2.7.x
        process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=4096)
        # Get results from stdout, application is asummed to return the execution time
        out, err = process.communicate()
        exec_times = self.parse_output(out)
        print("- [NBodyRunner] exec_times: {}".format(exec_times))
        #exec_time = float(process.stdout)
        return exec_times

    def parse_output(self, out):
        exec_times = [None] * 2
        #out_str = stdout.decode("utf-8")
        #lines = stdout.decode("utf-8").splitlines()
        lines = str(out).splitlines()
        #print(lines)
        for line in lines:
            #line = line.decode("utf-8").rstrip()
            #print(line)
            if line.startswith("Physical total"):
                exec_times[0] = float(line.split(',')[1])
            elif line.startswith("Parall(overall)"):
                exec_times[1] = float(line.split(',')[1])
            
        #buf = io.StringIO(outs)
        #print(buf.readlines())
        #for line in buf.readlines():
        #    if line.startswith("Physical total"):
        #        exec_times[0] = line.split(',')[1]
        #    elif line.startswith("Parall(overall)"):
        #        exec_times[1] = line.split(',')[1]
        return exec_times
        

# Main program
if __name__ == "__main__":
    workdir = '.'
    num_teams = 4
    src_filename = "src/parallel/main.c"
    temp_src_filename = 'src/parallel/main-4teams.c'
    run_script = 'run_dubinsky.sh'

    nbody_runner = NBodyRunner(workdir, num_teams, src_filename, temp_src_filename, run_script)
    nbody_runner.execute_nbody([60, 60, 60, 60])

#patts = [None] * 4
#patts[0] = r'([\S\s]int THDS0=)\d{1,}(;)'
#patts[1] = r'([\S\s]int THDS1=)\d{1,}(;)'
#patts[2] = r'([\S\s]int THDS2=)\d{1,}(;)'
#patts[3] = r'([\S\s]int THDS3=)\d{1,}(;)'

#pattern = re.compile(r'\(([0-9])*,')
