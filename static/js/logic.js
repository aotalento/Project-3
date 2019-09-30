// Creating map object
var myMap = L.map("map", {
  center: [30.7, -10.95],
  zoom: 3
});

// Adding tile layer to the map
var baseMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);

// Assemble API query URL
var url = 'static/data/OrgData.geojson';

// Grab the data with d3
d3.json(url, function(response) {
  console.log(response.features[1].properties)
  
  // Create a new marker cluster group
  var markers = L.markerClusterGroup();
  
  // Loop through data
  for (var i = 0; i < response.features.length; i++) {

    // Set the data location property to a variable
    var location = response.features[i].geometry;
    var props = response.features[i].properties

    var list = "<dl><dt>Name</dt>"
           + "<dd>" + props.Name + "</dd>"
           + "<dt>Age</dt>"
           + "<dd>" + props.Age + "</dd>"
           + "<dt>Branch</dt>"
           + "<dd>" + props.Branch + "</dd>"
           + "<dt>Rank</dt>"
           + "<dd>" + props.Rank + "</dd>"
           + "<dt>From</dt>"
           + "<dd>" + props.City + "</dd>"
           + "<dd>" + props.State + "</dd>"
           + "<dt>Died</dt>"
           + "<dd>" + props.Where + "</dd>"
           + "<dt>Date</dt>"
           + "<dd>" + props.Date + "</dd>"
           
    // Check for location property
    if (location) {

      // Add a new marker to the cluster group and bind a pop-up
      markers.addLayer(L.marker([location.coordinates[1], location.coordinates[0]])
        .bindPopup(list));
    }

  }

  // Add our marker cluster layer to the map
  myMap.addLayer(markers);

});
