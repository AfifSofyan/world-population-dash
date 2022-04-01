import html as html
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

pop = pd.read_csv('dataset/WPP2019_TotalPopulationBySex.csv')       # original dataset of WPP 2019
pop.PopTotal *= 1000        # The original population data is in a thousand unit
pop.PopMale *= 1000
pop.PopFemale *= 1000
pop = pop.rename(columns={'Time' : 'Year',
                          'PopTotal' : 'Population',
                          'Location' : 'Country'
                          })

coun_list = pd.read_csv('dataset/data_csv.csv')                     # a dataset of country names

pop_coun = pop[pop['Country'].isin(coun_list['Name'])]             # to exclude non-country data

pop_coun_rank = pop_coun.sort_values(by=['Year', 'Population'], ascending=[True, False]) # largest country dataframe

non = coun_list[~coun_list['Name'].isin(pop['Country'])]           # to figure out countries without population data

pop_world = pop[pop['Country'] == 'World']                         # dataframe for world category only
fig1 = px.line(pop_world, x='Year', y='Population', color='Variant')  # world population graph
fig1.update_xaxes(title=None)
fig1.update_yaxes(title=None)
fig1.update_layout(autosize=False,
                   height=242,
                   margin=dict(
                       l=0,
                       r=0,
                       b=30,
                       t=20,
                       pad=0
                       ))


app = Dash(__name__)


app.layout = html.Div(style={'font-family': 'Helvetica'},
                      children=[
                          # This is the part of page title
                          html.Div(
                              children=[
                                  html.H1(children='World Population Growth from 1950 to 2100',
                                          style={'margin-bottom': '10px',
                                                 'font-size': '25px'
                                                 }),
                                  html.P(children='This is a visualization project for the work of "World Population '
                                                  'Prospects 2019" by the United Nations',
                                         style={'margin-top': '10px',
                                                'font-size': '15px'
                                                }),
                              ],
                              style={'height': '80px',
                                     'background-color': 'gray',
                                     'color': 'white',
                                     'padding-top': '15px',
                                     'padding-left' : '20px',

                                     }
                          ),

                          # This is the end of part of page title

                          html.Div(
                              className='row',
                              style={'padding-top' : '30px',
                                     'padding-left' : '20px',
                                     'padding-right' : '20px'
                                     },
                              children=[
                                  html.Div(
                                      className='col-md-6',
                                      children=[
                                          html.H3(children='Top 20 Largest Country by Time',
                                                  style={'text-align': 'left',
                                                         'font-weight': 'bold',
                                                         'font-size': '15px'
                                                         }),
                                          dcc.Graph(id='pop-coun-rank-graph'),
                                          html.Div(
                                              className='row',
                                              children=[
                                                  html.Div(
                                                      className='col-md-6',
                                                      children=[
                                                          html.H5(children='Select Year',
                                                                  style={'margin-bottom': '10px',
                                                                         'margin-top': '10px'
                                                                         }),
                                                          dcc.Dropdown(
                                                              options=list(pop_coun_rank['Year'].unique()),
                                                              value=2019,
                                                              id='year-rank-graph')
                                                      ]

                                                  ),
                                                  html.Div(
                                                      className='col-md-6',
                                                      children=[
                                                          html.H5(children='Select Variant',
                                                                  style={'margin-bottom': '10px',
                                                                         'margin-top': '10px'
                                                                         }),
                                                          dcc.Dropdown(
                                                              options=list(pop_coun_rank['Variant'].unique()),
                                                              value='Medium',
                                                              id='var-rank-graph'
                                                          )
                                                      ]
                                                  )
                                              ]
                                          )
                                      ]

                                  ),
                                  html.Div(
                                      className='col-md-6',
                                      children=[
                                          html.Div(
                                              children=[
                                                  html.H3(
                                                      children='World Actual Population from 1950 to 2019 and its '
                                                               'Projection to 2100',
                                                      style={'text-align': 'left',
                                                             'font-weight': 'bold',
                                                             'font-size': '15px'
                                                             }
                                                  ),

                                                  dcc.Graph(id='pop_world_graph', figure=fig1),

                                              ]

                                          ),
                                          html.Div(
                                              children=[
                                                  html.H3(children='Population Growth by Country and Growth Variant',
                                                          style={'text-align': 'left',
                                                                 'font-weight': 'bold',
                                                                 'font-size': '15px'
                                                                 }),
                                                  dcc.Graph(
                                                      id='pop_coun_graph'
                                                  ),
                                                  html.Div(
                                                      className='row',
                                                      children=[
                                                          html.Div(
                                                              className='col-md-6',
                                                              children=[
                                                                  html.H5(children='Select Country',
                                                                          style={'margin-bottom': '10px',
                                                                                 'margin-top': '10px'
                                                                                 }
                                                                          ),
                                                                  dcc.Dropdown(
                                                                      options=list(pop_coun['Country'].unique()),
                                                                      value='United States of America',
                                                                      id='select_country'
                                                                  )
                                                              ]
                                                          ),
                                                          html.Div(
                                                              className='col-md-6',
                                                              children=[
                                                                  html.H5(children='Select Growth Variant',
                                                                          style={'margin-bottom': '10px',
                                                                                 'margin-top': '10px'
                                                                                 }
                                                                          ),
                                                                  dcc.Dropdown(
                                                                      options=list(pop_coun['Variant'].unique()),
                                                                      value='Medium',
                                                                      id='select_variant'
                                                                  )
                                                              ]
                                                          )
                                                      ]
                                                  )
                                              ]

                                          )
                                      ]
                                  )
                              ]
                          )
                      ]
                      )




@app.callback(
    Output('pop_coun_graph', 'figure'),
    Output('pop-coun-rank-graph', 'figure'),
    Input('select_country', 'value'),
    Input('select_variant', 'value'),
    Input('year-rank-graph', 'value'),
    Input('var-rank-graph', 'value'),

)
def update_dashboard(country2, variant2, year3, variant3):
    filtered_pop_coun = pop_coun[(pop_coun.Country == country2) & (pop_coun.Variant == variant2)]
    fig2 = px.line(filtered_pop_coun, x='Year', y='Population')
    fig2.update_xaxes(title=None)
    fig2.update_yaxes(title=None)
    fig2.update_layout(autosize=False,
                       height=242,
                       margin=dict(
                           l=0,
                           r=0,
                           b=30,
                           t=20,
                           pad=0
                       ))

    filtered_pop_coun_rank = pop_coun_rank[(pop_coun_rank.Year == year3) & (pop_coun_rank.Variant == variant3)].head(20)
    filtered_pop_coun_rank = filtered_pop_coun_rank.sort_values(by=['Population'])
    fig3 = px.bar(filtered_pop_coun_rank, x='Population', y='Country')
    fig3.update_xaxes(title=None)
    fig3.update_yaxes(title=None)
    fig3.update_layout(height=500,
                       autosize=False,
                       margin=dict(
                           l=0,
                           r=0,
                           b=20,
                           t=20,
                           pad=0
                       )
                       )

    return fig2, fig3


if __name__ == '__main__':
    app.run_server(debug=True)
