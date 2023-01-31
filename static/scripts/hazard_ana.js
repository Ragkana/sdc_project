//---------------------------------------------------------------------------------------// 
//---------------------------------- Download Map ---------------------------------------//
//---------------------------------------------------------------------------------------//
// ---------------- Global Map dawnload function ---------------- //
function simulateDownloadImageClick(uri, filename) {
    var link = document.createElement('a');
    if (typeof link.download !== 'string') {
        window.open(uri);
    } else {
        link.href = uri;
        link.download = filename;
        accountForFirefox(clickLink, link);
    }
}

function clickLink(link) {
    link.click();
}

function accountForFirefox(click) { // wrapper function
    let link = arguments[1];
    document.body.appendChild(link);
    click(link);
    document.body.removeChild(link);
}

// Change level name from database
function TwoDatalevel(dlev) {
    if (dlev == 'district_name') {
        return 'District';
    }
    if (dlev == 'province_name') {
        return 'Province';
    }
}

function ThreeDatalevel(dlev) {
    if (dlev == 'district_name') {
        return 'District';
    }
    if (dlev == 'commune_name') {
        return 'Commune';
    }
    else {
        return 'Province';
    }
}

// --------------------------------------------------* Cambodia *-------------------------------------------------------------//

function KHMdownloadChartasJPEG() {
    document.getElementById("khm_download_jpg").addEventListener("click", function () {
        html2canvas(document.getElementById("cambodia_map_container"), { allowTaint: true, useCORS: true }).then(function (canvas) {
            //console.log(canvas);
            simulateDownloadImageClick(canvas.toDataURL(), 'KHM_' + khm_haz + '_' + ThreeDatalevel(khm_lev) + '.jpg');
        });
    });
}

// --------------------------------------------------* Laos *-------------------------------------------------------------//

function LAOdownloadChartasJPEG() {
    document.getElementById("lao_download_jpg").addEventListener("click", function () {
        html2canvas(document.getElementById("laos_map_container"), { allowTaint: true, useCORS: true }).then(function (canvas) {
            //console.log(canvas);
            simulateDownloadImageClick(canvas.toDataURL(), 'LAO_' + lao_haz + '_' + TwoDatalevel(lao_lev) + '.jpg');
        });
    });
}


//----------------------------------------------------------------------------------------------------------------//
//--------------------------------------- Global function for leaflet Map ----------------------------------------//
//----------------------------------------------------------------------------------------------------------------//
// Destroy the old map and create the new one.
function destroyExistingMap(map) {
    if (map != undefined || map != null) {
        map.remove();
    }
}

// Assigning color for selected parameter class
function getColor(param, level) {
    if (level == 'province_name' || level == 'district_name') {
        return param == undefined ? '#fff' :
            param > 70 ? '#370001' :
                param > 40 ? '#9B0103' :
                    param > 15 ? '#F78900' :
                        param > 5 ? '#FFB200' :
                            '#FFEABB';
    } if (level == 'commune_name') {
        return param == undefined ? '#fff' :
            param > 90 ? '#370001' :
                param > 60 ? '#9B0103' :
                    param > 40 ? '#F78900' :
                        param > 15 ? '#FFB200' :
                            '#FFEABB';
    }
}

// Map tile selection Function 
function getMapTile(mt) {
    if (mt == 'satellite') {
        return 'http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}';
    }
    if (mt == 'terrain') {
        return 'http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}';
    }
    if (mt == 'base') {
        return 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';
    }
}

//-------------------------------------------------------------------------------------------------------------------------//
//--------------------------------------- Location marker function for leaflet Map ----------------------------------------//
//-------------------------------------------------------------------------------------------------------------------------//
// ------- Location marker image function ------- //
const pinkDot = new L.icon({
    iconUrl: '/static/images/Project_dot_on_map/pink_dot.png',
    iconSize: [14, 14], // size of the icon
    // remember that iconAnchor must always relate to iconSize by [x=x/2,y=y]
    iconAnchor: [7, 14], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -10] // point from which the popup should open relative to the iconAnchor
});

const greenDot = new L.icon({
    iconUrl: '/static/images/Project_dot_on_map/green_dot.png',

    iconSize: [14, 14], // size of the icon
    // remember that iconAnchor must always relate to iconSize by [x=x/2,y=y]
    iconAnchor: [7, 14], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -10] // point from which the popup should open relative to the iconAnchor
});

const purpleDot = new L.icon({
    iconUrl: '/static/images/Project_dot_on_map/purple_dot.png',

    iconSize: [14, 14], // size of the icon
    // remember that iconAnchor must always relate to iconSize by [x=x/2,y=y]
    iconAnchor: [7, 14], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -10] // point from which the popup should open relative to the iconAnchor
});

