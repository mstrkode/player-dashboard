from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_table
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

players = ['wade', 'dame', 'rose', 'curry', 'harden', 'wall', 'kobe','lonzo','westbrook','giannis']

files = [i + "1213.csv" for i in players]
columns = [0, 1, 2, 3, 4, 6, -3, -4, -5, -6, -7, -8, -1, -2, ]
files_csv = [pd.read_csv(i) for i in files]
files_csv = [i[i.columns[columns]] for i in files_csv]
opponents = sorted(list(set(files_csv[0]['Opp'].tolist())))
dates = files_csv[0]['Date'].tolist()
dates = sorted(list(set([i[-4:] for i in dates])))

for j in files_csv:
    j.drop(j.loc[j['AST'] == 'Inactive'].index, inplace=True)
    j.drop(j.loc[j['PTS'] == 'Inactive'].index, inplace=True)
    j.drop(j.loc[j['+/-'] == 'Inactive'].index, inplace=True)
    j.drop(j.loc[j['AST'] == 'Player Suspended'].index, inplace=True)
    j.drop(j.loc[j['PTS'] == 'Player Suspended'].index, inplace=True)
    j.drop(j.loc[j['+/-'] == 'Player Suspended'].index, inplace=True)
    j.drop(j.loc[j['AST'] == 'Did Not Dress'].index, inplace=True)
    j.drop(j.loc[j['PTS'] == 'Did Not Dress'].index, inplace=True)
    j.drop(j.loc[j['+/-'] == 'Did Not Dress'].index, inplace=True)
    j.drop(j.loc[j['AST'] == 'Not With Team'].index, inplace=True)
    j.drop(j.loc[j['PTS'] == 'Not With Team'].index, inplace=True)
    j.drop(j.loc[j['+/-'] == 'Not With Team'].index, inplace=True)
    j.drop(j.loc[j['AST'] == 'Did Not Play'].index, inplace=True)
    j.drop(j.loc[j['PTS'] == 'Did Not Play'].index, inplace=True)
    j.drop(j.loc[j['+/-'] == 'Did Not Play'].index, inplace=True)
    j['AST'].apply(int)
    j['PTS'].apply(int)
    # df[['two', 'three']] = df[['two', 'three']].astype(float)
    j['AST'] = j['AST'].astype(int)
    j['PTS'] = j['PTS'].astype(int)
    plus_minus = str(j.columns.tolist()[-2])
    j['+\-'] = j[plus_minus].astype(int)
    j['GmSc'] = j['GmSc'].astype(float)

players_to_csv = dict(zip(players, files_csv))
app.layout = html.Div([

    html.Div(children=[
        html.H2('NBA Stats', style={'textAlign': 'center', 'display': 'inline-block', })

    ]
    ),
    html.H1(''),
    # html.H1('SERP Tool Demo'),
    html.Div([
        html.H3('Players'),
        dcc.Dropdown(  ### PLAYER DROP DOWN
        id='players-dropdown', options=[i.upper() for i in players], value=players[0].upper()),
        html.H3('Opponent'),
        dcc.Dropdown(  ### OPPONENT DROP DOWN
            id='opponent-dropdown', options=[i.upper() for i in opponents], value=opponents),
        html.H3('Year'),
        dcc.Dropdown(  ### Date DROP DOWN
            id='date-dropdown', options=[i.upper() for i in dates], value=dates),
        html.H3('Game Log'),
        dash_table.DataTable(  ### DATATABLE
            id='my-datatable',
            columns=[{"name": i.upper(), "id": i} for i in files_csv[0].columns.values.tolist()],
            fixed_rows={'headers': True, 'data': 0},
            style_cell={'width': '150px'},
            style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(400, 248, 248)'}],
            style_header={'backgroundColor': 'rgb(350, 230, 230)', 'fontWeight': 'bold'},
            data=files_csv[0].to_dict('records'), filter_action='native', sort_action='native',
            row_selectable="multi", selected_rows=[])
    ])])


@app.callback([
    Output('my-datatable', 'data'),
    Output('date-dropdown', 'options'),
    Output('date-dropdown', 'value'),
],
    [Input('players-dropdown', 'value'),
    Input('opponent-dropdown', 'value'),
     Input('date-dropdown', 'value'),
     ]

)
def set_region_value(value,value2,value3):
    curr_df = players_to_csv[value.lower()]
    if value2 != None:
        curr_df = curr_df.query('Opp == @value2')
    if value3 != None:
        curr_df = curr_df.query('Date == @value3')
    dates = curr_df['Date'].tolist()
    dates = sorted(list(set([i[-4:] for i in dates])))
    curr_df["+/-"] = 'Hidden'

    return curr_df.to_dict('records'),dates,dates




if __name__ == '__main__':
    # print(files_csv)
    app.run_server(debug=True)
