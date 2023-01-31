//---------------------------------------------------------------------------------------------//
//-------------------------------------- Other function ---------------------------------------//
//---------------------------------------------------------------------------------------------// 
function ImpactTitleName(data) {
    if (data == 'deaths') {
        return 'Deaths'
    }
    if (data == 'injured') {
        return 'Injured'
    }
    if (data == 'missing') {
        return 'Missing'
    }
    if (data == 'house_destroy') {
        return 'Houses Destroyed'
    }
    if (data == 'house_damage') {
        return 'Houses Damaged'
    }
}

function Datalevel(dlev) {
    if (dlev == 'district_name') {
        return 'District';
    }
    if (dlev == 'commune_name') {
        return 'Commune';
    }
    if (dlev == 'province_name') {
        return 'Province';
    }
}
//--------------------------------------------------------------------------------------// 
//--------------------------------------- Tab ------------------------------------------//
//--------------------------------------------------------------------------------------//
$(document).ready(function () {
    $("#myTab a").click(function (z) {
        z.preventDefault();
        $(this).tab("show");
    });
});

//---------* Make the map avaliable in each tab *---------//
var camTab = document.getElementById('cambodia');
var observer1 = new MutationObserver(function () {
    if (camTab.style.display != 'none') {
        KHM_MapData.invalidateSize();
        KHM_YearSlider.invalidateSize();
    }
});
observer1.observe(camTab, { attributes: true });

var laoTab = document.getElementById('laos');
var observer2 = new MutationObserver(function () {
    if (laoTab.style.display != 'none') {
        LAO_MapData.invalidateSize();
        LAO_YearSlider.invalidateSize();
    }
});
observer2.observe(laoTab, { attributes: true });

var myaTab = document.getElementById('myanmar');
var observer3 = new MutationObserver(function () {
    if (myaTab.style.display != 'none') {
        MYA_MapData.invalidateSize();
        MYA_YearSlider.invalidateSize();
    }
});
observer3.observe(myaTab, { attributes: true });

//----------------------------------------------------------------------------------------------------------------//
//--------------------------------------- Global function for leaflet Map ----------------------------------------//
//----------------------------------------------------------------------------------------------------------------//

// Destroy the old map and create the new one.
function destroyExistingMap(map) {
    if (map != undefined || map != null) {
        map.remove();
    }
}

// choose which map level will show on site by dropdown selection.
function level(lev) {
    if (lev == 'district_name') {
        return camMap_d;
    }
    if (lev == 'commune_name') {
        return camMap_c;
    }
    if (lev == 'province_name') {
        return camMap_p;
    }
}

// Assigning color for selected parameter class
function getColor(param) {
    return param == undefined ? '#fff' :
        param > 80 ? '#370001' :
            param > 60 ? '#9B0103' :
                param > 40 ? '#F78900' :
                    param > 20 ? '#FFB200' :
                        '#FFEABB';
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

//-----------------------------------------------------------------------------------------------------//
//--------------------------------------- Cambodia leaflet Map ----------------------------------------//
//----------------------------------------------------------------------------------------------------//
var KHM_MapData;

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
    destroyExistingMap(KHM_MapData);
    // Retrieve Map data
    var KHM_map = data.map_data

    KHM_MapData = L.map('hc_map01_container', {
        zoomControl: false,
        minZoom: 3,     // Max Zoom out
        maxZoom: 12,    // Max Zoom in
        attributionControl: false, // Remove leaflet logo
        scrollWheelZoom: false, // You can't get the correct screenshot If allow to use scroll.
        preferCanvas: true
    }).setView([12.562108, 104.888535], 7);
    if (KHM_MapTile == 'base_w') {
        L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png').addTo(KHM_MapData);
    }
    else {
        L.tileLayer(getMapTile(KHM_MapTile), {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        }).addTo(KHM_MapData);
    }
    // Add Zoom button
    L.control.zoom({
        position: 'topleft'
    }).addTo(KHM_MapData);

    function style(feature) {
        return {
            fillColor: getColor(feature.properties.percentage),
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
            if (data.level == 'province_name') {
                layer.bindPopup('<b>' + ImpactTitleName(data.impact) + ' from ' + data.dis + '</b><br>' + layer.feature.properties.Province + ' : ' + layer.feature.properties.value).openPopup();
                layer.on('mouseout', function () {
                    this.closePopup();
                });
            }
            if (data.level == 'district_name') {
                layer.bindPopup('<b>' + ImpactTitleName(data.impact) + ' from ' + data.dis + '</b><br>' + layer.feature.properties.District + ' : ' + layer.feature.properties.value).openPopup();
                layer.on('mouseout', function () {
                    this.closePopup();
                });
            }
            if (data.level == 'commune_name') {
                layer.bindPopup('<b>' + ImpactTitleName(data.impact) + ' from ' + data.dis + '</b><br>' + layer.feature.properties.Commune + ' : ' + layer.feature.properties.value).openPopup();
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
        KHM_MapData.fitBounds(e.target.getBounds());
    }


    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: zoomToFeature
        });
    }

    geojson = L.geoJson(KHM_map, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(KHM_MapData);

    // Add SDC Project location
    var KHM_marker = KHM_createMarker(arr);
    KHM_marker.addTo(KHM_MapData);

}

