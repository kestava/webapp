import subprocess

class Database(object):
    
    @staticmethod
    def execute(cmd):
        print(cmd)
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = p.communicate()
        if not result[0] == '':
            print('Result: {0}'.format(result[0]))