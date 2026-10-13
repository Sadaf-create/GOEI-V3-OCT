"""Transparent demonstration calculations; no trained ML model."""
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parent

def load_data():
    df = pd.read_csv(ROOT / 'data' / 'regions.csv')
    required = ['region','region_ar','unemployment','poverty','skills','digital','sme','participation']
    if not set(required).issubset(df.columns):
        raise ValueError('regions.csv is missing required columns')
    for col in required[2:]:
        df[col] = pd.to_numeric(df[col], errors='raise')
        if not df[col].between(0, 100).all():
            raise ValueError(f'{col} must contain values from 0 to 100')
    if df.empty or df.region.duplicated().any():
        raise ValueError('The dataset must contain unique, nonempty regions')
    return df

def opportunity(df):
    out = df.copy()
    out['opportunity'] = ((100-out.unemployment*3).clip(0,100)*.25 +
                          (100-out.poverty*2).clip(0,100)*.25 +
                          out.skills*.20 + out.digital*.15 + out.sme*.15).round(1)
    return out

def scenario(unemployment, poverty, budget, training, sme, digital):
    if training+sme+digital != 100:
        raise ValueError('Allocations must total 100%')
    if not 0 <= budget <= 100:
        raise ValueError('Budget must be between 0 and 100 million')
    du = budget*(training*.0009+sme*.0006+digital*.0003)
    dp = budget*(training*.0005+sme*.0008+digital*.0003)
    return max(0,unemployment-du), max(0,poverty-dp)

JOBS = [
    ('Data analyst','محلل بيانات',['Python','SQL','Analytics'],'SQL foundations → Python data analysis','أساسيات SQL ← تحليل البيانات ببايثون'),
    ('Cybersecurity associate','مساعد أمن سيبراني',['Security','Networking','Python'],'Networking → Security fundamentals','الشبكات ← أساسيات الأمن'),
    ('Digital marketing specialist','أخصائي تسويق رقمي',['Marketing','Analytics','Communication'],'Digital campaigns → Marketing analytics','الحملات الرقمية ← تحليلات التسويق'),
    ('SME business coordinator','منسق أعمال المنشآت',['Business','Communication','Analytics'],'Business operations → Financial literacy','إدارة الأعمال ← الثقافة المالية')]

def match(skills):
    rows=[]
    for en,ar,required,path,path_ar in JOBS:
        rows.append(dict(role=en,role_ar=ar,score=round(100*len(set(skills)&set(required))/len(required)),
                         required=required,missing=[x for x in required if x not in skills],path=path,path_ar=path_ar))
    return sorted(rows,key=lambda r:r['score'],reverse=True)