//----------------------------------------------------------------------------------------------------------//
//------------------------------------------- Laos leaflet Map ---------------------------------------------//
//----------------------------------------------------------------------------------------------------------//
var LAO_MapData;
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
    destroyExistingMap(LAO_MapData);
    // Retrieve Map data
    var LAO_map = data.map_data

    LAO_MapData = L.map('hc_map02_container', {
        zoomControl: false,
        minZoom: 3,     // Max Zoom out
        maxZoom: 12,    // Max Zoom in
        attributionControl: false, // Remove leaflet logo
        scrollWheelZoom: false, // You can't get the correct screenshot If allow to use scroll.
        preferCanvas: true
    }).setView([17.6384, 105.2195], 6);
    if (LAO_MapTile == 'base_w') {
        L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png').addTo(LAO_MapData);
    }
    else {
        L.tileLayer(getMapTile(LAO_MapTile), {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        }).addTo(LAO_MapData);
    }

    // Add Zoom button
    L.control.zoom({
        position: 'topleft'
    }).addTo(LAO_MapData);

    function style(feature) {
        return {
            fillColor: getColor(feature.properties.percentage),
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
            if (data.level == 'province_name') {
                layer.bindPopup('<b>' + ImpactTitleName(data.impact) + ' from ' + data.dis + '</b><br>' + layer.feature.properties.Province + ' : ' + layer.feature.properties.value).openPopup();
                layer.on('mouseout', function () {
                    this.closePopup();
                });
            }
            if (data.level == 'district_name') {
                layer.bindPopup('<b>' + ImpactTitleName(data.impact) + ' from ' + data.dis + '</b><br>' + layer.feature.properties.District + ' : ' + layer.feature.properties.value).openPopup();
                layer.on('mouseout', function () {
                    this.closePopup();
                });
            }
            if (data.level == 'commune_name') {
                layer.bindPopup('<b>' + ImpactTitleName(data.impact) + ' from ' + data.dis + '</b><br>' + layer.feature.properties.Commune + ' : ' + layer.feature.properties.value).openPopup();
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
        LAO_MapData.fitBounds(e.target.getBounds());
    }


    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: zoomToFeature
        });
    }

    geojson = L.geoJson(LAO_map, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(LAO_MapData);

    // Add SDC Project location
    var LAO_marker = LAO_createMarker(arr);
    LAO_marker.addTo(LAO_MapData);
}

//-------------------------------------------------------------------------------------------------------------//
//------------------------------------------- Myanmar leaflet Map ---------------------------------------------//
//-------------------------------------------------------------------------------------------------------------//
var MYA_MapData;
// ------- laos Project Marker ------- //
function MYA_createMarker(arr) {
    var Group = L.layerGroup([]);
    for (var p in LAO_project) {
        var obj = LAO_project[p];

        for (var ind = 0; ind < arr.length; ind++) {
            if (obj.Project == arr[ind]) {
                var mya_loc = L.marker(obj.location, { icon: markerColor(ind) }).bindPopup(obj.Project);
                mya_loc.addTo(Group);
            }
        }

    }
    return Group;
}

