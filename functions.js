var map, markerLayer;
$(document).ready(function() {
  map = mapbox.map('map');
  map.addLayer(mapbox.layer().id('examples.map-20v6611k'));
  markerLayer = mapbox.markers.layer();

  // Add interaction to this marker layer. This binds tooltips to each marker that has title and description defined.
  mapbox.markers.interaction(markerLayer);
  map.addLayer(markerLayer);
  map.centerzoom({ lat: 0, lon: 0 }, 2);

  document.getElementById('markers').src = 'markers/markers' + getParameterByName('year') + '.js';
});

function addMarkerAtGeo(geolocate) {
    var lat, lon;
    wax.tilejson('http://api.tiles.mapbox.com/v3/examples.map-vyofok3q/geocode/' +
    encodeURIComponent(geolocate) + '.json', function(center) {
        if (center && center.results && center.results.length) {
            loc = center.results[0][0];
            addMarkerAtLatLng(loc.lat, loc.lon);
        }
    }
    );
}

function addMarkerAtLatLng(lat, lon) {
    markerLayer.add_feature({
      geometry: {
          // The order of coordinates here is lon, lat. This is because
          // we use the GeoJSON specification for all marker features.
          // (lon, lat is also the internal order of KML and other geographic formats)
          coordinates: [lon, lat]
      },
      properties: {
          // these properties customize the look of the marker
          // see the simplestyle-spec for a full reference:
          // https://github.com/mapbox/simplestyle-spec
          'marker-color': '#000',
          // 'marker-symbol': 'star-stroked',
          // title: 'Example Marker',
          description: [lon, lat].toString()
      }
    });
}

function getParameterByName(name)
{
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regexS = "[\\?&]" + name + "=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.search);
  if(results == null)
    return "";
  else
    return decodeURIComponent(results[1].replace(/\+/g, " "));
}


