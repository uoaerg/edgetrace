Array.min = function( array ){
    return Math.min.apply( Math, array );
};

Array.max = function( array ){
    return Math.max.apply( Math, array );
};

var average_center_lats = (Array.min(coordinates['latitude']) + Array.max(coordinates['latitude'])) / 2;
var average_center_lons = (Array.min(coordinates['longitude']) + Array.max(coordinates['longitude'])) / 2;

var mymap = L.map('mapid').setView([average_center_lats, average_center_lons], 1);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);

var coor_length = coordinates['latitude'].length;

var circle = new Array(coor_length);
var lats, lons;
for (i=0; i < coor_length; i++) {
    lats = coordinates['latitude'][i];
    lons = coordinates['longitude'][i];
    
    circle[i] = L.circle([lats, lons], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 100
    }).addTo(mymap);
    
    circle[i].bindPopup(lats + ', ' + lons);
}

var group = new L.featureGroup(circle);
mymap.fitBounds(group.getBounds());

//console.log(group.getBounds()['_northEast'])
