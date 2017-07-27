from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import os
import glob
import smopy
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from scipy import ndimage
from datetime import datetime
import imageio

%time df = pd.read_csv('all.csv', index_col=0, parse_dates=['time'])

print(df.head())
print(df.dtype)

