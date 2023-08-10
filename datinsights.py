import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots



def dat_insights(dataframe,sheet_name=False,rtn=True,dat=False,date_parse=False):
  palette = ["#FC645F", "#A8E4A0", "#7088FF", "#FEB1AF"]
  if type(dataframe) == str:
    dataframe = data_capture(dataframe,sheet_name,date_parse).capture()
  if dat is not False:
    dataframe = column_cleaner(dataframe,[column for column in dataframe.columns if column in dat])
  null_values = dataframe.isnull().sum().sort_values(ascending=False)
  nulls_sum = (dataframe.isnull().sum()).sum()
  fields_sum = (dataframe.shape[0] * dataframe.shape[1]) - nulls_sum
  nulls_percentile = max(null_values)
  fills_percentile = dataframe.shape[0] - nulls_percentile
  if null_values.shape[0] > 15:
    null_values = null_values[null_values != 0]
  else:
    pass
  fig = make_subplots(rows=2,
                      cols=2,
                      subplot_titles=["<b>CORRECT ENTRIES</b>",
                                      "<b>CORRECT CELLS",
                                      "<b>NULLS/COLUMN</b>"],
                      specs=[[{'type':'domain'},{'type':'domain'}],
                             [{'type':'xy',"colspan":2},{}]])
  fig.add_trace(go.Pie(labels=["Null entries","Valid entries"],
                       values=[nulls_percentile,fills_percentile],
                       hole=0.4,
                       marker_colors=palette,
                       name="Correct entries",
                       title=dataframe.shape[0],legendgroup="apie"),1,1)
  fig.add_trace(go.Pie(labels=["Null cells",
                               "Valid cells"],
                       values=[nulls_sum,
                               fields_sum],
                       hole=0.4,
                       marker_colors=palette,
                       name="Correct cells",
                       title=dataframe.shape[0]*dataframe.shape[1],
                       legendgroup="pie"),1,2)
  fig.add_trace(go.Bar(x=null_values,
                       y=null_values.index,
                       name="Nulls/Column",
                       orientation="h",
                       marker_color="#FC645F",
                       showlegend=False),2,1)
  fig.update_traces(textposition='inside')
  fig.update_layout(height=600,
                    width=800,
                    title=f"<b>{sheet_name.upper()} INSIGHTS</b>",
                    yaxis_title="Columns",
                    xaxis_title="Nulls",
                    font_size=14)
  if rtn == True:
    fig.show(config={'modeBarButtonsToAdd':['drawline',
                                            'drawopenpath',
                                            'drawclosedpath',
                                            'drawcircle',
                                            'drawrect',
                                            'eraseshape']})
  else:
    return fig





def correlation_matrix(dataframe, name, rtn=True):
  dataframe = dataframe.convert_dtypes()
  fig=make_subplots(cols=1,
                    rows=1)
  z,x = dataframe.corr(method="pearson"),dataframe.corr(method="pearson").columns
  fig.add_trace(go.Heatmap(z = z,
                           x = x,
                           y = x,
                           colorscale="Burg"))
  fig.update_layout(height=800,width=800,title=f"<b>{name} FEATURE CORRELATION MATRIX")
  if rtn == True:
    fig.show('png')
        # fig.show(config={'modeBarButtonsToAdd':['drawline',
        #                                     'drawopenpath',
        #                                     'drawclosedpath',
        #                                     'drawcircle',
        #                                     'drawrect',
        #                                     'eraseshape']})
  else:
    return fig
