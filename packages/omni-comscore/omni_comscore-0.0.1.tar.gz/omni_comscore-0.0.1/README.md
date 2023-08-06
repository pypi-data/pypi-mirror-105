# Omnicom media group | Comscore Library

Under construction!

Developed by Carlos Trujillo, Data Analytics Manager from Omnicom Media Group Chile (c) 2021

## Examples (How To Use)

Connection to Comscore data bases

```python
from omni_comscore import comscore_omnicom_api

comscore = comscore_omnicom_api(user = 'user_name', password = 'password_value')

```

Executing the first query to obtain the total visits in time from different domains.
```python

from omni_comscore import comscore_omnicom_api

comscore = comscore_omnicom_api(user = 'user_name', password = 'password_value')

dataframe_time = comscore.domain_by_time(country = 'cl')
```