const orangeDot = new L.icon({
    iconUrl: '/static/images/Project_dot_on_map/orange_dot.png',

    iconSize: [14, 14], // size of the icon
    // remember that iconAnchor must always relate to iconSize by [x=x/2,y=y]
    iconAnchor: [7, 14], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -10] // point from which the popup should open relative to the iconAnchor
});

const yellowDot = new L.icon({
    iconUrl: '/static/images/Project_dot_on_map/yellow_dot.png',

    iconSize: [14, 14], // size of the icon
    // remember that iconAnchor must always relate to iconSize by [x=x/2,y=y]
    iconAnchor: [7, 14], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -10] // point from which the popup should open relative to the iconAnchor
});

const darkpurpleDot = new L.icon({
    iconUrl: '/static/images/Project_dot_on_map/darkpurple_dot.png',
    iconSize: [14, 14], // size of the icon
    // remember that iconAnchor must always relate to iconSize by [x=x/2,y=y]
    iconAnchor: [7, 14], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -10] // point from which the popup should open relative to the iconAnchor
});

const blueDot = new L.icon({
    iconUrl: '/static/images/Project_dot_on_map/blue_dot.png',
    iconSize: [14, 14], // size of the icon
    // remember that iconAnchor must always relate to iconSize by [x=x/2,y=y]
    iconAnchor: [7, 14], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -10] // point from which the popup should open relative to the iconAnchor
});

const lightblueDot = new L.icon({
    iconUrl: '/static/images/Project_dot_on_map/lightblue_dot.png',
    iconSize: [14, 14], // size of the icon
    // remember that iconAnchor must always relate to iconSize by [x=x/2,y=y]
    iconAnchor: [7, 14], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -10] // point from which the popup should open relative to the iconAnchor
});

const lightgreenDot = new L.icon({
    iconUrl: '/static/images/Project_dot_on_map/lightgreen_dot.png',
    iconSize: [14, 14], // size of the icon
    // remember that iconAnchor must always relate to iconSize by [x=x/2,y=y]
    iconAnchor: [7, 14], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -10] // point from which the popup should open relative to the iconAnchor
});

const lightpinkDot = new L.icon({
    iconUrl: '/static/images/Project_dot_on_map/lightpink_dot.png',
    iconSize: [14, 14], // size of the icon
    // remember that iconAnchor must always relate to iconSize by [x=x/2,y=y]
    iconAnchor: [7, 14], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -10] // point from which the popup should open relative to the iconAnchor
});

const whiteDot = new L.icon({
    iconUrl: '/static/images/Project_dot_on_map/white_dot.png',
    iconSize: [14, 14], // size of the icon
    // remember that iconAnchor must always relate to iconSize by [x=x/2,y=y]
    iconAnchor: [7, 14], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -10] // point from which the popup should open relative to the iconAnchor
});

// ------- Project Marker color ------- //
function markerColor(val) {
    if (val == 0) {
        return pinkDot;
    }
    if (val == 1) {
        return greenDot;
    }
    if (val == 2) {
        return purpleDot;
    }
    if (val == 3) {
        return orangeDot;
    }
    if (val == 4) {
        return blueDot;
    }
    if (val == 5) {
        return yellowDot;
    }
    if (val == 6) {
        return lightgreenDot;
    }
    if (val == 7) {
        return darkpurpleDot;
    }
    if (val == 8) {
        return lightblueDot;
    }
    if (val == 9) {
        return whiteDot;
    }
    else {
        return lightpinkDot;
    }
}

// ------- Cambodia SDC project Marker color notation in box ------- //
function KHM_MakerNoteBox(arr) {
    var marker_arr = [];
    for (var i = 0; i < arr.length; i++) {
        if (i == 0) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/pink_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 1) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/green_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 2) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/purple_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 3) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/orange_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 4) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/blue_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 5) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/yellow_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 6) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/lightgreen_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 7) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/darkpurple_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 8) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/lightblue_dot.png' style='width:1rem'> " + arr[i]);
        }
        else if (i >= 9) {
            marker_arr.push("<img src='/static/images/Project_dot_on_map/lightpink_dot.png' style='width:1rem'> " + arr[i]);
        }

    }
    return document.getElementById('KHM_project_show').innerHTML = marker_arr;
}

