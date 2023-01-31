//------------* Global function for map *------------//
// Assigning color for selected parameter class
function getColor(cond, param) {
    if (cond == 'rainfall') {
        return param > 225.10 ? '#F1F624' :
            param > 175.30 ? '#FA9C3C' :
                param > 125.50 ? '#DA5A69' :
                    param > 75.70 ? '#A62098' :
                        param > 25.90 ? '#6400A7' :
                            '#120789';
    }
    if (cond == 'humidity') {
        return param > 86.00 ? '#058266' :
            param > 68.00 ? '#52A86B' :
                param > 50.00 ? '#84C26A' :
                    param > 32.00 ? '#B2D867' :
                        param > 14.00 ? '#D7EB67' :
                            '#FCFD66';
    }
    if (cond == 'max_temp' || cond == 'min_temp') {
        return param > 39.50 ? '#F2F524' :
            param > 28.50 ? '#F79651' :
                param > 17.50 ? '#D04E73' :
                    param > 6.50 ? '#7E3390' :
                        param > -4.50 ? '#5602A4' :
                            '#120889';
    }
    if (cond == 'windspeed') {
        return param > 99.10 ? '#0B1F5D' :
            param > 77.30 ? '#235EA7' :
                param > 55.50 ? '#33A7C2' :
                    param > 33.70 ? '#8BD1B9' :
                        param > 11.90 ? '#E5F5B1' :
                            '#FEFFD7';
    }
}

