import pandas as pd

def read_from_csv(path, index_col=False):
    df = pd.read_csv(path, index_col=index_col)
    # print('READ FROM CSV\n')
    # print(df)

    return df

def save_to_csv(df, to_path, index=False):
    df.head()
    # print('SAVED TO CSV\n')
    # print(df)
    df.to_csv(to_path, index=index, encoding='UTF-8-SIG')

def save_to_excel(df, writer, sheet_name=None):
    df.head()
    # print(df)
    if not sheet_name:
        df.to_excel(writer, index=False)
    else:
        df.to_excel(writer, sheet_name=sheet_name, index=False)