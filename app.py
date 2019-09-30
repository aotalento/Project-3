from flask import (
    Flask,
    render_template,
    jsonify,
    request)
# from IPython.display import HTML
import pandas as pd
import requests
import json
# from bs4 import BeautifulSoup as bs
# import re
import plotly as py
import plotly.graph_objs as go
py.offline.init_notebook_mode(connected = True)


app = Flask(__name__)



@app.route('/')
def home():
    return render_template('Afghan.html')

@app.route('/lost')
def lost():
    return render_template('Lost.html')

@app.route('/links')
def links():
    return render_template('Links.html')


@app.route("/bubble")
def bubble():
    data = pd.read_csv("casualty_data.csv")

    geo = pd.read_csv("casualty_province_geocodes.csv")

    data["Casualty_Location"] = data["Country"] + " " + data["Province"]

    data["Date"] = pd.to_datetime(data["Date"])

    data["year"] = pd.DatetimeIndex(data['Date']).year

    df = data.groupby(["Casualty_Location","year"])["Where"].count().reset_index()

    df = pd.merge(df,geo,on="Casualty_Location")

    #find center
    center_lat = df["lat"].astype(float).mean()
    center_lng = df["lng"].astype(float).mean()
    import plotly.express as px
    gapminder = px.data.gapminder()
    fig = px.scatter_geo(df, lat="lat",lon="lng",
                         hover_name="Casualty_Location", size="Where",
    #                      color = "Casualty_Location",
#                          center = [center_lat,center_lng],
#                          scope = 5,
                         animation_frame="year",
                         projection="natural earth")
    return(py.offline.plot(fig,output_type = 'div'))
    
    
@app.route("/json")
def json():
    data = pd.read_csv("casualty_data.csv")
    casualty_geocodes = pd.read_csv("casualty_geocodes.csv")
    origin_geocodes = pd.read_csv("origin_geocodes.csv")

    casualty_geocodes["lat"] = pd.to_numeric(casualty_geocodes["lat"],errors='ignore')
    casualty_geocodes["lng"] = pd.to_numeric(casualty_geocodes["lng"],errors='ignore')
    origin_geocodes["lat"] = pd.to_numeric(origin_geocodes["lat"],errors='ignore')
    origin_geocodes["lng"] = pd.to_numeric(origin_geocodes["lng"],errors='ignore')

    data["Casualty_Location"] = data["Country"] + " " + data["Province"] +" "+ data["Where"]
    data["Origin"] = data["State"] + " " + data["City"]
    casualty_geocodes.rename(columns = {"lat":"lat_c"},inplace = True)
    casualty_geocodes.rename(columns = {"lng":"lng_c"},inplace = True)
    df = pd.merge(data,casualty_geocodes,on = "Casualty_Location")
    origin_geocodes.rename(columns = {"Where":"Origin"},inplace = True)
    origin_geocodes.rename(columns = {"lat":"lat_o"},inplace = True)
    origin_geocodes.rename(columns = {"lng":"lng_o"},inplace = True)
    df = pd.merge(df,origin_geocodes,on = "Origin")
    df["Date"] = pd.to_datetime(df["Date"])
    df["location_c"] = 1
    df["location_o"]= 1
    for i in range(0,len(df)):
        df["location_c"][i] = [(df["lat_c"][i]),(df["lng_c"][i])]
        df["location_o"][i] = [(df["lat_o"][i]),(df["lng_o"][i])]
#     df = pd.read_csv("df_for_json.csv")
    return(df.to_json(orient='index'))
    
if __name__ == "__main__":
    app.run(debug=True)