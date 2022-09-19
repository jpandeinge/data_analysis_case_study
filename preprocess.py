import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.experimental import enable_iterative_imputer
from sklearn.base import TransformerMixin
from sklearn.impute import IterativeImputer


from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler, RobustScaler


@st.experimental_singleton
def get_data():
    file_path = 'data/Data_Analyst_Case_Study_Data.xlsx'
    df = pd.read_excel(file_path)
    return df

# a function to map the month to a number

@st.experimental_singleton
def month_to_num(DataFrame):
    # map the month column to month index
    month_dict = dict(jan=1, feb=2, mar=3, apr=4, may=5, jun=6,
                      jul=7, aug=8, sep=9, oct=10, nov=11, dec=12)
    DataFrame['month'] = DataFrame['month'].map(month_dict)
    return DataFrame

@st.experimental_singleton
# impute missing values
class CustomImputer(TransformerMixin):
    def __init__(self, cols=None, strategy='mean'):
        self.cols = cols
        self.strategy = strategy

    def transform(self, df):
        X = df.copy()
        impute = IterativeImputer(max_iter=10, random_state=0)
        if self.cols == None:
            self.cols = list(X.columns)
        for col in self.cols:
            if X[col].dtype == np.dtype('O'):
                X[col].fillna(X[col].value_counts().index[0], inplace=True)
            else:
                X[col] = impute.fit_transform(X[[col]])

        return X

    def fit(self, *_):
        return self


    

@st.experimental_singleton
# create a function to clean the data
def clean_data(df):
    # 1. remove spaces from column names
    df.columns = df.columns.str.replace(' ', '')
    # 2.  remove spaces at the end of values in all columns
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    # 3. # Let's replace 'nan' and spaces with np.nan
    df.replace('', np.nan, inplace=True)
    df.replace('nan', np.nan, inplace=True)
    # use the month_to_num function to map the month to a number
    df = month_to_num(df)
    # 4.  impute missing values
    call = CustomImputer()
    df = call.fit_transform(df)
    return df


def scaling_data(self):
    std_scaler = StandardScaler()
    self.df = clean_data(get_data())

    # scale the numerical columns
    self.df['scaled_balance'] = std_scaler.fit_transform(self.df[['balance']])
    self.df['scaled_duration'] = std_scaler.fit_transform(self.df[['duration']])

    self.df.drop(['balance', 'duration'], axis=1, inplace=True)

    scaled_balance = self.df['scaled_balance']
    scaled_duration = self.df['scaled_duration']

    self.df.drop(['scaled_balance', 'scaled_duration'], axis=1, inplace=True)
    self.df.insert(4, 'scaled_balance', scaled_balance)
    self.df.insert(10, 'scaled_duration', scaled_duration)

    return self.df

def encoding_data(self, df):
    # encode the categorical columns
    le = LabelEncoder()
    self.df = scaling_data(self)
    for col in self.df.columns:
        # select columns that are not numerical
        try:
            if self.df[col].dtype == np.dtype('O'):
                self.df[col] = le.fit_transform(self.df[col])
        except:
            pass

    return self.df

@st.experimental_singleton
# create a function to clean the data
def clean_data_more(df):
    # 1. import the clean_data function
    df = clean_data(df)
    # 2.  scale the numerical columns
    df = scaling_data(df)
    # 3.  encode the categorical columns
    df = encoding_data(df)
    return df

# create a function to split the data