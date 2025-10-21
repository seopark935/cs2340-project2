import folium
import json
from django.shortcuts import render


# Create your views here.
def index(request):
    m = folium.Map(location = [20, 0], zoom_start = 3, min_zoom = 3, max_zoom = 10, max_bounds= True)
    with open("map/custom.geo.json") as f:
        countries = json.load(f)
    folium.GeoJson(countries,
                     name = "Countries", 
                     tooltip= folium.GeoJsonTooltip(fields = ["formal_en"], aliases = ["Country:"]),
                     style_function=lambda feature: {'fillColor': 'yellow', 'color': 'yellow', 'weight': 0.1,'fillOpacity': 0.3, 'stroke': False},
                    highlight_function = lambda x: {'fillColor': 'white', 'color': 'white', 'weight': 0.5, 'stroke': False},
                    zoom_on_click= True,

                    ).add_to(m)
    
    map_html = m._repr_html_()
    return render(request, "map/index.html", {"map": map_html})
# Create your views here.