function MYA_MapChart(data, arr) {
    destroyExistingMap(MYA_MapData);
    // Retrieve Map data
    var MYA_map = data.map_data

    MYA_MapData = L.map('hc_map03_container', {
        zoomControl: false,
        minZoom: 3,     // Max Zoom out
        maxZoom: 12,    // Max Zoom in
        attributionControl: false, // Remove leaflet logo
        scrollWheelZoom: false, // You can't get the correct screenshot If allow to use scroll.
        preferCanvas: true
    }).setView([20.00, 95.00], 5);
    L.tileLayer(getMapTile(MYA_MapTile), {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    }).addTo(MYA_MapData);

    // Add Zoom button
    L.control.zoom({
        position: 'topleft'
    }).addTo(MYA_MapData);

    function style(feature) {
        return {
            fillColor: getColor(feature.properties.percentage),
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
            if (data.level == 'province_name') {
                layer.bindPopup('<b>' + ImpactTitleName(data.impact) + ' from ' + data.dis + '</b><br>' + layer.feature.properties.Province + ' : ' + layer.feature.properties.value).openPopup();
                layer.on('mouseout', function () {
                    this.closePopup();
                });
            }
            if (data.level == 'district_name') {
                layer.bindPopup('<b>' + ImpactTitleName(data.impact) + ' from ' + data.dis + '</b><br>' + layer.feature.properties.District + ' : ' + layer.feature.properties.value).openPopup();
                layer.on('mouseout', function () {
                    this.closePopup();
                });
            }
            if (data.level == 'commune_name') {
                layer.bindPopup('<b>' + ImpactTitleName(data.impact) + ' from ' + data.dis + '</b><br>' + layer.feature.properties.Commune + ' : ' + layer.feature.properties.value).openPopup();
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
        MYA_MapData.fitBounds(e.target.getBounds());
    }


    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: zoomToFeature
        });
    }

    geojson = L.geoJson(MYA_map, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(MYA_MapData);

    // Add SDC Project location
    var MYA_marker = MYA_createMarker(arr);
    MYA_marker.addTo(MYA_MapData);
}

//----------------------------------------------------------------------------------------------//
//-------------------------------------- HighChart Chart ---------------------------------------//
//----------------------------------------------------------------------------------------------// 
var KHM_local_Chart;
var KHM_year_Chart;

var LAO_local_Chart;
var LAO_year_Chart;
// Destroy previous date slider function
function destroyExistingChart(chart) {
    if (chart && chart) {
        chart.destroy();
    }
}
//------------* Cambodia Event Chart Function *------------//
function KHM_EventChart(khm_data) {
    destroyExistingChart(KHM_local_Chart);
    var l_labels = khm_data.level_code;
    var l_data = {
        labels: l_labels,
        datasets: [{
            label: ImpactTitleName(khm_data.impact) + ' cumulative',
            data: khm_data.level_value,
            backgroundColor: [
                '#0b2d5a'
            ],
            borderColor: [
                '#0b2d5a'
            ],
            borderWidth: 1
        }]
    };
    // Config
    var l_config = {
        type: 'bar',
        data: l_data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        },
    };
    // Render chart
    KHM_local_Chart = new Chart(
        document.getElementById('KHM_local_Chart'),
        l_config
    );
}
//------------* Cambodia Year Chart Function *------------//
function KHM_YearChart(khm_data) {
    destroyExistingChart(KHM_year_Chart);
    var y_labels = khm_data.list_year;
    var y_data = {
        labels: y_labels,
        datasets: [{
            label: ImpactTitleName(khm_data.impact) + ' cumulative',
            data: khm_data.list_impact,
            backgroundColor: [
                '#0b2d5a'
            ],
            borderColor: [
                '#0b2d5a'
            ],
            borderWidth: 1
        }]
    };
    // Config
    var y_config = {
        type: 'bar',
        data: y_data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        },
    };
    // Render chart
    KHM_year_Chart = new Chart(
        document.getElementById('KHM_year_Chart'),
        y_config
    );
}

