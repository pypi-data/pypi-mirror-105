from os.path import dirname
import sys
import subprocess

path_file = dirname(dirname(__file__))



def version():

    return subprocess.run([f'poetry', 'version', '-s'], capture_output=True, text=True).stdout.rstrip()

if __name__ == '__main__':
    print(version())