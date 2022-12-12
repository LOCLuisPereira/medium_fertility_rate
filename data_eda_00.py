import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data




st.set_page_config(
    page_title = 'Fertility Rate EDA',
    layout='wide'
)




FILE = 'lifeexpectancy1_trans00.csv'
df = pd.read_csv(FILE)





def geo_graphics(key=0) :

    source = alt.topo_feature(data.world_110m.url, "countries")

    background = alt.Chart(source).mark_geoshape(fill="white")

    final_map = lambda x : (
        (background + x)
        .configure_view(strokeWidth=0)
        .properties(width=700, height=400)
        .project("naturalEarth1")
    )




    option = st.selectbox('Metric.', [
            'Life Expectancy',
            'GDP Per Capita',
            'Economic Inflation',
            'Health Expense Per Capity',
            'Fertility Rate',
            'Electricity Distribution',
            'Water Access',
            'CO2 levels',
            'Internet Access',
            'Education',
            'Literacy Rate',
            'HIV',
            'Tuberculosis',
            'Homicides Per 100k',
            'Forest Density',
            'Urban Population Density',
            'Urban Population Growth'
        ],
        key = key
    )




    # TODO: Use a dictionary here. The goal was to add one or two, but in the end, ended up will the whole set
    if option == 'Literacy Rate' :
        xgraph = 'literacy_rate'

    elif option == 'Homicides Per 100k' :
        xgraph = 'homicidies_per_100k'

    elif option == 'Electricity Distribution' :
        xgraph = 'electricity'

    elif option == 'Education' :
        xgraph = 'schooling'

    elif option == 'HIV' :
        xgraph = 'hiv_aids'

    elif option == 'Water Access' :
        xgraph = 'water_access'

    elif option == 'Tuberculosis' :
        xgraph = 'tuberculosis'

    elif option == 'Economic Inflation' :
        xgraph = 'inflation'

    elif option == 'Health Expense Per Capity' :
        xgraph = 'health_exp_per_capita'

    elif option == 'Fertility Rate' :
        xgraph = 'fertility_rate'

    elif option == 'Life Expectancy' :
        xgraph = 'life_expectancy'

    elif option == 'Internet Access' :
        xgraph = 'internet'

    elif option == 'GDP Per Capita' :
        xgraph = 'gdp_per_capita'

    elif option == 'CO2 levels' :
        xgraph = 'co2'

    elif option == 'Forest Density' :
        xgraph = 'forest'

    elif option == 'Urban Population Density' :
        xgraph = 'urban_population'

    elif option == 'Urban Population Growth' :
        xgraph = 'urban_population_growth'


    mask = (
        alt.Chart(source)
        .mark_geoshape(stroke="black", strokeWidth=0.75)
        .encode(
            color=alt.Color(
                f"{xgraph}:Q",
                title='Life Expenctancy'
            ),
            tooltip=[
                alt.Tooltip("country_code:N", title="Country"),
                alt.Tooltip(f"{xgraph}:Q", title="Life Expentacy"),
            ],
        ).transform_lookup(
            lookup="id",
            from_=alt.LookupData(df, "country_code_num", [xgraph, "country_code"]),
        )
    )
    st.altair_chart(final_map(mask), use_container_width=True)









# DATASET CONSTITUTION KPIs
st.title('World Data Analysis')
st.write('Dataset statistics.')
x,y,z = st.columns(3)
with x :
    st.metric(
        label='Countries',
        value=df['country'].count()
    )
with y :
    st.metric(
        label='Continents',
        value=len(df[df['continent'].notnull()].continent.unique())
    )
with z :
    st.metric(
        label='Developing Countries Ratio',
        value=f"{round((len(df[df.status == 'Developing'].status) + 1) / len(df.status)*100,1)} %"
    )




# GEOGRAPHIC INFOGRAPH SHOWING
st.title('Geographical Info Show')
st.write('Choose comparing mode to open a side-by-side world map.')
comparing_mode = st.selectbox('Comparing Mode', ['No', 'Yes'])

if comparing_mode == 'Yes' :
    left, right = st.columns(2)
    with left : geo_graphics(0)
    with right : geo_graphics(1)
else : geo_graphics()







xcol, ycol, zcol = st.columns(3)

with xcol :
    st.header('Life Expectancy')
    scatter_exp_fert = alt.Chart(df).mark_circle(size=30).encode(
        x='life_expectancy:Q',
        y='fertility_rate:Q',
        tooltip=['country', 'life_expectancy', 'fertility_rate']
    ).configure_mark(
        color='red'
    ).interactive()
    st.altair_chart(scatter_exp_fert, use_container_width=True)