// ------- Cambodia SDC project Marker color notation in box ------- //
function LAO_MakerNoteBox(arr) {
    var marker_arr = [];
    for (var i = 0; i < arr.length; i++) {
        if (i == 0) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/pink_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 1) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/green_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 2) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/purple_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 3) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/orange_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 4) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/blue_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 5) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/yellow_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 6) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/lightgreen_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 7) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/darkpurple_dot.png' style='width:1rem'> " + arr[i]);
        }
        if (i == 8) {
            marker_arr.push(" <img src='/static/images/Project_dot_on_map/lightblue_dot.png' style='width:1rem'> " + arr[i]);
        }
        else if (i >= 9) {
            marker_arr.push("<img src='/static/images/Project_dot_on_map/lightpink_dot.png' style='width:1rem'> " + arr[i]);
        }

    }
    return document.getElementById('LAO_project_show').innerHTML = marker_arr;
}

//-----------------------------------------------------------------------------------------------------//
//--------------------------------------- Cambodia leaflet Map ----------------------------------------//
//----------------------------------------------------------------------------------------------------//
var cam_map;

// ------- Cambodis Project Marker ------- //
function KHM_createMarker(arr) {
    var Group = L.layerGroup([]);
    for (var p in KHM_project) {
        var obj = KHM_project[p];

        for (var ind = 0; ind < arr.length; ind++) {
            if (obj.Project == arr[ind]) {
                var khm_loc = L.marker(obj.location, { icon: markerColor(ind) }).bindPopup(obj.Project);
                khm_loc.addTo(Group);
            }
        }

    }
    return Group;
}

// ------- Cambodis Leaflet Map Generate Function ------- //
function KHM_MapChart(data, arr) {
    destroyExistingMap(cam_map);
    cam_map = L.map('cam_map', {
        zoomControl: false,
        minZoom: 3,     // Max Zoom out
        maxZoom: 12,    // Max Zoom in
        attributionControl: false, // Remove leaflet logo
        scrollWheelZoom: false, // You can't get the correct screenshot If allow to use scroll.
        preferCanvas: true
    }).setView([12.562108, 104.888535], 7);
    //L.tileLayer('https://api.mapbox.com/styles/v1/nazmul-rimes/ck9wljpn30kbx1is5a630hmtb/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibmF6bXVsLXJpbWVzIiwiYSI6ImNrOWFzeHNtcDA3MjAzbG50dnB0YmkxNnAifQ.usNB6Kf9PyFtKTUF1XI38g').addTo(cam_map);
    //L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
    if (KHM_MapTile == 'base_w') {
        L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png').addTo(cam_map);
    }
    else {
        L.tileLayer(getMapTile(KHM_MapTile), {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        }).addTo(cam_map);
    }


    // Add Zoom button
    L.control.zoom({
        position: 'topleft'
    }).addTo(cam_map);

    function style(feature) {
        return {
            fillColor: getColor(feature.properties.percentage, data.lev),
            fillOpacity: 0.7,
            weight: 2,
            opacity: 1,
            color: '#2F96B2',
            dashArray: '3'
        };
    }

    // Add interaction
    function highlightFeature(e) {
        var layer = e.target;
        // Don't show highlightFeature function if there is no data.
        if (layer.feature.properties.value !== undefined) {
            layer.setStyle({
                weight: 5,
                color: '#2F96B2',
                dashArray: '',
                fillOpacity: 0.7
            });

            if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                layer.bringToFront();
            }
            // Add Info popup when mouseover
            if (data.lev == 'province_name') {
                layer.bindPopup('<b>' + data.haz + '</b><br>' + layer.feature.properties.Province + ' : ' + layer.feature.properties.value).openPopup();
                layer.on('mouseout', function () {
                    this.closePopup();
                });
            }
            if (data.lev == 'district_name') {
                layer.bindPopup('<b>' + data.haz + '</b><br>' + layer.feature.properties.District + ' : ' + layer.feature.properties.value).openPopup();
                layer.on('mouseout', function () {
                    this.closePopup();
                });
            }
            if (data.lev == 'commune_name') {
                layer.bindPopup('<b>' + data.haz + '</b><br>' + layer.feature.properties.Commune + ' : ' + layer.feature.properties.value).openPopup();
                layer.on('mouseout', function () {
                    this.closePopup();
                });
            }

        }
    }

    function resetHighlight(e) {
        geojson.resetStyle(e.target);
    }

    // Zoom
    function zoomToFeature(e) {
        cam_map.fitBounds(e.target.getBounds());
    }


    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: zoomToFeature
        });
    }

    // Retrieve Map data
    var KHM_map = data.map_data

    geojson = L.geoJson(KHM_map, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(cam_map);

    // Add SDC Project location
    var KHM_marker = KHM_createMarker(arr);
    KHM_marker.addTo(cam_map);

}


