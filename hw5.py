from typing import Union,Tuple
import pathlib
import pandas as pd
import numpy as np
from validate_email import validate_email
import matplotlib.pyplot as plt


class QuestionnaireAnalysis:


    def __init__(self, data_fname: Union[pathlib.Path, str]):
        if type(data_fname) == str:
            self.data_fname = pathlib.Path(data_fname)     
        else:
            
            self.data_fname = data_fname
        if not self.data_fname.exists():
            raise ValueError("Path does not exist")
        self.data = None
        

    def read_data(self):
        self.data = pd.read_json(self.data_fname,orient = 'columns')
        

    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        x =  self.data['age']
        (hist, edges, patches) = plt.hist(x, bins=range(0,110,10), label='hst')
        return(hist.astype(int), edges)  
      
    def remove_rows_without_mail(self) -> pd.DataFrame:
        self.data['is_valid_email'] =  self.data['email'].apply(lambda x:validate_email(x) and "." in x[-4:])
        a = (self.data.index[ self.data['is_valid_email'] == False].tolist())
        self.data =  self.data.drop(index=a,columns =['is_valid_email'] )
        self.data =  self.data.reset_index(drop=True)
        return self.data

    def fill_na_with_mean(self) -> Union[pd.DataFrame, np.ndarray]:
        df1 =  self.data.loc[:,'q1':'q5']
        row_num= pd.isnull( self.data.loc[:,'q1':'q5']).any(1).to_numpy().nonzero()[0]
        df1 = df1.apply(lambda row: row.fillna(row.mean()), axis=1)
        self.data.update(df1)
        return (self.data,row_num)

        




        