//------------* Laos Event Chart Function *------------//
function LAO_EventChart(lao_data) {
    destroyExistingChart(LAO_local_Chart);
    var l_labels_lao = lao_data.level_code;
    var l_data_lao = {
        labels: l_labels_lao,
        datasets: [{
            label: ImpactTitleName(lao_data.impact) + ' cumulative',
            data: lao_data.level_value,
            backgroundColor: [
                '#0b2d5a'
            ],
            borderColor: [
                '#0b2d5a'
            ],
            borderWidth: 1
        }]
    };
    // Config
    var l_config_lao = {
        type: 'bar',
        data: l_data_lao,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        },
    };
    // Render chart
    LAO_local_Chart = new Chart(
        document.getElementById('LAO_local_Chart'),
        l_config_lao
    );
}
//------------* Laos Year Chart Function *------------//
function LAO_YearChart(lao_data) {
    destroyExistingChart(LAO_year_Chart);
    var y_labels = lao_data.list_year;
    var y_data = {
        labels: y_labels,
        datasets: [{
            label: ImpactTitleName(lao_data.impact) + ' cumulative',
            data: lao_data.list_impact,
            backgroundColor: [
                '#0b2d5a'
            ],
            borderColor: [
                '#0b2d5a'
            ],
            borderWidth: 1
        }]
    };
    // Config
    var y_config = {
        type: 'bar',
        data: y_data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        },
    };
    // Render chart
    LAO_year_Chart = new Chart(
        document.getElementById('LAO_year_Chart'),
        y_config
    );
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
    download(JSON.stringify(data.mapdata_out), "KHM_" + data.dis + "_" + Datalevel(data.level) + ".geojson", "text/plain");
}

function KHM_onDownload_TIFF(data) {
    //console.log(data.mapdata_out);
    download(JSON.stringify(data.mapdata_out), "KHM_" + data.dis + "_" + Datalevel(data.level) + ".tiff", "text/plain");
}

//--------* Laos *--------//
function LAO_onDownload_JSON(data) {
    //console.log(data.mapdata_out);
    download(JSON.stringify(data.mapdata_out), "LAO_" + data.dis + "_" + Datalevel(data.level) + ".geojson", "text/plain");
}

function LAO_onDownload_TIFF(data) {
    //console.log(data.mapdata_out);
    download(JSON.stringify(data.mapdata_out), "LAO_" + data.dis + "_" + Datalevel(data.level) + ".tiff", "text/plain");
}

//--------* Myanmar *--------//
function MYA_onDownload_JSON(data) {
    //console.log(data.mapdata_out);
    download(JSON.stringify(data.mapdata_out), "MYA_" + data.dis + "_" + Datalevel(data.level) + ".geojson", "text/plain");
}

function MYA_onDownload_TIFF(data) {
    //console.log(data.mapdata_out);
    download(JSON.stringify(data.mapdata_out), "MYA_" + data.dis + "_" + Datalevel(data.level) + ".tiff", "text/plain");
}

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

// --------------------------------------------------* Cambodia *-------------------------------------------------------------//

function KHMdownloadChartasJPEG() {
    document.getElementById("khm_download_jpg").addEventListener("click", function () {
        html2canvas(document.getElementById("cambodia_map_container"), { allowTaint: true, useCORS: true }).then(function (canvas) {
            //console.log(canvas);
            simulateDownloadImageClick(canvas.toDataURL(), 'KHM_' + khm_dis_sel + '_' + khm_impact_sel + '_' + Datalevel(khm_lev_sel) + '.jpg');
        });
    });
}

// --------------------------------------------------* Laos *-------------------------------------------------------------//

function LAOdownloadChartasJPEG() {
    document.getElementById("lao_download_jpg").addEventListener("click", function () {
        html2canvas(document.getElementById("laos_map_container"), { allowTaint: true, useCORS: true }).then(function (canvas) {
            //console.log(canvas);
            simulateDownloadImageClick(canvas.toDataURL(), 'LAO_' + lao_dis_sel + '_' + lao_impact_sel + '_' + Datalevel(lao_lev_sel) + '.jpg');
        });
    });
}

// --------------------------------------------------* Myanmar *-------------------------------------------------------------//

function MYAdownloadChartasJPEG() {
    document.getElementById("mya_download_jpg").addEventListener("click", function () {
        html2canvas(document.getElementById("maynmar_map_container"), { allowTaint: true, useCORS: true }).then(function (canvas) {
            //console.log(canvas);
            simulateDownloadImageClick(canvas.toDataURL(), 'MYA_' + mya_dis_sel + '_' + mya_impact_sel + '_' + Datalevel(mya_lev_sel) + '.jpg');
        });
    });
}