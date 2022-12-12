from pycountry_convert import country_alpha2_to_continent_code
import pandas as pd

f1 = 'lifeexpectancy1.csv'
df = pd.read_csv(f1)

geo_data = {}
def convert_to_int(s) :
    s = s.strip()
    return float(s)

with open('geo.csv','r') as handler :
    _ = handler.readline()
    for line in handler :
        xs = line.strip('\n').split(',')
        geo_data[xs[0]] = {
            'alpha2' : xs[-5].strip(),
            'alpha3' : xs[-4].strip(),
            'numeric' : int(xs[-3]),
            'latitude' : float(xs[-2].strip()),
            'longitude' : float(xs[-1].strip()),
        }

def get_continent( name ) :
    try :
        return country_alpha2_to_continent_code(name)
    except :
        return 'unk'

# Renamings
df = df.rename(columns={
    'Country' : 'country',
    'literacyrate' : 'literacy_rate',
    'homicidiesper100k' : 'homicidies_per_100k',
    'Schooling' : 'schooling',
    'HIV.AIDS' : 'hiv_aids',
    'Status' : 'status',
    'wateraccess' : 'water_access',
    'healthexppercapita' : 'health_exp_per_capita',
    'fertilityrate' : 'fertility_rate',
    'lifeexp' : 'life_expectancy',
    'gdppercapita' : 'gdp_per_capita',
    'CO2' : 'co2',
    'urbanpop' : 'urban_population',
    'urbanpopgrowth' : 'urban_population_growth'

})


# Roundings
df['country_code'] = df['country'].apply(lambda x : geo_data[x]['alpha2'])
df['country_code_num'] = df['country'].apply(lambda x : geo_data[x]['numeric'])
df['continent'] = df['country_code'].apply(lambda x : get_continent(x))
df['lat'] = df['country'].apply(lambda x : geo_data[x]['latitude'])
df['lon'] = df['country'].apply(lambda x : geo_data[x]['longitude'])

df.to_csv('lifeexpectancy1_trans00.csv')