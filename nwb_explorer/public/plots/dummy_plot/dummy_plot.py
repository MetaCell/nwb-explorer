import json
import pandas as pd
import holoviews as hv
 
def plot_holoviews():
        macro_df = pd.read_csv('http://assets.holoviews.org/macro.csv', '\t')
        key_dimensions = [('year', 'Year'), ('country', 'Country')]
        value_dimensions = [('unem', 'Unemployment'), ('capmob', 'Capital Mobility'),
                            ('gdp', 'GDP Growth'), ('trade', 'Trade')]
        macro = hv.Table(macro_df, key_dimensions, value_dimensions)
        gdp_unem_scatter = macro.to.scatter('Year', ['GDP Growth', 'Unemployment'])
        gdp_unem_scatter.overlay('Country')
        return gdp_unem_scatter
