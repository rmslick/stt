
class Quaternion:
    def __init__(self, r,i,j,k):
        # [0,1,2,3] <-> [r, i, j, k]
        self.q = [r,i,j,k] 
    def __getitem__(self,key):
        #return self.q[key] for testing on matlab
        return self.q[key-1]
    def __setitem__(self,key,value):
        #return self.q[key] for testing on matlab
        self.q[key-1] = value