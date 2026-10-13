"""GOEI / GOIP dashboard prototype based on the supplied GOEI V3 proposal."""
import json
import pandas as pd
import streamlit as st
from core import load_data, opportunity, scenario, match

st.set_page_config(page_title='GOEI | Opportunity Intelligence',page_icon='🌍',layout='wide')
lang=st.sidebar.selectbox('Language / اللغة',['العربية','English'])
ar=lang=='العربية'
def t(en,arabic): return arabic if ar else en
st.markdown('''<style>
.stApp{background:#f5f7f3}h1,h2,h3{color:#174a3a}
[data-testid="stMetric"]{background:white;border:1px solid #dfe8df;border-radius:12px;padding:20px}
[data-testid="stSidebar"]{background:#e9f1e9}
</style>''',unsafe_allow_html=True)
if ar:
    st.markdown('<style>[data-testid="stMainBlockContainer"]{direction:rtl;text-align:right} [data-testid="stSidebar"]{direction:rtl}</style>',unsafe_allow_html=True)
st.sidebar.title('GOEI · GOIP')
st.sidebar.caption(t('Global Opportunity & Economic Inclusion Initiative','المبادرة العالمية للفرص والشمول الاقتصادي'))
labels=[t('Overview','نظرة عامة'),t('Employment observatory','مرصد التوظيف والفقر'),t('Opportunity index','مؤشر الفرصة الاقتصادية'),t('Skills & jobs','المهارات والوظائف'),t('Policy simulator','محاكاة السياسات'),t('Programs & targets','البرامج والمستهدفات'),t('Governance & roadmap','الحوكمة وخارطة الطريق')]
page=st.sidebar.radio(t('Navigation','القائمة'),range(7),format_func=lambda i:labels[i])
try: base=load_data()
except (OSError,ValueError) as e:
    st.error(t('Cannot load data: ','تعذر تحميل البيانات: ')+str(e));st.stop()
region=st.sidebar.selectbox(t('Region','المنطقة'),['all']+base.region.tolist(),format_func=lambda x:t('All regions','جميع المناطق') if x=='all' else (base.set_index('region').loc[x,'region_ar'] if ar else x))
year=st.sidebar.selectbox(t('Demo year','السنة التجريبية'),[2026,2025,2024])
df=base.copy()
df['unemployment']=(df.unemployment+(2026-year)*.35).clip(0,100)
df['poverty']=(df.poverty+(2026-year)*.45).clip(0,100)
if region!='all': df=df[df.region==region]
df=opportunity(df)
st.sidebar.download_button(t('Export regional CSV','تصدير CSV للمناطق'),df.to_csv(index=False).encode('utf-8-sig'),f'GOEI_demo_{year}.csv','text/csv')
st.sidebar.caption(t('No API key or paid service required. Runs locally.','لا يتطلب مفتاح API أو خدمة مدفوعة. يعمل محلياً.'))
st.caption('GOEI / GLOBAL OPPORTUNITY INTELLIGENCE PLATFORM')
st.title(labels[page])
st.warning(t('Synthetic demonstration data. Regional indicators, index weights and simulation effects are illustrative, not official statistics or validated forecasts.','بيانات اصطناعية توضيحية. المؤشرات الإقليمية وأوزان المؤشر ونتائج المحاكاة تجريبية وليست إحصاءات رسمية أو توقعات معتمدة.'))

def metrics():
    cols=st.columns(4)
    for col,label,val in zip(cols,[t('Opportunity / 100','الفرصة / 100'),t('Unemployment','البطالة'),t('Poverty','الفقر'),t('Skills readiness','جاهزية المهارات')],[f'{df.opportunity.mean():.1f}',f'{df.unemployment.mean():.1f}%',f'{df.poverty.mean():.1f}%',f'{df.skills.mean():.0f}%']):
        col.metric(label,val)

def table(data):
    display=data[['region_ar' if ar else 'region','unemployment','poverty','skills','digital','opportunity']].copy()
    display.columns=[t('Region','المنطقة'),t('Unemployment %','البطالة ٪'),t('Poverty %','الفقر ٪'),t('Skills %','المهارات ٪'),t('Digital %','النفاذ الرقمي ٪'),t('Opportunity /100','الفرصة /100')]
    st.dataframe(display,hide_index=True,width='stretch')

