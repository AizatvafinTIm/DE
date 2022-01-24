from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import dash
from EulerMethod import EulerMethod
from ImprovedEuler import ImprovedEuler
from RungeKutta import RungeKutta

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.H1('Assignment DE'),
    html.Div("Please enter the values to input"),

    html.Br(),

    html.Div([
        " n (amount of steps): ",
        html.Br(),
        dcc.Input(id='my-input_h', value='5', type='text', style={}),

    ]),
    html.Br(),
    html.Div([
        " x0: ",
        html.Br(),
        dcc.Input(id='my-input_x0', value='0', type='text')
    ]),
    html.Br(),

    html.Div([
        " y0: ",
        html.Br(),
        dcc.Input(id='my-input_y0', value='0', type='text')
    ]),
    html.Br(),

    html.Div([
        " left border: ",
        html.Br(),
        dcc.Input(id='my-input_l', value='0', type='text')
    ]),
    html.Br(),
    html.Div([
        " right border: ",
        html.Br(),
        dcc.Input(id='my-input_r', value='10', type='text')
    ]),

    html.Br(),

    html.Div([
        " minN: ",
        html.Br(),
        dcc.Input(id='my-input_minN', value='1', type='text')
    ]),
    html.Br(),

    html.Div([
        " maxN: ",
        html.Br(),
        dcc.Input(id='my-input_maxN', value='10', type='text')
    ]),

    html.Br(),
    html.Label(" Graphs of solutions and exact  ".upper()),

    html.Div(
        dcc.Graph(id='all_graph')
    ),
    html.Br(),
    html.Label("Graphs of LTE".upper()),

    html.Div(
        dcc.Graph(id="lte_graph")
    ),
    html.Br(),
    html.Label("Graphs of maxGte(n)".upper()),

    html.Div(
        dcc.Graph(id="gte_graph")
    )

])


@app.callback(
    Output('all_graph', 'figure'),
    Input('my-input_h', 'value'),
    Input('my-input_x0', 'value'),
    Input('my-input_y0', 'value'),
    Input('my-input_l', 'value'),
    Input('my-input_r', 'value'),
)
def update_output_div(h, x0, y, l, r):
    em = EulerMethod(float(h), float(x0), float(y), float(l), float(r))
    iem = ImprovedEuler(float(h), float(x0), float(y), float(l), float(r))
    rk = RungeKutta(float(h), float(x0), float(y), float(l), float(r))
    interval = em.interval
    exact_graph = em.count_exact()
    euler_graph = em.count_euler_arr()
    ieuler_graph = iem.count_ieuler()
    rungek_graph = rk.count_rungekutta()

    fig = go.Figure(
        data=go.Scatter(x=interval, y=exact_graph, mode='lines+markers', line=dict(color='#ffe476'), name='Exact')
    )
    fig.add_trace(go.Scatter(x=interval, y=euler_graph, mode='lines+markers', line=dict(color="#0000ff"), name='Euler'))
    fig.add_trace(
        go.Scatter(x=interval, y=ieuler_graph, mode='lines+markers', line=dict(color="#ff0000"), name='Improved Euler'))
    fig.add_trace(
        go.Scatter(x=interval, y=rungek_graph, mode='lines+markers', line=dict(color="#80ff66"), name='Runge-Kutte'))
    return fig


@app.callback(
    Output('lte_graph', 'figure'),
    Input('my-input_h', 'value'),
    Input('my-input_x0', 'value'),
    Input('my-input_y0', 'value'),
    Input('my-input_l', 'value'),
    Input('my-input_r', 'value'),
)
def update_output_lte_div(h, x0, y, l, r):
    em = EulerMethod(float(h), float(x0), float(y), float(l), float(r))
    iem = ImprovedEuler(float(h), float(x0), float(y), float(l), float(r))
    rk = RungeKutta(float(h), float(x0), float(y), float(l), float(r))
    interval = em.interval

    lte_euler_graph = em.count_lte()
    lte_ieuler_graph = iem.count_lte()
    lte_rungek_graph = rk.count_lte()
    fig = go.Figure(
        data=go.Scatter(x=interval, y=lte_euler_graph, mode='lines+markers', line=dict(color='#ffe476'),
                        name='Euler LTE')
    )
    fig.add_trace(go.Scatter(x=interval, y=lte_ieuler_graph, mode='lines+markers', line=dict(color="#0000ff"),
                             name='Im. Euler LTE'))
    fig.add_trace(
        go.Scatter(x=interval, y=lte_rungek_graph, mode='lines+markers', line=dict(color="#ff0000"),
                   name='Runge-Kutte LTE'))
    return fig


@app.callback(
    Output('gte_graph', 'figure'),
    Input('my-input_minN', 'value'),
    Input('my-input_maxN', 'value'),
    Input('my-input_x0', 'value'),
    Input('my-input_y0', 'value'),
    Input('my-input_l', 'value'),
    Input('my-input_r', 'value'),
)
def update_output_gte_div(minN, maxN, x0, y, l, r):
    max_gte_for_euler = []
    max_gte_for_ieuler = []
    max_gte_for_rungek = []
    minN = int(minN)
    maxN = int(maxN)
    x0 = float(x0)
    y = float(y)
    l = float(l)
    r = float(r)
    range_n = list(range(minN, maxN + 1))
    for i in range(minN, maxN + 1):
        em = EulerMethod(i, x0, y, l, r)
        iem = ImprovedEuler(i, x0, y, l, r)
        rk = RungeKutta(i, x0, y, l, r)
        max_gte_for_euler.append(max(em.count_gte()))
        max_gte_for_ieuler.append(max(iem.count_gte()))
        max_gte_for_rungek.append(max(rk.count_gte()))

    fig = go.Figure(
        data=go.Scatter(x=range_n, y=max_gte_for_euler, mode='lines+markers', line=dict(color='#ffe476'),
                        name='maxGTE(n) Euler')
    )
    fig.add_trace(go.Scatter(x=range_n, y=max_gte_for_ieuler, mode='lines+markers', line=dict(color="#0000ff"),
                             name='maxGTE(n) Im. Euler'))
    fig.add_trace(
        go.Scatter(x=range_n, y=max_gte_for_rungek, mode='lines+markers', line=dict(color="#ff0000"),
                   name='maxGTE(n) Runge-Kutte'))
    return fig


if __name__ == "__main__":
    app.run_server(port=4050)