//-----------------------------------------------------------------------------------------------------//
//----------------------------------------- Laos leaflet Map -----------------------------------------//
//----------------------------------------------------------------------------------------------------//
var lao_map;

// ------- laos Project Marker ------- //
function LAO_createMarker(arr) {
    var Group = L.layerGroup([]);
    for (var p in LAO_project) {
        var obj = LAO_project[p];

        for (var ind = 0; ind < arr.length; ind++) {
            if (obj.Project == arr[ind]) {
                var lao_loc = L.marker(obj.location, { icon: markerColor(ind) }).bindPopup(obj.Project);
                lao_loc.addTo(Group);
            }
        }

    }
    return Group;
}

function LAO_MapChart(data, arr) {
    destroyExistingMap(lao_map);
    lao_map = L.map('lao_map', {
        zoomControl: false,
        minZoom: 3,     // Max Zoom out
        maxZoom: 12,    // Max Zoom in
        attributionControl: false, // Remove leaflet logo
        scrollWheelZoom: false, // You can't get the correct screenshot If allow to use scroll.
        preferCanvas: true
    }).setView([17.6384, 105.2195], 6);
    if (LAO_MapTile == 'base_w') {
        L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png').addTo(lao_map);
    }
    else {
        L.tileLayer(getMapTile(LAO_MapTile), {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        }).addTo(lao_map);
    }

    // Add Zoom button
    L.control.zoom({
        position: 'topleft'
    }).addTo(lao_map);

    function style(feature) {
        return {
            fillColor: getColor(feature.properties.percentage, data.lev),
            fillOpacity: 0.7,
            weight: 2,
            opacity: 1,
            color: '#2F96B2',
            dashArray: '3'
        };
    }

    // Add interaction
    function highlightFeature(e) {
        var layer = e.target;
        // Don't show highlightFeature function if there is no data.
        if (layer.feature.properties.value !== undefined) {
            layer.setStyle({
                weight: 5,
                color: '#2F96B2',
                dashArray: '',
                fillOpacity: 0.7
            });

            if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                layer.bringToFront();
            }
            // Add Info popup when mouseover
            if (data.lev == 'province_name') {
                layer.bindPopup('<b>' + data.haz + '</b><br>' + layer.feature.properties.Province + ' : ' + layer.feature.properties.value).openPopup();
                layer.on('mouseout', function () {
                    this.closePopup();
                });
            }
            if (data.lev == 'district_name') {
                layer.bindPopup('<b>' + data.haz + '</b><br>' + layer.feature.properties.District + ' : ' + layer.feature.properties.value).openPopup();
                layer.on('mouseout', function () {
                    this.closePopup();
                });
            }

        }
    }

    function resetHighlight(e) {
        geojson.resetStyle(e.target);
    }

    // Zoom
    function zoomToFeature(e) {
        lao_map.fitBounds(e.target.getBounds());
    }


    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: zoomToFeature
        });
    }

    // Retrieve Map data
    var LAO_map = data.map_data

    geojson = L.geoJson(LAO_map, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(lao_map);

    // Add SDC Project location
    var LAO_marker = LAO_createMarker(arr);
    LAO_marker.addTo(lao_map);

}


//--------------------------------------------------------------------------------------------------------------------------//
//----------------------------------------- GeoJSON generate and download function -----------------------------------------//
//-------------------------------------------------------------------------------------------------------------------------//

function download(content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([content], { type: contentType });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}

//--------* Cambodia *--------//
function KHM_onDownload_JSON(data) {
    //console.log(data.mapdata_out);
    download(JSON.stringify(data.mapdata_out), "KHM_" + data.haz + "_" + ThreeDatalevel(data.lev) + ".geojson", "text/plain");
}

function KHM_onDownload_TIFF(data) {
    //console.log(data.mapdata_out);
    download(JSON.stringify(data.mapdata_out), "KHM_" + data.haz + "_" + ThreeDatalevel(data.lev) + ".tiff", "text/plain");
}

//--------* Laos *--------//
function LAO_onDownload_JSON(data) {
    //console.log(data.mapdata_out);
    download(JSON.stringify(data.mapdata_out), "LAO_" + data.haz + "_" + TwoDatalevel(data.lev) + ".geojson", "text/plain");
}

function LAO_onDownload_TIFF(data) {
    //console.log(data.mapdata_out);
    download(JSON.stringify(data.mapdata_out), "LAO_" + data.haz + "_" + TwoDatalevel(data.lev) + ".tiff", "text/plain");
}

