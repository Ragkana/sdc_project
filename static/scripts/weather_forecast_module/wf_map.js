//------------* Global function for map *------------//
// Assigning color for selected parameter class
function getColor(param) {
    return param > 90 ? '#062655' :
        param > 80 ? '#08306B' :
            param > 70 ? '#08519C' :
                param > 60 ? '#2171B5' :
                    param > 40 ? '#4292C6' :
                        param > 30 ? '#6BAED6' :
                            param > 20 ? '#9ECAE1' :
                                param > 10 ? '#C6DBEF' :
                                    param > 5 ? '#DEEBF7' :
                                        '#F7FBFF';
}

// Destroy the old map and create the new one.
function destroyExistingMap(map) {
    if (map != undefined || map != null) {
        map.remove();
    }
}

//-----------------------------------------------------------------------------------------------------//
//--------------------------------------- Cambodia leaflet Map ----------------------------------------//
//----------------------------------------------------------------------------------------------------//

//------------* Cambodia map Function *------------//
var cam_map;

function KHM_MapChart(data) {
    var wfparam = data.wf_param;
    destroyExistingMap(cam_map);
    cam_map = L.map('cam_map', {
        zoomControl: false,
        minZoom: 3,     // Max Zoom out
        maxZoom: 9,    // Max Zoom in
    }).setView([12.562108, 104.888535], 7);
    //L.tileLayer('https://api.mapbox.com/styles/v1/nazmul-rimes/ck9wljpn30kbx1is5a630hmtb/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibmF6bXVsLXJpbWVzIiwiYSI6ImNrOWFzeHNtcDA3MjAzbG50dnB0YmkxNnAifQ.usNB6Kf9PyFtKTUF1XI38g').addTo(cam_map);
    L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png').addTo(cam_map);

    function style(feature) {
        return {
            fillColor: getColor(feature.properties[wfparam]),
            weight: 2,
            opacity: 1,
            color: '#2F96B2',
            dashArray: '3',
            fillOpacity: 0.7
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
            color: '#2F96B2',
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


    // Add legend to map
    var legend = L.control({ position: 'bottomright' });
    legend.onAdd = function (cam_map) {

        var div = L.DomUtil.create('div', 'info legend'),
            grades = [0, 5, 10, 20, 30, 40, 60, 70, 80, 90];

        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML += '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' + grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
        }
        return div;
    };

    legend.addTo(cam_map);

}

//--------------------------------------------------------------------------------------------------//
//--------------------------------------- Laos leaflet Map ----------------------------------------//
//-------------------------------------------------------------------------------------------------//
var lao_map;

function LAO_MapChart(data) {
    var wfparam = data.wf_param;
    destroyExistingMap(lao_map);
    lao_map = L.map('lao_map', {
        zoomControl: false,
        minZoom: 3,     // Max Zoom out
        maxZoom: 9,    // Max Zoom in
    }).setView([17.6384, 105.2195], 6);
    L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png').addTo(lao_map);

    function style(feature) {
        return {
            fillColor: getColor(feature.properties[wfparam]),
            weight: 2,
            opacity: 1,
            color: '#2F96B2',
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
            color: '#2F96B2',
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


    // Add legend to map
    var legend = L.control({ position: 'bottomright' });
    legend.onAdd = function (lao_map) {

        var div = L.DomUtil.create('div', 'info legend'),
            grades = [0, 5, 10, 20, 30, 40, 60, 70, 80, 90];

        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML += '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' + grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
        }
        return div;
    };

    legend.addTo(lao_map);

}


//-----------------------------------------------------------------------------------------------------//
//--------------------------------------- Myanmar leaflet Map ----------------------------------------//
//----------------------------------------------------------------------------------------------------//
var mya_map = L.map('mya_map', {
    zoomControl: false,
    minZoom: 3,     // Max Zoom out
    maxZoom: 9,    // Max Zoom in
}).setView([20.00, 95.00], 5);
L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png').addTo(mya_map);

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