#!/opt/anaconda/envs/bd9/bin/python3
import sys

def check_str(p_arr):

        if p_arr[0].isdigit()== False:
                return 0
        l_uid = int(p_arr[0])
        if l_uid%256 == 189:

                if len(p_arr) < 3:
                        return False
                if len(p_arr[0])==0 or len(p_arr[1])==0 or len(p_arr[2])==0:
                        return False
                if p_arr[2][:4] != 'http':
                        return False
                try:
                        inNumberfloat = float(p_arr[1])
                except ValueError:
                        return False
                return True
        else:
                return False
def main():

    for line in sys.stdin:

        splitted = line.strip().split("\t")
        if check_str(splitted) == True:
                print(splitted[0]+"\t"+str(int(float(splitted[1])*1000))+"\t"+splitted[2])
    
main()

