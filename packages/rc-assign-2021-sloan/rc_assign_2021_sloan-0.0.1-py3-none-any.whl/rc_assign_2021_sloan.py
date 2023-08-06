import sqlite3
import pandas as pd
import numpy as np
import time

def dataframe_info(df):
    column_list = list(df.columns)
    rows, cols = df.shape
    print(f"Here are the columns of the dataframe: \n{column_list}")
    print("----------------------------------------\n")
    print(df.info())
    print("----------------------------------------\n")
    print(f"The dataframe has {rows} rows and {cols} columns.\n")
    print("----------------------------------------\n")
    print(df.describe())
    print("----------------------------------------\n")
    print("Here is a preview of the dataframe.")
    print(df.head())
    print("----------------------------------------\n")


def sql_to_df(dbLocation, query):
    try:
        conn = sqlite3.connect(dbLocation)
    except:
        print("Please use legal string argument for the location of the database.")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def df_to_sql(dbLocation, table_name, df):
    unique_part = str(round(time.time()))
    conn = sqlite3.connect(dbLocation)
    new_table_name = table_name+f"_{unique_part}"
    df.to_sql(new_table_name, conn, if_exists='replace', index=False)
    conn.close()
    return new_table_name

def create_table_query(df, table_name):
    query = "CREATE TABLE "+ str(table_name) + "("
    for col in df.columns:
        t = df[col].dtypes.type
        if t is np.int64 or t is np.int32:
            query = query + f"{col} INTEGER, "
        elif t is np.float64 or t is np.float32:
            query = query + f"{col} REAL, "
        elif t is np.object0:
            query = query + f"{col} TEXT, "
        else:
            query = query + f"{col} BLOB, "
    query = query[:-2] + ")"
    print(query)

        
def similar_columns(df1,df2):
    df1 = set(df1)
    df2 = set(df2)
    intersect = df1.intersection(df2)
    return intersect

def percentile(df, N):
    try:
        N = int(N)
    except:
        print("Use an Integer type value for N.")
    if N > 100 or N < 0:
        print("N should be an Integer between 0 and 100.")
        return None
    numeric = df.select_dtypes(include='number')
    col_percentile = []
    for col in numeric.columns:
        arr = np.array(numeric[col])
        percentile = np.percentile(arr, N)
        col_percentile.append((col, round(percentile, 3)))
    return col_percentile

def df_value_greater_than(df, column, value):
    try:
        value = float(value)
    except:
        print("Use a numeric value for arguement value.")
    df_filtered = df[df[column] >= value]
    return df_filtered

def df_value_less_than(df, column, value):
    try:
        value = float(value)
    except:
        print("Use a numeric value for arguement value.")
    df_filtered = df[df[column] <= value]
    return df_filtered
