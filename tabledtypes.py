
def table_dtype(dataframe,rtn=True):
  import pandas as pd
  import plotly.graph_objects as go
  import plotly.express as px
  from plotly.subplots import make_subplots

  # Color palette for Plotly
  palette = ["#FC645F", "#A8E4A0", "#7088FF", "#FEB1AF"]
  # Función que crea reporte de tipo de variables y datos
  # dataframe = objet.dataframe
  # arg = True: use fig.show() otherwise it returns fig for object
  df_dtypes = dataframe.convert_dtypes()
  table_columns = [column for column in df_dtypes.dtypes.index.values]
  table_values = [str(value) for value in df_dtypes.dtypes]
  values = pd.Series(table_values)
  fig = make_subplots(rows=2,
                      cols=2,
                      specs=[[{"type":"table"},{"type":"domain"}],
                             [{"type":"table"},{"type":"domain"}]],
                      subplot_titles=["",
                                      "<b>TYPE",
                                      "",
                                      "<b>CLASS"])
  fig.add_trace(go.Pie(labels=values.value_counts().index,
                       values=values.value_counts(),
                       marker_colors=palette,
                       hole=0.4,
                       title=values.shape[0],
                       legendgroup="pie"),1,2)
  fig.update_traces(textposition='inside')
  fig.add_trace(go.Table(header=dict(values=['Column',
                                             'Data type'],
                                     fill_color="#A8E4A0",
                                     line_color='darkslategray'),
                         cells=dict(values=[table_columns,
                                            table_values],
                                    line_color='darkslategray')),1,1)
  fig.update_layout(height=500,width=1000,
                    title="<b>DATA TYPE ANALYSIS",
                    font_size=12)

  type_var = []
  for value in range(0,len(df_dtypes.dtypes)):
    if "Int"  in str(df_dtypes.dtypes[value]) or "Float" in str(df_dtypes.dtypes[value]):
      type_var.append("Numerical")
    else:
      if len(df_dtypes[df_dtypes.dtypes.index[value]].value_counts().index) <= 2:
        type_var.append("Numerical/Boolean")
      else:
        if len(df_dtypes[df_dtypes.dtypes.index[value]].value_counts().index) >= 100:
          type_var.append("Undetermined")
        else:
          type_var.append("Categorical")

  pie_values = [values for values in [type_var.count("Categorical"), type_var.count("Undetermined"), type_var.count("Numerical"), type_var.count("Numerical/Boolean")] if values !=0]
  pie_labels = str(set(type_var)).replace("{","").replace("}","").replace("'","").split(",")
  fig.add_trace(go.Table(header=dict(values=["Columns",
                                             "Classification"],
                                     fill_color="#A8E4A0",
                                     line_color='darkslategray'),
                         cells=dict(values=[df_dtypes.dtypes.index,type_var])),2,1)
  fig.add_trace(go.Pie(labels=pie_labels,
                       values=pie_values,
                       marker_colors=palette,
                       hole=0.4,
                       legendgroup="pie2"),2,2)
  fig.update_layout(height=800,width=1000,title="<b>DATA TYPE ANALYSIS",font_size=14)
  if rtn == True:
    fig.show()
  else:
    return fig
