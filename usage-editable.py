import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import plotly

app = dash.Dash()

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True
#app.css.config.serve_locally = True

DF_SIMPLE = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D', 'E', 'F'],
    'y': [40, 30, 10, 20, 30, 60],
    'z': [100, 10, 20, 30, 100, 30]
})

progress_bar_map = dict()
progress_bar_map['y'] = 100
progress_bar_map['z'] = 100

app.layout = html.Div([
    html.H4('Editable DataTable'),
    dt.DataTable(
        rows=DF_SIMPLE.to_dict('records'),

        # optional - sets the order of columns
        columns=sorted(DF_SIMPLE.columns),
        progress_bar_columns=progress_bar_map,
        editable=True,

        id='editable-table'
    ),
], className='container')


@app.callback(
    Output('output', 'children'),
    [Input('editable-table', 'rows')])
def update_selected_row_indices(rows):
    return json.dumps(rows, indent=2)


@app.callback(
    Output('graph', 'figure'),
    [Input('editable-table', 'rows')])
def update_figure(rows):
    dff = pd.DataFrame(rows)
    return {
        'data': [{
            'x': dff['x'],
            'y': dff['y'],
        }],
        'layout': {
            'margin': {'l': 10, 'r': 0, 't': 10, 'b': 20}
        }
    }

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

app.css.append_css({
    'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'
})




if __name__ == '__main__':
    app.run_server(debug=True)
