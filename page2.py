from dash import dcc, Input, Output, Dash, clientside_callback, State, html, ctx
import dash_mantine_components as dmc
import plotly.express as px
import pandas as pd
import json
from dash_iconify import DashIconify


app = Dash()


#card do mantine

homeText = dmc.Text("Home")

card = dmc.Card(
    [
        dmc.Text("Welcome! login with:", size="lg"),
        dmc.Group(
            [
                dmc.Button(
                    leftSection=DashIconify(icon="logos:google"),
                    variant="outline",
                ),
                dmc.Button(
                    "BlueSky",
                    leftSection=DashIconify(icon="logos:bluesky"),
                    variant="outline",
                ),
            ],
            grow=True,
            my="lg",
        ),
        dmc.Divider(
            label="Or continue with email",
            variant="dashed",
            labelPosition="center",
        ),
        dmc.Stack(
            [
                dmc.TextInput(label="Email:"),
                dmc.PasswordInput(label="Password:"),
            ],
            gap="md",
        ),
        dmc.Group(
            [
                dmc.Anchor(
                    dmc.Text("Don't have an account? Register", c="gray", size="sm"),
                    href="/",
                ),
                dmc.Button("Login"),
            ],
            grow=True,
            mt="lg",
        ),
    ],
    withBorder=True,
    p="lg",
    w=400,
    h=400,
)

#fim card do mantine


app.layout = dmc.MantineProvider(theme={
    "primaryColor": "lime",
    "defaultRadius": "sm",
    "components": {
        "Card": {
            "defaultProps": {
                "shadow": "xl"
            }
        }
    }
},

    children=[
    dmc.AppShell([
        dmc.AppShellHeader([
            dmc.SimpleGrid([dmc.Avatar(
                src="https://cdn-icons-png.flaticon.com/512/17/17004.png", radius="xl"
            ),
                dmc.Button(
                "Home", variant="subtle", id='home-btn'),
                dmc.Button(
                "login", variant="subtle", id='login-btn'),
                dmc.Button(
                "Teste", variant="subtle", id='teste-btn'),
            ],
                cols=4,
                spacing='xl',
                verticalSpacing='lg'
            )
        ]),

        dmc.AppShellMain(children=[card],
                         id='page')
    ])
])


@app.callback(
    Output("page", "children"),
    [Input("home-btn", "n_clicks"),
     Input("login-btn", "n_clicks"),
     Input("teste-btn", "n_clicks"),

     ])
def change_pages(home, login, teste):
    
    callbackcontext_message = json.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    })
    
    button = ctx.triggered_id
        
    if(button == 'home-btn'):
        return homeText
    
    if(button == 'login-btn'):
        return card
    
    if(button == 'teste-btn'):
        return html.Pre(callbackcontext_message)
    
    return homeText
        

app.run()

