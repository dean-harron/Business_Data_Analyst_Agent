import pandas as pd
from data.profile import profile_dataframe

def test_profile():
    df=pd.DataFrame({"revenue":[10,20,30],"segment":["A","A","B"]})
    p=profile_dataframe(df)
    assert p["rows"]==3
    assert p["columns"]==2
    assert p["numeric_summary"]["revenue"]["mean"]==20.0
