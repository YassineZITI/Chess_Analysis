
import pandas as pd
import dash
import plotly.express as px
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output 


### importing and preprocessing data
dff=pd.read_csv("chess_games.csv")
df=dff.copy()
df['Date']=pd.to_datetime(df['Date'],format='%Y/%m/%d')
df.drop(['game_id','moves','opponent_id','opponent_rating','analysis'],axis=1,inplace=True)

df.opening=df.opening.str.split(':').str[0]
df.winner=df.winner.fillna('draw')
openings=list(df.opening.unique())
df['wining']=df.winner
for i in range(len(df)):
    if df.at[i,'winner']=='draw':
        continue
    elif df.at[i,'winner']==df.at[i,'my_color']:
        df.at[i,'wining']='won'
    else:
        df.at[i,'wining']='lost'
df.dropna(subset=['accuracy'],inplace=True)
### helping functions
def filter_inputs(data,speed,color,opening):
    if speed=='all' and color=='all':
        pass
    if speed=='all' and color!='all':
        data=data[data.my_color==color]
    if speed!='all' and color=='all':
        data= data[data.speed==speed]
    if speed!='all' and color!='all':
        data= data.loc[(data.speed==speed)&(data.my_color==color)]
    if opening=='all':
        return data
    
    data=data[data.opening == opening]
    return data

def get_pie(data,col):
    data=data.groupby([col]).size().reset_index()
    data.columns=[col,'count']
    return data
def month(row):
    date=str(row)
    look_up = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May',
            '6': 'Jun', '7': 'Jul', '8': 'Aug', '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
    return look_up[date]
def get_data(data,col):
    ## first let' retrive the accuracy data
    ## because i didn't analys each game i played we will visualize
    ## the average accuracy each and we hope that i analysed at least one game each month
    

    
    data=data[data['Date'].dt.year==2021].sort_values('Date')
    data['month']=data['Date'].dt.month
    data=data.groupby(['month'])[[col]].mean().reset_index()
    data['month'] = data['month'].apply(month)
    return data
### dash application

app=dash.Dash(__name__)

### app layout

app.layout=html.Div([
    html.H1('Chess Analysis', style={'textAlign': 'center'}),
    html.Div([
        html.H2('select the speed of the game', style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='speed',
            options=[{'label':'all','value':'all'},
            {'label':'blitz','value':'blitz'},
            {'label':'rapid','value':'rapid'}],
            value='blitz')
        ],style={'display':'flex'}),
    html.Div([
        html.H2('select a color', style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='color',
            options=[{'label':'all','value':'all'},
            {'label':'white','value':'white'},
            {'label':'black','value':'black'}],
            value='black')
        ],style={'display':'flex'}),
    html.Div([
        html.H2('select an opening', style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='opening',
            options=[{'label':'all','value':'all'}]+[{'label':i,'value':i} for i in openings],
            value='Lion Defense'
            )
        ],style={'display':'flex'}),

    html.Br(),
    html.Br(),
    dcc.Textarea(
        id='textarea',
        value='3097',
        style={'textAlign':'center','width': '100%', 'height': 19},
    ),
    html.Div([
        
        html.H2('graph 0', style={'textAlign': 'center'}),
        dcc.Graph(figure={},id='graph0')
        
    ]
    ),
    html.Br(),
    html.Div([
        html.Div([
            html.H2('graph 1', style={'textAlign': 'center'}),
            dcc.Graph(figure={},id='graph1')
        ]),
        html.Div([
            html.H2('graph 2', style={'textAlign': 'center'}),
            dcc.Graph(figure={},id='graph2')
        ])
    ]
    ),
    html.Br(),
    html.Div([
        html.Div([
            html.H2('graph 3', style={'textAlign': 'center'}),
            dcc.Graph(figure={},id='graph3')
        ]),
        html.Div([
            html.H2('graph 4', style={'textAlign': 'center'}),
            dcc.Graph(figure={},id='graph4')
        ])
    ]
    ),
    html.Br(),
    html.Div([
        
        html.H2('graph 5', style={'textAlign': 'center'}),
        dcc.Graph(figure={},id='graph5')
        ]
             )
    

])

### app interactivity
@app.callback([Output(component_id='textarea',component_property='value'),
               Output(component_id='graph0',component_property='figure'),
               Output(component_id='graph1',component_property='figure'),
               Output(component_id='graph2',component_property='figure'),
               Output(component_id='graph3',component_property='figure'),
               Output(component_id='graph4',component_property='figure'),
               Output(component_id='graph5',component_property='figure')],
               [Input(component_id='speed',component_property='value'),
               Input(component_id='color',component_property='value'),
               Input(component_id='opening',component_property='value')])
def get_graphs(speed,color,opening):
    
    
    Data=filter_inputs(df,speed,color,opening)
    
    
    output0='there is only ' + str(len(Data)) + ' games'
    fig0=px.pie(get_pie(Data,'wining'), values='count', names='wining', title='wining pie chart')
    fig1=px.pie(get_pie(Data,'game_ending'), values='count', names='game_ending', title='game_ending pie chart')
    fig2=px.bar(get_data(Data,'accuracy'),y='accuracy',x='month')
    fig3=px.bar(get_data(Data,'inaccuracy'),y='inaccuracy',x='month')
    fig4=px.bar(get_data(Data,'mistake'),y='mistake',x='month')
    fig5=px.bar(get_data(Data,'blunder'),y='blunder',x='month')
    return output0,fig0,fig1,fig2,fig3,fig4,fig5
    






### run the app
if __name__ == '__main__':
    app.run_server(debug=True,port=8000)
