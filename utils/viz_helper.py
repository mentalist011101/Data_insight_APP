import plotly.express as px
import pandas as pd

def generate_plot(df, chart_type, x_col, y_col=None):
    """Génération de graphiques avec Plotly Express"""
    if chart_type == "histogramme":
        fig = px.histogram(df, x=x_col)
    elif chart_type == "barre":
        fig = px.bar(df, x=x_col, y=y_col if y_col else None)
    elif chart_type == "ligne":
        fig = px.line(df, x=x_col, y=y_col if y_col else None)
    elif chart_type == "nuage de points" and y_col:
        fig = px.scatter(df, x=x_col, y=y_col)
    else:
        fig = px.bar(df, x=x_col)  # Fallback
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#2c3e50"}
    )
    return fig