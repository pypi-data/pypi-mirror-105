Tableau dashboard updater


Install
```sh
pip tableau-client-talenttech-oss
```

```python
from tableau.client import Client

tableau_client = Client(url_server_tableau='https://example.org/',
                        user_name_tableau='',
                        password_tableau=''
                        )
tableau_client.dashboard_refresh('dashboard_name')

```