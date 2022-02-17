#berlin

class index(object):
    def __init__(self,root):
        self.root = root

    def grab(self,fl):
        import os
        import pandas as pd
        
        fl = os.path.join(self.root,fl)
        print("Importing {:s}".format(fl))
        return pd.read_csv(fl)
    