if page==0:
    metrics()
    c1,c2=st.columns([2,1])
    with c1:
        st.subheader(t('Employment & poverty landscape','مشهد التوظيف والفقر'))
        chart=df.set_index('region_ar' if ar else 'region')[['unemployment','poverty']]
        chart.columns=[t('Unemployment %','البطالة ٪'),t('Poverty %','الفقر ٪')]
        st.bar_chart(chart,color=['#12694f','#afcfb5'])
    with c2:
        st.subheader(t('Intervention priorities','أولويات التدخل'))
        for row in df.sort_values('opportunity').head(3).to_dict('records'):
            st.write(f"**{row['region_ar'] if ar else row['region']} · {row['opportunity']}/100**")
            st.caption(t('Prioritise skills access and SME support','أولوية لإتاحة المهارات ودعم المنشآت') if row['skills']<65 else t('Expand demand-aligned training','توسيع التدريب المرتبط بالطلب'))
    st.subheader(t('Regional opportunity intelligence','ذكاء الفرص الإقليمي'));table(df)
    st.subheader(t('Five connected pillars','خمس ركائز مترابطة'))
    for c,en,aa in zip(st.columns(5),['Measure','Prepare','Enable','Finance','Scale'],['القياس','التأهيل','التمكين','التمويل','التوسع']):c.info(t(en,aa))
elif page==1:
    metrics()
    q=st.text_input(t('Search region','ابحث عن منطقة'))
    filtered=df[df.region.str.contains(q,case=False,regex=False)|df.region_ar.str.contains(q,regex=False)]
    table(filtered)
    st.info(t('Rates have different denominators and must not be added. Summaries use simple regional means, not population-weighted estimates. Historical years are invented demo variations.','تختلف مقامات المعدلات ولا يجوز جمعها. الملخصات متوسطات بسيطة وليست مرجحة بالسكان. السنوات السابقة تغيرات تجريبية مصطنعة.'))
    st.subheader(t('Data integration pathway','مسار تكامل البيانات'))
    st.write(t('Labour → Income → Education → Business registry → Social protection. Official connectors and harmonised definitions are required for operational use.','العمل ← الدخل ← التعليم ← سجلات المنشآت ← الحماية الاجتماعية. يتطلب التشغيل مصادر رسمية وتعريفات متوافقة.'))
elif page==2:
    st.subheader(t('Transparent scoring model','نموذج حساب شفاف'))
    st.dataframe(pd.DataFrame({t('Component','المكوّن'):[t('Employment','التوظيف'),t('Poverty resilience','مواجهة الفقر'),t('Skills','المهارات'),t('Digital access','النفاذ الرقمي'),t('SME ecosystem','منظومة المنشآت')],t('Weight','الوزن'):['25%','25%','20%','15%','15%'],'Formula':['clip(100 − 3 × unemployment, 0, 100)','clip(100 − 2 × poverty, 0, 100)','skills score','digital score','SME score']}),hide_index=True,width='stretch')
    st.caption(t('The proposal does not prescribe these weights. This demonstration index is not used for eligibility or funding decisions.','لا تحدد الوثيقة هذه الأوزان. المؤشر التجريبي ليس لقرارات الأهلية أو التمويل.'))
    table(df.sort_values('opportunity',ascending=False))
elif page==3:
    skills=st.multiselect(t('Select your skills','اختر المهارات'),['Python','SQL','Analytics','Security','Networking','Marketing','Communication','Business'],default=['Python','SQL'])
    st.caption(t('Explainable matching = selected required skills / total required skills. Sample roles, not live vacancies.','التطابق = المهارات المطلوبة المحددة ÷ جميع المهارات المطلوبة. أدوار نموذجية وليست شواغر فعلية.'))
    for job in match(skills):
        with st.container(border=True):
            st.subheader(f"{job['role_ar'] if ar else job['role']} · {job['score']}%")
            st.progress(job['score']/100)
            st.write(t('Required: ','المطلوب: ')+', '.join(job['required']))
            st.write(t('Missing: ','الناقص: ')+(', '.join(job['missing']) or t('None','لا يوجد')))
            st.info(job['path_ar'] if ar else job['path'])
