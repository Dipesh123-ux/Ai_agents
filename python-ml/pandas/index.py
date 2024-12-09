# Pandas

# Userful for data processing and analysis 

#  pandas dataframe is 2d tabular data structure with labeled axes (rows and columns)

import pandas as pd
from sklearn import datasets
import numpy  as np


cal = datasets.fetch_california_housing()

cal_df = pd.DataFrame(cal.data,columns=cal.feature_names)

print(cal_df.head(),cal_df.shape)


# importing csv files 

diabetes_df = pd.read_csv('./diabetes.csv')

print(diabetes_df.head())

cal_df.to_csv('calfornia.csv')

# exporting the pandas datafrom to an excel

cal_df.to_excel('california.xlsx')

## creating  a df with random values

random = pd.DataFrame(np.random.rand(20,10))

print(random.head())


