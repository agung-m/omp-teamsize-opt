import subprocess
import re
from threading import Thread
from subprocess_timeout_task import SubprocessTimeoutTask


class NBodyRunner:
    def __init__(self, workdir, num_teams, src_filename, temp_src_filename, \
                    run_script, build_script, cleanup_script, \
                    exe="bin/barneshut-p", dataset="datasets/dubinski", \
                    timestep=0.00001):
        self.workdir = workdir
        self.num_teams = num_teams
        self.main_src = self.workdir + '/' + src_filename
        self.run_script = self.workdir + '/' + run_script
        self.build_script = self.workdir + '/' + build_script
        self.cleanup_script = self.workdir + '/' + cleanup_script
        
        self.dataset = dataset
        self.timestep = timestep
        self.exe = exe
        self.run_cmd = [self.exe, self.dataset, str(self.timestep)]
        #print(" [NBodyRunner] cmd = {}".format(self.run_cmd))

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

    def build_nbody(self):
        return subprocess.call([self.build_script])

    def clean_outputs(self):
        return subprocess.call([self.cleanup_script])
        
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

    def execute_nbody_alt(self, params, timeout=None):
        exec_times = [None] * 2
        params = params.tolist()
        self.modify_src(params)
        command = [self.run_script]
        print(">> [NBodyRunner] team sizes: {}".format(params))
        #process = subprocess.run(command, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        # subprocess call for Python 2.7.x
        process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1)
        with process.stdout:
            for line in iter(process.stdout.readline, b''):
                line = line.decode("utf-8").rstrip()
                #print(line)
                if line.startswith("Physical total"):
                    exec_times[0] = float(line.split(',')[1])
                elif line.startswith("Parall(overall)"):
                    exec_times[1] = float(line.split(',')[1])
        
        # Finish sucessfully or failed after timeout (in seconds)
        try:
            ret = process.wait(timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            ret = -1;
        
        # Exec time can be None if ret_code != 0
        print("<< [NBodyRunner] ret_code: {}, exec_times: {}".format(ret, exec_times))
        #exec_time = float(process.stdout)
        return exec_times

    def execute_nbody_check(self, params, timeout=None):
        exec_times = [None] * 2
        self.modify_src(params)
        command = [self.run_script]
        print(">> [NBodyRunner] team sizes: {}".format(params))
        p = None
        try:
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, bufsize=1)
            #out, err = p.communicate(timeout=timeout)
            with p.stdout:
                for line in iter(p.stdout.readline, b''):
                    line = line.decode("utf-8").rstrip()
                    #print(line)
                    if line.startswith("Physical total"):
                        exec_times[0] = float(line.split(',')[1])
                    elif line.startswith("Parall(overall)"):
                        exec_times[1] = float(line.split(',')[1])
    
            ret = p.wait(timeout)
            print("<< [NBodyRunner] ret_code: {}, exec_times: {}".format(ret, exec_times))
        except subprocess.TimeoutExpired:
            print("(-) Timeout error!")
            if p:
                p.kill()
                p.communicate()
        except subprocess.SubprocessError as se:
            print("(-) Subprocess error: {}".format(se))
            if p:
                p.kill()
                p.communicate()
        except OSError as e:
            print("(-) Failed to run shell: {}".format(e))
            
        return exec_times 
    
    def execute_nbody_check_output(self, params, timeout=None):
        exec_times = [None] * 2
        self.modify_src(params)
        command = [self.run_script]
        print(">> [NBodyRunner] team sizes: {}".format(params))
        try:
            out = subprocess.check_output(command, universal_newlines=True, timeout=timeout)
            #out, err = p.communicate(timeout=timeout)
            #lines = str(out).splitlines()
            for line in out.splitlines():
                #line = line.decode("utf-8").rstrip()
                #print(line)
                if line.startswith("Physical total"):
                    exec_times[0] = float(line.split(',')[1])
                elif line.startswith("Parall(overall)"):
                    exec_times[1] = float(line.split(',')[1])
    
            print("<< [NBodyRunner] exec_times: {}".format(exec_times))
        except subprocess.TimeoutExpired:
            print("(-) Timeout error!")
            #if p:
            #    p.kill()
            #    p.communicate()
        except subprocess.SubprocessError as se:
            print("(-) Subprocess error: {}".format(se))
            #if p:
            #    p.kill()
            #    p.communicate()
        #except OSError as e:
        #    print("(-) Failed to run shell: {}".format(e))
            
        return exec_times 
    
    def execute_nbody_monitor(self, params, timeout=None):
        exec_times = [None] * 2
        self.modify_src(params)
        # Call build script
        ret = self.build_nbody()
        if ret != 0:
            print("[-] Build fails!")
            return exec_times
        
        #command = [self.run_script]
        #command = [self.exe, self.dataset, str(self.timestep)]
        print(">> [NBodyRunner] team sizes: {}".format(params))
        
        # Timeout monitor
        mon = SubprocessTimeoutTask(timeout)
        #t = Thread(target = mon.run, args=(p,))
        t = Thread(target = mon.run)
        t.start()
        try:
            #p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
            p = subprocess.Popen(self.run_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
            
            mon.setSubprocess(p)
            #out, err = p.communicate(timeout=timeout)
            with p.stdout:
                for line in iter(p.stdout.readline, b''):
                    #line = line.decode("utf-8").rstrip()
                    #print(line)
                    if line.startswith(b'Physical total'):
                        s = line.decode('utf-8').rstrip()
                        exec_times[0] = float(s.split(',')[1])
                    elif line.startswith(b'Parall(overall)'):
                        s = line.decode('utf-8').rstrip()
                        exec_times[1] = float(s.split(',')[1])
    
            ret = p.wait()
            print("<< [NBodyRunner] ret_code: {}, exec_times: {}".format(ret, exec_times))
            mon.stop()
            # Call cleanup script
            self.clean_outputs()

        except subprocess.SubprocessError as se:
            print("(-) Subprocess error: {}".format(se))
            if p:
                p.kill()
                p.wait()
            
        t.join()
        return exec_times 


# Main program
if __name__ == "__main__":
    workdir = '.'
    num_teams = 4
    src_filename = "src/parallel/main.c"
    temp_src_filename = 'src/parallel/main-4teams.c'
    run_script = 'run_dubinsky.sh'
    build_script = 'build_dubinsky.sh'

    nbody_runner = NBodyRunner(workdir, num_teams, src_filename, temp_src_filename, run_script, build_script)
    nbody_runner.execute_nbody([60, 60, 60, 60])

#patts = [None] * 4
#patts[0] = r'([\S\s]int THDS0=)\d{1,}(;)'
#patts[1] = r'([\S\s]int THDS1=)\d{1,}(;)'
#patts[2] = r'([\S\s]int THDS2=)\d{1,}(;)'
#patts[3] = r'([\S\s]int THDS3=)\d{1,}(;)'

#pattern = re.compile(r'\(([0-9])*,')
