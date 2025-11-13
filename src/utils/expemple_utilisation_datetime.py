#Code comparaison de dates
from datetime import datetime, timedelta

def programmer_date_rendu():
    return(datetime.now()+timedelta(weeks = 2))

print(programmer_date_rendu())