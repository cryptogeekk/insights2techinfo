import pandas as pd 
from datetime import datetime
from string import Template

def print_output_html():
    data=pd.read_csv('data.csv')
    columns=data.columns
    data.drop([columns[0]], axis=1, inplace=True)
    data.to_html('output.html')

    pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>

    time_updated = datetime.utcnow()


    html_string = """\
    <html>
    <head><title>Researcher List</title>
    <h1>Highly Cited Computer Science Researcher According to WoS 2021</h1>
    <p>Dataset last updated on $code</p>
    <p>The original list published by WoS only contains few metrics such as name, affillation. 
    But in our database we have used ten different metrics to make researchers information more informative.
    </p>
    </head>
    <link rel="stylesheet" type="text/css" href="df_style.css"/>
    <body>
        {table}
    </body>
    </html>.
    """
    string_html1=Template(html_string).safe_substitute(code=time_updated)

    # OUTPUT AN HTML FILE
    with open('output.html', 'w') as f:
        f.write(string_html1.format(table=data.to_html(classes='mystyle')))
    
if __name__=="__main__":
    print_output_html()
