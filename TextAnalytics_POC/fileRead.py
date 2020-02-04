import os
import pandas as pd

def csvRead(sourceFileName):
    df_data = pd.read_csv(sourceFileName,dtype=str,encoding='cp1252')
    return (df_data)

def txtRead(sourceFileName):
    df_data = pd.read_table(sourceFileName,sep='\t',dtype=str,encoding='cp1252')
    return (df_data)

def xlsxRead(sourceFileName):
    df_data = pd.read_excel(sourceFileName,dtype=str,encoding='cp1252')
    return (df_data)