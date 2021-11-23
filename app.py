import pandas as pd 

def print_output_html():
    data=pd.read_csv('data.csv')
    data.to_html('output.html')

if __name__=="__main__":
    print_output_html()