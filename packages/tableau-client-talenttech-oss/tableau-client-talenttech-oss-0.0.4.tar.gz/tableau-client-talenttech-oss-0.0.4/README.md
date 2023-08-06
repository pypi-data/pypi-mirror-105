Tableau dashboard client


Install
```sh
pip tableau-client-talenttech-oss
```

```python
from tableau.client import Client

#initial connection to server tableau
tableau_client = Client(url_server_tableau='https://example.org/',
                        user_name_tableau='',
                        password_tableau=''
                        )

# update extract refresh for tableau workbook
# workbook_name - name published tableau workbook on server
tableau_client.dashboard_refresh(workbook_name ='workbook_name')

# export sheet tableau workbook to csv file
# sheet_name - name worksheet in tableau workbook (workbook_name)
# csv_path - path with file name to save sheet_name to csv 
tableau_client.view_to_csv(workbook_name='',
                           sheet_name='',
                           csv_path='./view_data.csv'
                           )
```