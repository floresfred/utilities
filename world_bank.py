import pandas as pd


def urban_population_pct_total():

    title = 'Urban population (% of total population)'
    data_dir = r'C:\Users\fredf\Documents\data\world_bank\Data_Extract_From_Population_estimates_and_projections'
    file_name = r'\47619949-c652-4d27-9a3e-77655a978619_Data.csv'

    wb = pd.read_csv(data_dir + file_name)
    wb = wb.dropna(subset=['Country Code'], axis=0)
    ctry = wb[['Country Name', 'Country Code']]
    wb = wb.drop(columns=['Country Code', 'Series Name', 'Series Code'])
    wb = wb.set_index('Country Name')
    wb = wb.rename(columns={s: pd.to_datetime(int(s[:4]), format='%Y') + pd.offsets.YearEnd(0) for s in wb.columns})
    wb = wb.T

    for c in ctry['Country Name']:
        wb[c] = pd.to_numeric(wb[c], errors='coerce')

    return wb