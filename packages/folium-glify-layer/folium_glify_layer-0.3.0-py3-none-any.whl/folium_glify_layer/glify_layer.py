# -*- coding: utf-8 -*-


from folium.elements import JSCSSMixin
from folium.features import GeoJsonPopup, Tooltip
from folium.map import Layer
from jinja2 import Template


class GlifyLayer(JSCSSMixin, Layer):
    """
    Creates a GlifyLayer.

    Parameters
    ----------
    feature_collections: dict
        The geo-json feature collections you want to plot:

        * `shapes`: A FeatureCollection of Polygon's
        * `lines`: A FeatureCollection of LineString's
        * `points`: A FeatureCollection of Point's
        
    glify_options: dict
        Options for L.glify object (currently a single set of options is used for all geometry types).
        e.g. { border, opacity, size, sensitivity }


    Examples
    --------
    >>> GlifyLayer({
    ...     'lines': {
    ...          'type': 'FeatureCollection',
    ...          'features': [
    ...            {
    ...              'type': 'Feature',
    ...              'geometry': {
    ...                'type': 'LineString',
    ...                'coordinates': [[-70,-25],[-70,35],[70,35]],
    ...                },
    ...              'properties': {
    ...                'times': [1435708800000, 1435795200000, 1435881600000]
    ...              }
    ...            }
    ...          ]
    ...       })
    ...     }

    See https://github.com/onaci/Leaflet.glify.layer for more information.

    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}

            var map = {{ this._parent.get_name() }};
           
            var options = {
                types: {{ this.feature_collections|tojson }},
                glifyOptions: {{ this.glify_options|tojson }}
            };

            {%- if this.color_function is not none %}
                options.glifyOptions.color = {{ this.color_function.strip() }};
            {%- endif %}
            {%- if this.click_function is not none %}
                options.glifyOptions.click = {{ this.click_function.strip() }};
            {%- endif %}

            {%- if this.popup is not none %}
                options.glifyOptions.click = function(e, feature, xy){
                    if (Array.isArray(feature)){
                        L.popup()
                        // its a [lng,lat] 
                        .setLatLng(feature.reverse())
                        .setContent(`Popup content is limited to coordinates for Point features: ${feature.reverse()}`)
                        .openOn(map);
                    } else {
                        var popupOptions = {{this.popup|tojson}};
                        var content = '';

                        if (tooltipOptions.fields){
                            popupOptions.fields.forEach(function(field, index){
                                if (popupOptions.labels) {
                                    content += `<strong>${popupOptions.aliases[index]}: </strong>${feature.properties[field]}<br/>`
                                } else {
                                    content += `<strong>${field}: </strong>${feature.properties[field]}<br/>`
                                }                           
                            });
                        } else {
                            content += `<strong>${key}: </strong>${feature.properties[key]}<br/>`
                        }

                        L.popup()
                        .setLatLng(e.latlng)
                        .setContent(content)
                        .openOn(map);
                    }  
                };
            {%- endif %}
            
            {%- if this.tooltip is not none %}

                var tooltipOptions = {{this.tooltip|tojson}};
                var tooltip = L.DomUtil.create('div', 'tooltip', map._container);      
                var offset = tooltipOptions.offset || [10, 10];
                tooltip.style.padding = "10px";
                tooltip.style.position = 'absolute';
                tooltip.style.zIndex = 999999;
                tooltip.style.background = "#CCC";
                tooltip.style.fontSize = "14px";

                // override default styles with any from user
                Object.keys(tooltipOptions.styles).forEach(function(key){
                    tooltip.style[key] = tooltipOptions.styles[key];
                })

                options.glifyOptions.hover = function(e, feature, xy){  

                    if (Array.isArray(feature)){
                        var f = feature.slice().reverse();
                        L.tooltip({ sticky: tooltipOptions.sticky })
                        // its a [lng,lat] 
                        .setLatLng(f)
                        .setTooltipContent(`Tooltip content is limited to coordinates for Point features: ${f}`)
                        .openOn(map);
                    } else {      
                        var content = '';
                        if (tooltipOptions.fields){
                            tooltipOptions.fields.forEach(function(field, index){
                                if (tooltipOptions.labels) {
                                    content += `<strong>${tooltipOptions.aliases[index]}: </strong>${feature.properties[field]}<br/>`
                                } else {
                                    content += `<strong>${field}: </strong>${feature.properties[field]}<br/>`
                                }                           
                            });
                        } else {
                            Object.keys(feature.properties).forEach(function(key) {
                                content += `<strong>${key}: </strong>${feature.properties[key]}<br/>`
                            });
                        }
                        
                        tooltip.innerHTML = content; 
                        tooltip.style.opacity = 1;      
                        tooltip.style.left = `${e.containerPoint.x + offset[0]}px`;
                        tooltip.style.top = `${e.containerPoint.y + offset[1]}px`;

                        // TODO - use hoverOff instead if/when implemented in L.glify
                        setTimeout(function() {
                            tooltip.style.opacity = 0; 
                        }, tooltipOptions.timeout_ms || 5000);
                    }  
                };

            {%- endif %}
            
            
            L.glify.layer(options).addTo({{ this._parent.get_name() }});          

        {% endmacro %}
        """)

    default_js = [
        ('glify-browser',
         'https://unpkg.com/leaflet.glify@3.0.2/dist/glify-browser.js'),
        ('leaflet-glify-layer',
         'https://unpkg.com/leaflet-glify-layer@0.0.6/dist/leaflet-glify-layer.js')
    ]

    def __init__(self, feature_collections, glify_options={}, 
        color_function=None, click_function=None, popup=None, tooltip=None):
        
        super(GlifyLayer, self).__init__()
        self._name = 'GlifyLayer'
  
        if feature_collections:
            self.feature_collections = feature_collections
        else:
            raise ValueError('feature_collections must not be None.')
        
        self.glify_options = glify_options
        self.color_function = color_function
        self.click_function = click_function
    
        self.popup = popup
        self.tooltip = tooltip