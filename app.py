import pandas as pd 

def print_output_html():
    data=pd.read_csv('data.csv')
    columns=data.columns
    data.drop([columns[0]], axis=1, inplace=True)
    data.to_html('output.html')

    pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>

    html_string = """
    <html>
    <head><title>HTML Pandas Dataframe with CSS</title></head>
    <link rel="stylesheet" type="text/css" href="df_style.css"/>
    <body>
        {table}
    </body>
    </html>.
    """


    # OUTPUT AN HTML FILE
    with open('output.html', 'w') as f:
        f.write(html_string.format(table=data.to_html(classes='mystyle')))
    
if __name__=="__main__":
    print_output_html()