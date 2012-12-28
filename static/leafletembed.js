var map;
var ajaxRequest;
var plotlist;
var plotlayers=[];
var footprintPolygon;

function onClick(e) {
  e.target.bindPopup(e.target.data, {autoPan:false,maxWidth:400})
          .openPopup();
}

function onLocationFound(e) {
    var radius = e.accuracy / 2;

    L.circle(e.latlng, radius).addTo(map);
}

function onLocationError(e) {
  map.stopLocate();
}

function permalink() {
  var center = map.getCenter();
  var lat = Math.round(center.lat * 100000000) / 100000000;
  var lon = Math.round(center.lng * 100000000) / 100000000;
  var serverUrl='http://' + window.location.hostname + '/index.php';
  var layer = map.hasLayer(osmTiles) ? "&layer=osm" : "";
  var newLoc=serverUrl + "?lat=" + lat + "&lon=" + lon + "&zoom=" + map.getZoom() + layer;
  window.location=newLoc;
}

// Layers
var osmTiles;
var mapQuestTiles;


function initmap() {

  // set up AJAX request
  ajaxRequest=getXmlHttpObject();
  if (ajaxRequest==null) {
    alert ("This browser does not support HTTP Request");
    return;
  }

  // set up the map
  map = new L.Map('map');

  // create the tile layers with correct attribution
  var permalink=' — <a href=#" onClick="permalink();return false;">Permalink</a>';
  var dataAttrib='Map data from <a href="http://www.osm.org" target="_blank">OpenStreetMap</a> contributors';

  var osmUrl='/{z}/{x}/{y}.png';
  var osmAttrib=dataAttrib + permalink;
  osmTiles = new L.TileLayer(osmUrl, {minZoom: 2, maxZoom: 18, attribution: osmAttrib});		
  var baseLayers = {
    "MapQuest": mapQuestTiles
  };

  map.setView(new L.LatLng(0,0),2);
  map.addLayer(osmTiles);
  //L.control.layers(baseLayers, null, {position: 'topleft'}).addTo(map);
  askForPlots();
  map.on('moveend', onMapMove);
  map.on('dblclick', onMapClick);
}

function onMapClick(e){
  var marker = L.marker(e.latlng).addTo(map);
  var msg='/marker/?lat='+e.latlng.lat+'&lng='+e.latlng.lng;
  ajaxRequest.onreadystatechange = stateChanged;
  ajaxRequest.open('GET', msg, true);
  ajaxRequest.send(null);
}

function onMapMove(e) { askForPlots(); }

function getXmlHttpObject() {
  if (window.XMLHttpRequest) { return new XMLHttpRequest(); }
  if (window.ActiveXObject)  { return new ActiveXObject("Microsoft.XMLHTTP"); }
  return null;
}

function askForPlots() {
  // request the marker info with AJAX for the current bounds
  var bounds=map.getBounds();
  var minll=bounds.getSouthWest();
  var maxll=bounds.getNorthEast();
  var size=map.getSize();
  var msg='/box/?rect='+minll.lng+','+minll.lat+','+maxll.lng+','+maxll.lat+'&zoom='+map.getZoom()+'&width='+size.x+'&height='+size.y;
  ajaxRequest.onreadystatechange = stateChanged;
  ajaxRequest.open('GET', msg, true);
  ajaxRequest.send(null);
}

function isNumeric(s) {
  var intRegex = /^\d+$/;
  var floatRegex = /^((\d+(\.\d *)?)|((\d*\.)?\d+))$/;
  return ((intRegex.test(s) || floatRegex.test(s)));
}

function drawFootprint(val) {
  val = JSON.parse(val);
  var pts= [];
  for (x in eval(val)) {
    pts.push(new L.LatLng(val[x]['lat'], val[x]['lon'], false));
  }
  if (footprintPolygon != null) {
    map.removeLayer(footprintPolygon);
  }
  footprintPolygon = L.polygon(pts, { color:'blue', weight : 1, fillOpacity:0.1 });
  footprintPolygon.addTo(map);
}

	function stateChanged() {
		// if AJAX returned a list of markers, add them to the map
		if (ajaxRequest.readyState==4) {
			//use the info here that was returned
			if (ajaxRequest.status==200) {
				plotlist=eval("(" + ajaxRequest.responseText + ")");
				removeMarkers();
				for (i=0;i<plotlist.length;i++) {
					var plotll = new L.LatLng(plotlist[i].lat,plotlist[i].lon, true);
					var plotmark = new L.Marker(plotll);
					plotmark.data=plotlist[i];
					map.addLayer(plotmark);
					plotmark.bindPopup("<h3>"+plotlist[i].name+"</h3>"+plotlist[i].details);
					plotlayers.push(plotmark);
				}
			}
		}
	}

function removeMarkers() {
	for (i=0;i<plotlayers.length;i++) {
		map.removeLayer(plotlayers[i]);
	}
	plotlayers=[];
}
initmap()