with ycol :
    st.header('GDP')
    scatter_exp_fert = alt.Chart(df).mark_circle(size=30).encode(
        x='gdp_per_capita:Q',
        y='fertility_rate:Q',
        tooltip=['country', 'gdp_per_capita', 'fertility_rate']
    ).configure_mark(
        color='red'
    ).interactive()
    st.altair_chart(scatter_exp_fert, use_container_width=True)

with zcol :
    st.header('Status')
    df_ = df[['status', 'fertility_rate']].replace({'Leastdeveloped':'Developing'})
    df_ = df_.groupby('status').mean().reset_index()

    gp = alt.Chart(df_).mark_bar().encode(
        x=alt.X('status', axis=alt.Axis(labelAngle=0)),
        y='fertility_rate',
    ).configure_mark(
        color='red'
    ).interactive()
    st.altair_chart(gp,use_container_width=True)




xcol, ycol, zcol = st.columns(3)

with xcol :
    st.header('Health Expenses')
    gp = alt.Chart(df).mark_circle(size=30).encode(
        x='health_exp_per_capita:Q',
        y='fertility_rate:Q',
        tooltip=['country', 'health_exp_per_capita', 'fertility_rate']
    ).configure_mark(
        color='red'
    ).interactive()
    st.altair_chart(gp,use_container_width=True)
with ycol :
    st.header('Tuberculosis')
    gp = alt.Chart(df).mark_circle(size=30).encode(
        x='tuberculosis:Q',
        y='fertility_rate:Q',
        tooltip=['country', 'tuberculosis', 'fertility_rate']
    ).configure_mark(
        color='red'
    ).interactive()
    st.altair_chart(gp,use_container_width=True)
with zcol :
    st.header('HIV')
    gp = alt.Chart(df).mark_circle(size=30).encode(
        x='hiv_aids:Q',
        y='fertility_rate:Q',
        tooltip=['country', 'hiv_aids', 'fertility_rate']
    ).configure_mark(
        color='red'
    ).interactive()
    st.altair_chart(gp,use_container_width=True)




xcol, ycol = st.columns(2)

with xcol :
    st.header('Literacy Rate')
    gp = alt.Chart(df).mark_circle(size=30).encode(
        x='literacy_rate:Q',
        y='fertility_rate:Q',
        tooltip=['country', 'literacy_rate', 'fertility_rate']
    ).configure_mark(
        color='red'
    ).interactive()
    st.altair_chart(gp,use_container_width=True)
with ycol :
    st.header('Internet')
    gp = alt.Chart(df).mark_circle(size=30).encode(
        x='internet:Q',
        y='fertility_rate:Q',
        tooltip=['country', 'internet', 'fertility_rate']
    ).configure_mark(
        color='red'
    ).interactive()
    st.altair_chart(gp,use_container_width=True)




st.header('Final Thoughts')

st.write('''
To build this analysis, first we took a dataset from Kaggle about life expectancy (link on the bottom of the page). But instead of analyzing how many years a human being lives according to the country he was born, we chose to focus on the newborn counterpart.

On our analyzis, we see a lot of negative correlations, some neutral ones and zero positive correlations. In other words, almost all factors lead to people having less children.

In our data, we found that women in developed countries tend to have 1.4 children, while on still devoloping countries they tend have 2.3 children. On the economic side, GDP abruptly afftects the fertility-rate. Contries with fewer gross domestic products have the higher amount of children. Here, the correlation consists on the fact that small increments on GDP have a heavy impact on the number of expected babies.

In terms of life expectancy, the more years one is expected to live, the less children one will bear.

When looking at health related metrics, we find that investing in health results in less expected children. Tuberculosis and HIV have no real influence on the fertility rate. As a side note, the country with biggest levels of HIV is also the country with the higher fertility rate. This hints that people are prone to have unprotected sex, which in turn hints us that the majority of children are not planned.

Following a similar path, we have a literacy rate and an internet access relating negatively with the expected number of children.
''')

st.header('Who am I?')
st.write('''
Hi, I am Luis Pereira and you can find me on Medium
(https://medium.com/@luiscavacapereira) and LinkedIn (https://www.linkedin.com/in/luiscavacapereira/).
''')

st.header('Dataset')
st.write('''
https://www.kaggle.com/datasets/kacperk77/life-expectancy
''')