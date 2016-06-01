import json
import os
from flask import Flask, render_template, make_response, jsonify
from urllib import urlopen
from datetime import datetime, timedelta

app = Flask(__name__)

weather_file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))), "weather.json")

url = urlopen('http://opendata-download-metfcst.smhi.se/api/category/pmp1.5g/version/1/geopoint/lat/59.19/lon/17.62/data.json').read()
result = json.loads(url)
eftermiddag = datetime.strftime(datetime.now(),"%Y-%m-%dT15:00")
now = datetime.strftime(datetime.now(),"%Y-%m-%dT%H:00")
nexthour = datetime.strftime(datetime.today() + timedelta(hours = 1),"%Y-%m-%dT%H:00")

@app.route('/')
def index():
    return render_template("weather.html")


@app.route('/api/v1/weather')
def weather():
    for item in result['timeseries']:
        if item["validTime"][:16] == now:
            nutime = now[11:]
            nutemp = item['t']
            nucloud = item['tcc']
            nurain = item['pcat']
            nudata = {"temp":nutemp, "tid":nutime, "moln":nucloud, "regn":nurain }
            break

    for item in result['timeseries']:
        if item["validTime"][:16] == nexthour:
            nexttime = nexthour[11:]
            nexttemp = item['t']
            nextcloud = item['tcc']
            nextrain = item ['pcat']
            nextdata = {"temp":nexttemp, "tid":nexttime, "moln":nextcloud, "regn":nextrain }
            break

    for item in result['timeseries']:
        if item["validTime"][:16] == eftermiddag:
            eftime = eftermiddag[11:]
            eftemp = item['t']
            efcloud = item['tcc']
            efrain = item['pcat']
            efdata = {"temp":eftemp, "tid":eftime, "moln":efcloud, "regn":efrain}
            break


    alldata = {"nu":nudata, "sen":nextdata, "em":efdata}
    print alldata

    with open(weather_file, 'w') as fp:
        json.dump(alldata, fp, ensure_ascii=False)

    return make_response(jsonify(alldata))

if __name__ == '__main__':
    app.run()