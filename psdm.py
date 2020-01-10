from tqdm import *
import time  
with tqdm(range(100), ncols=90) as t:
    for i in t:
        time.sleep(0.01)