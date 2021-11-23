import pandas as pd 

def print_output_html():
    data=pd.read_csv('data.csv')
    columns=data.columns
    data.drop([columns[0]], axis=1, inplace=True)
    data.to_html('output.html')

if __name__=="__main__":
    print_output_html()