elif page==4:
    st.write(t('12-month assumption-based scenario. No causal or trained forecasting model is used.','سيناريو لمدة 12 شهراً مبني على افتراضات دون نموذج سببي أو تنبؤي مدرب.'))
    uploaded=st.file_uploader(t('Load saved scenario JSON','تحميل سيناريو JSON محفوظ'),type=['json'])
    if uploaded and st.button(t('Apply saved scenario','تطبيق السيناريو المحفوظ')):
        try:
            s=json.load(uploaded)
            for k in ['training','sme','digital']:
                if type(s[k]) is not int or not 0<=s[k]<=100:raise ValueError('Invalid allocation')
            if not isinstance(s['budget'],(int,float)) or not 0<=s['budget']<=100:raise ValueError('Invalid budget')
            if s['training']+s['sme']+s['digital']!=100:raise ValueError('Allocations must total 100')
            for k in ['training','sme','digital','budget']:st.session_state[k]=float(s[k]) if k=='budget' else s[k]
            st.success(t('Loaded. Region and year remain selected in the sidebar.','تم التحميل. المنطقة والسنة وفق اختيار القائمة الجانبية.'))
        except (KeyError,ValueError,TypeError) as e:st.error(str(e))
    c1,c2=st.columns(2)
    with c1:
        training=st.slider(t('Skills & training %','المهارات والتدريب ٪'),0,100,40,key='training')
        sme=st.slider(t('SME support %','دعم المنشآت ٪'),0,100,30,key='sme')
        digital=st.slider(t('Digital access %','النفاذ الرقمي ٪'),0,100,30,key='digital')
        budget=st.number_input(t('Budget in USD millions','الميزانية بمليون دولار'),0.,100.,10.,key='budget')
        st.caption(f"{t('Total allocation','إجمالي التخصيص')}: {training+sme+digital}%")
    with c2:
        try:
            u,p=scenario(df.unemployment.mean(),df.poverty.mean(),budget,training,sme,digital)
            st.metric(t('Simulated unemployment','البطالة التجريبية'),f'{u:.2f}%',f'{u-df.unemployment.mean():.2f} pp',delta_color='inverse')
            st.metric(t('Simulated poverty','الفقر التجريبي'),f'{p:.2f}%',f'{p-df.poverty.mean():.2f} pp',delta_color='inverse')
            saved=dict(training=training,sme=sme,digital=digital,budget=budget,region=region,year=year,unemployment=u,poverty=p,dataset='synthetic demo')
            st.download_button(t('Save scenario JSON','حفظ السيناريو JSON'),json.dumps(saved,ensure_ascii=False,indent=2).encode('utf-8'),'GOEI_scenario.json','application/json')
        except ValueError as e:st.error(t(str(e),'يجب أن يبلغ مجموع التخصيص 100٪'))
    with st.expander(t('Model assumptions','افتراضات النموذج')):
        st.code('Δ unemployment (pp) = budget × (0.0009 × training% + 0.0006 × SME% + 0.0003 × digital%)\nΔ poverty (pp) = budget × (0.0005 × training% + 0.0008 × SME% + 0.0003 × digital%)')
        st.write(t('Invented coefficients require empirical calibration. Rates are capped at zero. No funding is committed.','معاملات تجريبية تتطلب معايرة فعلية. لا تنخفض المعدلات عن الصفر. لا يتم الالتزام بتمويل.'))