// Destroy the old map and create the new one.
function destroyExistingMap(map) {
    if (map != undefined || map != null) {
        map.remove();
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

//-----------------------------------------------------------------------------------------------------//
//--------------------------------------- Cambodia leaflet Map ----------------------------------------//
//----------------------------------------------------------------------------------------------------//
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
//------------* Cambodia map Function *------------//
var cam_map;

function KHM_MapChart(data, arr) {
    var wfparam = data.wf_param;
    destroyExistingMap(cam_map);
    cam_map = L.map('cam_map', {
        zoomControl: false,
        minZoom: 3,     // Max Zoom out
        maxZoom: 9,    // Max Zoom in
        attributionControl: false // Remove leaflet logo
    }).setView([12.562108, 104.888535], 7);
    //L.tileLayer('https://api.mapbox.com/styles/v1/nazmul-rimes/ck9wljpn30kbx1is5a630hmtb/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibmF6bXVsLXJpbWVzIiwiYSI6ImNrOWFzeHNtcDA3MjAzbG50dnB0YmkxNnAifQ.usNB6Kf9PyFtKTUF1XI38g').addTo(cam_map);
    L.tileLayer(getMapTile(KHM_MapTile), {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    }).addTo(cam_map);

    function style(feature) {
        return {
            fillColor: getColor(wfparam, feature.properties[wfparam]),
            weight: 2,
            opacity: 1,
            color: '#9B0103',
            dashArray: '3',
            fillOpacity: 0.8
        };
    }
    // load json data recieve from views.py
    var khm_mapData = data.khm_map_data;
    //L.geoJson(khm_mapData, { style: style }).addTo(cam_map);

    // Add Zoom button
    L.control.zoom({
        position: 'topleft'
    }).addTo(cam_map);

    // Add interaction
    function highlightFeature(e) {
        var layer = e.target;

        layer.setStyle({
            weight: 5,
            color: '#9B0103',
            dashArray: '',
            fillOpacity: 0.7
        });

        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
        // Add Info popup when mouseover
        layer.bindPopup('<b>' + wfparam + '</b><br>' + layer.feature.properties.Province + ' : ' + layer.feature.properties[wfparam]).openPopup();
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

    geojson = L.geoJson(khm_mapData, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(cam_map);

    // Add SDC Project location
    var KHM_marker = KHM_createMarker(arr);
    KHM_marker.addTo(cam_map);

}

//--------------------------------------------------------------------------------------------------//
//--------------------------------------- Laos leaflet Map ----------------------------------------//
//-------------------------------------------------------------------------------------------------//
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
    var wfparam = data.wf_param;
    destroyExistingMap(lao_map);
    lao_map = L.map('lao_map', {
        zoomControl: false,
        minZoom: 3,     // Max Zoom out
        maxZoom: 9,    // Max Zoom in
        attributionControl: false // Remove leaflet logo
    }).setView([17.6384, 105.2195], 6);
    L.tileLayer(getMapTile(LAO_MapTile), {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    }).addTo(lao_map);

    function style(feature) {
        return {
            fillColor: getColor(wfparam, feature.properties[wfparam]),
            weight: 2,
            opacity: 1,
            color: '#9B0103',
            dashArray: '3',
            fillOpacity: 0.7
        };
    }
    // load json data recieve from views.py
    var lao_mapData = data.lao_map_data;
    //L.geoJson(khm_mapData, { style: style }).addTo(cam_map);

    // Add Zoom button
    L.control.zoom({
        position: 'topleft'
    }).addTo(lao_map);

    // Add interaction
    function highlightFeature(e) {
        var layer = e.target;

        layer.setStyle({
            weight: 5,
            color: '#9B0103',
            dashArray: '',
            fillOpacity: 0.7
        });

        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
        // Add Info popup when mouseover
        layer.bindPopup('<b>' + wfparam + '</b><br>' + layer.feature.properties.Province + ' : ' + layer.feature.properties[wfparam]).openPopup();
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

    geojson = L.geoJson(lao_mapData, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(lao_map);

    // Add SDC Project location
    var LAO_marker = LAO_createMarker(arr);
    LAO_marker.addTo(lao_map);

}


//-----------------------------------------------------------------------------------------------------//
//--------------------------------------- Myanmar leaflet Map ----------------------------------------//
//----------------------------------------------------------------------------------------------------//
var mya_map = L.map('mya_map', {
    zoomControl: false,
    minZoom: 3,     // Max Zoom out
    maxZoom: 9,    // Max Zoom in
}).setView([20.00, 95.00], 5);
L.tileLayer(getMapTile(MYA_MapTile), {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
}).addTo(mya_map);

//---------------------------------------------------------------------------------------------//
//--------------------------------------- JS for Tab  ----------------------------------------//
//--------------------------------------------------------------------------------------------//
//-----*Main Tab*-----//
$(document).ready(function () {
    $("#myTab a").click(function (t) {
        t.preventDefault();
        $(this).tab("show");
    });
});

//---------* Make the map avaliable in each tab *---------//
var camTab = document.getElementById('cambodia');
var observer1 = new MutationObserver(function () {
    if (camTab.style.display != 'none') {
        cam_map.invalidateSize();
    }
});
observer1.observe(camTab, { attributes: true });

var laoTab = document.getElementById('laos');
var observer2 = new MutationObserver(function () {
    if (laoTab.style.display != 'none') {
        lao_map.invalidateSize();
    }
});
observer2.observe(laoTab, { attributes: true });

var myaTab = document.getElementById('myanmar');
var observer3 = new MutationObserver(function () {
    if (myaTab.style.display != 'none') {
        mya_map.invalidateSize();
    }
});
observer3.observe(myaTab, { attributes: true });

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

// ------- Laos SDC project Marker color notation in box ------- //
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

//----------------------------------------------------------------------------------------------//
//--------------------------------------- Date Picker  ----------------------------------------//
//--------------------------------------------------------------------------------------------//
// Cambodia : Date picker
$(document).ready(function () {
    $('#datepicker_cambodia').datepicker({
        clearBtn: true,
        todayHighlight: true,
        autoclose: true, // When date has been selected
        immediateUpdates: true,
        orientation: 'auto bottom',
        language: 'en',
        endDate: new Date(), // cant select tomorrow on date-picker
        format: 'yyyy-mm-dd'
    });

    $('#datepicker_cambodia').datepicker('setDate', 'today').date();
});

// Laos : Date picker
$(document).ready(function () {
    $('#datepicker_laos').datepicker({
        clearBtn: true,
        todayHighlight: true,
        autoclose: true, // When date has been selected
        immediateUpdates: true,
        orientation: 'auto bottom',
        language: 'en',
        endDate: new Date(), // cant select tomorrow on date-picker
        format: 'yyyy-mm-dd'
    });

    $('#datepicker_laos').datepicker('setDate', 'today').date();
});

//----------------------------------------------------------------------------------------------------//
//--------------------------------------- Legend map function ----------------------------------------//
//----------------------------------------------------------------------------------------------------//
function KHM_LegendBar(param) {
    if (param == 'rainfall') {
        document.getElementById("khm_cbar").style.background = "linear-gradient(to right, rgb(13, 8, 135), rgb(27, 6, 141), rgb(38, 5, 145), rgb(47, 5, 150), rgb(56, 4, 154), rgb(67, 3, 158), rgb(75, 3, 161), rgb(83, 2, 163), rgb(91, 1, 165), rgb(100, 0, 167), rgb(108, 0, 168), rgb(116, 1, 168), rgb(123, 2, 168), rgb(131, 5, 167), rgb(139, 10, 165), rgb(146, 15, 163), rgb(153, 21, 159), rgb(160, 26, 156), rgb(167, 33, 151), rgb(173, 39, 147), rgb(179, 44, 142), rgb(184, 50, 137), rgb(190, 56, 133), rgb(196, 62, 127), rgb(201, 68, 122), rgb(205, 74, 118), rgb(210, 79, 113), rgb(215, 86, 108), rgb(219, 92, 104), rgb(223, 98, 99), rgb(227, 104, 95), rgb(231, 110, 91), rgb(235, 117, 86), rgb(238, 123, 81), rgb(241, 129, 77), rgb(244, 136, 73), rgb(247, 144, 68), rgb(249, 151, 63), rgb(250, 158, 59), rgb(252, 165, 55), rgb(253, 172, 51), rgb(253, 181, 46), rgb(254, 189, 42), rgb(253, 197, 39), rgb(252, 205, 37), rgb(251, 215, 36), rgb(248, 223, 37), rgb(246, 232, 38), rgb(243, 240, 39), rgb(240, 249, 33))";
        document.getElementById("khm_cbar_value").innerHTML = "<td>25.90</td><td>75.70</td><td>125.50</td><td>175.30</td><td>225.10</td>";
    }
    if (param == 'humidity') {
        document.getElementById("khm_cbar").style.background = "linear-gradient(to right, rgb(255, 255, 102), rgb(250, 252, 102), rgb(245, 250, 102), rgb(239, 247, 102), rgb(234, 245, 102), rgb(229, 242, 102), rgb(224, 239, 102), rgb(219, 237, 102), rgb(213, 234, 102), rgb(208, 232, 102), rgb(203, 229, 102), rgb(198, 226, 102), rgb(193, 224, 102), rgb(187, 221, 102), rgb(182, 219, 102), rgb(177, 216, 102), rgb(172, 213, 102), rgb(167, 211, 102), rgb(161, 208, 102), rgb(156, 206, 102), rgb(151, 203, 102), rgb(146, 200, 102), rgb(141, 198, 102), rgb(135, 195, 102), rgb(130, 193, 102), rgb(125, 190, 102), rgb(120, 187, 102), rgb(114, 185, 102), rgb(109, 182, 102), rgb(104, 180, 102), rgb(99, 177, 102), rgb(94, 174, 102), rgb(88, 172, 102), rgb(83, 169, 102), rgb(78, 167, 102), rgb(73, 164, 102), rgb(68, 161, 102), rgb(62, 159, 102), rgb(57, 156, 102), rgb(52, 154, 102), rgb(47, 151, 102), rgb(42, 148, 102), rgb(36, 146, 102), rgb(31, 143, 102), rgb(26, 141, 102), rgb(21, 138, 102), rgb(16, 135, 102), rgb(10, 133, 102), rgb(5, 130, 102), rgb(0, 128, 102))";
        document.getElementById("khm_cbar_value").innerHTML = "<td>14.00</td><td>32.00</td><td>50.00</td><td>68.00</td><td>86.00</td>";
    }
    if (param == 'max_temp' || param == 'min_temp') {
        document.getElementById("khm_cbar").style.background = "linear-gradient(to right, rgb(13, 8, 135), rgb(27, 6, 141), rgb(38, 5, 145), rgb(47, 5, 150), rgb(56, 4, 154), rgb(67, 3, 158), rgb(75, 3, 161), rgb(83, 2, 163), rgb(91, 1, 165), rgb(100, 0, 167), rgb(108, 0, 168), rgb(116, 1, 168), rgb(123, 2, 168), rgb(131, 5, 167), rgb(139, 10, 165), rgb(146, 15, 163), rgb(153, 21, 159), rgb(160, 26, 156), rgb(167, 33, 151), rgb(173, 39, 147), rgb(179, 44, 142), rgb(184, 50, 137), rgb(190, 56, 133), rgb(196, 62, 127), rgb(201, 68, 122), rgb(205, 74, 118), rgb(210, 79, 113), rgb(215, 86, 108), rgb(219, 92, 104), rgb(223, 98, 99), rgb(227, 104, 95), rgb(231, 110, 91), rgb(235, 117, 86), rgb(238, 123, 81), rgb(241, 129, 77), rgb(244, 136, 73), rgb(247, 144, 68), rgb(249, 151, 63), rgb(250, 158, 59), rgb(252, 165, 55), rgb(253, 172, 51), rgb(253, 181, 46), rgb(254, 189, 42), rgb(253, 197, 39), rgb(252, 205, 37), rgb(251, 215, 36), rgb(248, 223, 37), rgb(246, 232, 38), rgb(243, 240, 39), rgb(240, 249, 33))";
        document.getElementById("khm_cbar_value").innerHTML = "<td>-4.50</td><td>6.50</td><td>17.50</td><td>28.50</td><td>39.50</td>";
    }
    if (param == 'windspeed') {
        document.getElementById("khm_cbar").style.background = "linear-gradient(to right, rgb(255, 255, 217), rgb(252, 254, 210), rgb(249, 253, 204), rgb(246, 252, 197), rgb(243, 250, 191), rgb(240, 249, 184), rgb(237, 248, 178), rgb(232, 246, 177), rgb(225, 243, 178), rgb(219, 241, 178), rgb(213, 239, 179), rgb(207, 236, 179), rgb(201, 234, 180), rgb(190, 230, 181), rgb(178, 225, 182), rgb(167, 220, 183), rgb(155, 216, 184), rgb(143, 211, 185), rgb(131, 207, 187), rgb(121, 203, 188), rgb(111, 199, 189), rgb(100, 195, 191), rgb(90, 191, 192), rgb(80, 188, 194), rgb(70, 184, 195), rgb(62, 179, 196), rgb(56, 173, 195), rgb(50, 167, 194), rgb(44, 161, 194), rgb(39, 155, 193), rgb(33, 149, 192), rgb(29, 142, 191), rgb(30, 134, 187), rgb(31, 125, 183), rgb(32, 117, 179), rgb(33, 109, 175), rgb(33, 100, 171), rgb(34, 92, 167), rgb(35, 85, 164), rgb(35, 79, 161), rgb(36, 72, 157), rgb(36, 65, 154), rgb(37, 58, 151), rgb(36, 52, 147), rgb(32, 48, 137), rgb(27, 44, 127), rgb(22, 40, 117), rgb(17, 37, 108), rgb(13, 33, 98), rgb(8, 29, 88))";
        document.getElementById("khm_cbar_value").innerHTML = "<td>11.90</td><td>33.70</td><td>55.50</td><td>77.30</td><td>99.10</td>";
    }
}

function LAO_LegendBar(param) {
    if (param == 'rainfall') {
        document.getElementById("lao_cbar").style.background = "linear-gradient(to right, rgb(13, 8, 135), rgb(27, 6, 141), rgb(38, 5, 145), rgb(47, 5, 150), rgb(56, 4, 154), rgb(67, 3, 158), rgb(75, 3, 161), rgb(83, 2, 163), rgb(91, 1, 165), rgb(100, 0, 167), rgb(108, 0, 168), rgb(116, 1, 168), rgb(123, 2, 168), rgb(131, 5, 167), rgb(139, 10, 165), rgb(146, 15, 163), rgb(153, 21, 159), rgb(160, 26, 156), rgb(167, 33, 151), rgb(173, 39, 147), rgb(179, 44, 142), rgb(184, 50, 137), rgb(190, 56, 133), rgb(196, 62, 127), rgb(201, 68, 122), rgb(205, 74, 118), rgb(210, 79, 113), rgb(215, 86, 108), rgb(219, 92, 104), rgb(223, 98, 99), rgb(227, 104, 95), rgb(231, 110, 91), rgb(235, 117, 86), rgb(238, 123, 81), rgb(241, 129, 77), rgb(244, 136, 73), rgb(247, 144, 68), rgb(249, 151, 63), rgb(250, 158, 59), rgb(252, 165, 55), rgb(253, 172, 51), rgb(253, 181, 46), rgb(254, 189, 42), rgb(253, 197, 39), rgb(252, 205, 37), rgb(251, 215, 36), rgb(248, 223, 37), rgb(246, 232, 38), rgb(243, 240, 39), rgb(240, 249, 33))";
        document.getElementById("lao_cbar_value").innerHTML = "<td>25.90</td><td>75.70</td><td>125.50</td><td>175.30</td><td>225.10</td>";
    }
    if (param == 'humidity') {
        document.getElementById("lao_cbar").style.background = "linear-gradient(to right, rgb(255, 255, 102), rgb(250, 252, 102), rgb(245, 250, 102), rgb(239, 247, 102), rgb(234, 245, 102), rgb(229, 242, 102), rgb(224, 239, 102), rgb(219, 237, 102), rgb(213, 234, 102), rgb(208, 232, 102), rgb(203, 229, 102), rgb(198, 226, 102), rgb(193, 224, 102), rgb(187, 221, 102), rgb(182, 219, 102), rgb(177, 216, 102), rgb(172, 213, 102), rgb(167, 211, 102), rgb(161, 208, 102), rgb(156, 206, 102), rgb(151, 203, 102), rgb(146, 200, 102), rgb(141, 198, 102), rgb(135, 195, 102), rgb(130, 193, 102), rgb(125, 190, 102), rgb(120, 187, 102), rgb(114, 185, 102), rgb(109, 182, 102), rgb(104, 180, 102), rgb(99, 177, 102), rgb(94, 174, 102), rgb(88, 172, 102), rgb(83, 169, 102), rgb(78, 167, 102), rgb(73, 164, 102), rgb(68, 161, 102), rgb(62, 159, 102), rgb(57, 156, 102), rgb(52, 154, 102), rgb(47, 151, 102), rgb(42, 148, 102), rgb(36, 146, 102), rgb(31, 143, 102), rgb(26, 141, 102), rgb(21, 138, 102), rgb(16, 135, 102), rgb(10, 133, 102), rgb(5, 130, 102), rgb(0, 128, 102))";
        document.getElementById("lao_cbar_value").innerHTML = "<td>14.00</td><td>32.00</td><td>50.00</td><td>68.00</td><td>86.00</td>";
    }
    if (param == 'max_temp' || param == 'min_temp') {
        document.getElementById("lao_cbar").style.background = "linear-gradient(to right, rgb(13, 8, 135), rgb(27, 6, 141), rgb(38, 5, 145), rgb(47, 5, 150), rgb(56, 4, 154), rgb(67, 3, 158), rgb(75, 3, 161), rgb(83, 2, 163), rgb(91, 1, 165), rgb(100, 0, 167), rgb(108, 0, 168), rgb(116, 1, 168), rgb(123, 2, 168), rgb(131, 5, 167), rgb(139, 10, 165), rgb(146, 15, 163), rgb(153, 21, 159), rgb(160, 26, 156), rgb(167, 33, 151), rgb(173, 39, 147), rgb(179, 44, 142), rgb(184, 50, 137), rgb(190, 56, 133), rgb(196, 62, 127), rgb(201, 68, 122), rgb(205, 74, 118), rgb(210, 79, 113), rgb(215, 86, 108), rgb(219, 92, 104), rgb(223, 98, 99), rgb(227, 104, 95), rgb(231, 110, 91), rgb(235, 117, 86), rgb(238, 123, 81), rgb(241, 129, 77), rgb(244, 136, 73), rgb(247, 144, 68), rgb(249, 151, 63), rgb(250, 158, 59), rgb(252, 165, 55), rgb(253, 172, 51), rgb(253, 181, 46), rgb(254, 189, 42), rgb(253, 197, 39), rgb(252, 205, 37), rgb(251, 215, 36), rgb(248, 223, 37), rgb(246, 232, 38), rgb(243, 240, 39), rgb(240, 249, 33))";
        document.getElementById("lao_cbar_value").innerHTML = "<td>-4.50</td><td>6.50</td><td>17.50</td><td>28.50</td><td>39.50</td>";
    }
    if (param == 'windspeed') {
        document.getElementById("lao_cbar").style.background = "linear-gradient(to right, rgb(255, 255, 217), rgb(252, 254, 210), rgb(249, 253, 204), rgb(246, 252, 197), rgb(243, 250, 191), rgb(240, 249, 184), rgb(237, 248, 178), rgb(232, 246, 177), rgb(225, 243, 178), rgb(219, 241, 178), rgb(213, 239, 179), rgb(207, 236, 179), rgb(201, 234, 180), rgb(190, 230, 181), rgb(178, 225, 182), rgb(167, 220, 183), rgb(155, 216, 184), rgb(143, 211, 185), rgb(131, 207, 187), rgb(121, 203, 188), rgb(111, 199, 189), rgb(100, 195, 191), rgb(90, 191, 192), rgb(80, 188, 194), rgb(70, 184, 195), rgb(62, 179, 196), rgb(56, 173, 195), rgb(50, 167, 194), rgb(44, 161, 194), rgb(39, 155, 193), rgb(33, 149, 192), rgb(29, 142, 191), rgb(30, 134, 187), rgb(31, 125, 183), rgb(32, 117, 179), rgb(33, 109, 175), rgb(33, 100, 171), rgb(34, 92, 167), rgb(35, 85, 164), rgb(35, 79, 161), rgb(36, 72, 157), rgb(36, 65, 154), rgb(37, 58, 151), rgb(36, 52, 147), rgb(32, 48, 137), rgb(27, 44, 127), rgb(22, 40, 117), rgb(17, 37, 108), rgb(13, 33, 98), rgb(8, 29, 88))";
        document.getElementById("lao_cbar_value").innerHTML = "<td>11.90</td><td>33.70</td><td>55.50</td><td>77.30</td><td>99.10</td>";
    }
}