elif page==5:
    st.info(t('Source targets are proposed ambitions, not validated forecasts. Baseline is 0 in 2026. Funding and approvals are not secured; no achievement data supplied.','المستهدفات طموحات مقترحة وليست توقعات معتمدة. خط الأساس صفر في 2026. التمويل والموافقات غير مؤمنة ولم تقدم بيانات إنجاز.'))
    targets=[('Partner countries','الدول الشريكة','10','2030'),('Skills beneficiaries','مستفيدو المهارات','250,000','2033'),('SMEs supported','المنشآت المدعومة','25,000','2033'),('Research outputs','المخرجات البحثية','100','2032'),('Inclusion-linked capital','رأس المال المرتبط بالشمول','$500M','2035'),('Institutional partnerships','الشراكات المؤسسية','20','2030')]
    for start in [0,3]:
        for c,r in zip(st.columns(3),targets[start:start+3]):c.metric(t(r[0],r[1]),r[2]);c.caption(t('Proposed by ','مقترح بحلول ')+r[3])
    st.subheader(t('Program portfolio','محفظة البرامج'))
    for en,aa in [('Employment & poverty observatory','مرصد التوظيف والفقر'),('Future skills & workforce transformation','مهارات المستقبل وتحول القوى العاملة'),('Entrepreneurship & SME development','ريادة الأعمال وتنمية المنشآت'),('Investment & economic inclusion','الاستثمار والشمول الاقتصادي'),('Innovation & digital transformation','الابتكار والتحول الرقمي')]:st.write('◈ '+t(en,aa))
else:
    st.subheader(t('Implementation roadmap','خارطة الطريق'))
    for years,en,aa,desc,dar in [('2026–2027','Foundation','التأسيس','Institutional approval, methodology, initial partnership MoUs','الاعتماد المؤسسي والمنهجية ومذكرات التفاهم الأولى'),('2028–2030','Build','البناء','GOIP pilot, observatory and two national pilots','منصة تجريبية ومرصد وتطبيقان وطنيان'),('2031–2033','Scale','التوسع','Regional expansion, blended finance and skills pathways','توسع إقليمي وتمويل مختلط ومسارات مهارات'),('2034–2035','Institutionalise','المأسسة','Independent evaluation and permanent research consortium','تقييم مستقل وتحالف بحثي دائم')]:
        with st.container(border=True):st.write(f'**{years} · {t(en,aa)}**');st.write(t(desc,dar))
    st.subheader(t('Governance','الحوكمة'))
    st.write(t('International advisory board → policy direction\n\nScientific committee → methodology and independent evaluation\n\nUniversity delivery unit → programs, partnerships and reporting','مجلس استشاري دولي ← توجيه السياسات\n\nلجنة علمية ← المنهجية والتقييم المستقل\n\nوحدة تنفيذ جامعية ← البرامج والشراكات والتقارير'))
    st.subheader(t('Risk register','سجل المخاطر'))
    st.dataframe(pd.DataFrame({t('Risk','المخاطرة'):[t('Data comparability','قابلية مقارنة البيانات'),t('Algorithmic bias','التحيز الخوارزمي'),t('Partner volatility','تذبذب التزام الشركاء'),t('Funding continuity','استمرارية التمويل'),t('Overstated attribution','المبالغة في نسب الأثر')],t('Level','المستوى'):['High','Medium','Medium','Medium','High'],t('Mitigation','المعالجة'):[t('Validated definitions and confidence limits','تعريفات معتمدة وحدود الثقة'),t('Independent audit and human oversight','تدقيق مستقل وإشراف بشري'),t('Modular program design','برامج مستقلة قابلة للتكامل'),t('Diversified financing','تنويع التمويل'),t('Independent pre-registered evaluation','تقييم مستقل مسجل مسبقاً')]}),hide_index=True,width='stretch')
    st.caption(t('Based on the attached GOEI V3 revised paper proposed to King Khalid University. Initiative lead: Dr. Abeer Alalmaie. Independent prototype; no institutional endorsement implied.','مبني على وثيقة GOEI V3 المقترحة لجامعة الملك خالد. قائدة المبادرة د. عبير الالمعي. نموذج مستقل لا يعني اعتماداً مؤسسياً.'))
st.divider()
st.caption(t('GOEI / GOIP · Prototype V3 · Synthetic data · Human-led decisions','GOEI / GOIP · نموذج V3 · بيانات اصطناعية · قرارات بإشراف بشري'))
