//----------------------------------------------------------------------------------------------//
//--------------------------------------------- Tab --------------------------------------------//
//----------------------------------------------------------------------------------------------//
$(document).ready(function () {
    $("#myTab a").click(function (e) {
        e.preventDefault();
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
//--------------------------------------------- Map --------------------------------------------//
//----------------------------------------------------------------------------------------------//
var cam_map;
var lao_map;

/*function getColor(param) {
    if (param.Province == station) {
        return '#2F96B2';
    } else {
        return '#C4C7D7';
    }
}*/
function getColor(param) {
    return '#C4C7D7';

}

// GeoJSON style
function style(feature) {
    return {
        weight: 2,
        opacity: 1,
        color: '#2F96B2',
        //fillColor: '#C4C7D7',
        fillColor: getColor(feature.properties),
        dashArray: '4',
        fillOpacity: 0.7
    };
}

var locationIcon = new L.icon({
    iconUrl: '/static/images/location.png',

    iconSize: [34, 34], // size of the icon
    // remember that iconAnchor must always relate to iconSize by [x=x/2,y=y]
    iconAnchor: [17, 34], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -20] // point from which the popup should open relative to the iconAnchor
});

// --------------** Cambodia Map **--------------//
function KHM_map(json) {
    cam_map = L.map('cam_map', {
        zoomControl: false,
        minZoom: 3,     // Max Zoom out
        maxZoom: 9,    // Max Zoom in
    }).setView([12.562108, 104.888535], 7);
    //L.tileLayer('https://api.mapbox.com/styles/v1/nazmul-rimes/ck9wljpn30kbx1is5a630hmtb/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibmF6bXVsLXJpbWVzIiwiYSI6ImNrOWFzeHNtcDA3MjAzbG50dnB0YmkxNnAifQ.usNB6Kf9PyFtKTUF1XI38g').addTo(cam_map);
    L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png').addTo(cam_map);

    // Add Zoom button
    L.control.zoom({
        position: 'topleft'
    }).addTo(cam_map);

    // Add interaction
    function highlightFeature(e) {
        var khm_layer = e.target;
        khm_layer.setStyle({
            weight: 5,
            color: '#2F96B2',
            //fillColor: '#2F96B2',
            dashArray: '',
            fillOpacity: 0.7
        });

        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            khm_layer.bringToFront();
        }
        // Add Info popup when mouseover
        khm_layer.bindPopup(khm_layer.feature.properties.Province).openPopup();
    }

    function resetHighlight(e) {
        khm_geojson.resetStyle(e.target);
    }

    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight
        });
    }

    var khm_geojson = L.geoJson(json, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(cam_map);
}

// --------------** Laos Map **--------------//

function LAO_map(json) {
    lao_map = L.map('lao_map', {
        zoomControl: false,
        minZoom: 3,     // Max Zoom out
        maxZoom: 9,    // Max Zoom in
    }).setView([17.6384, 105.2195], 6);
    L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png').addTo(lao_map);

    L.marker([14.8194, 106.8208], { icon: locationIcon }).addTo(lao_map).bindPopup("Test icon");

    L.geoJson(json, {
        style: style
    }).addTo(lao_map);

}

// --------------** Myanmar Map **--------------//


//------------------------------------------------------------------------------------------------------------//
//--------------------------------------------- Time series Chart --------------------------------------------//
//-----------------------------------------------------------------------------------------------------------//
// Setup Block
var labels = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
];

// Destroy the old chart and create the new one.
function destroyExistingChart(chart) {
    if (chart != undefined || chart != null) {
        chart.destroy();
    }
}

// ------------------------** Cambodia Chart **------------------------//

function KHM_ts(khm_data) {
    //destroyExistingChart(KHM_Chart);
    var ctx = document.getElementById('khm_chart').getContext('2d');
    // Rander Chart
    var KHM_Chart = new Chart(ctx,khm_chart_config);

    var wfdata = {
        labels: labels,
        datasets: [{
            label: 'Min Temp',
            backgroundColor: '#2f96b2',
            borderColor: '#2f96b2',
            data: [khm_data.min_temp],
            yAxisID: 'A'
        },
        {
            label: 'Max Temp',
            backgroundColor: '#0b2d5a',
            borderColor: '#0b2d5a',
            data: [khm_data.max_temp],
            yAxisID: 'A'
        }, {
            label: 'Rainfall',
            backgroundColor: '#c4c7d7',
            borderColor: '#c4c7d7',
            data: [khm_data.rainfall],
            yAxisID: 'B'
        }
        ]
    };

    // Config Block
    var khm_chart_config = {
        display: true,
        type: 'line',
        data: wfdata,
        options: {
            scales: {
                'A': {
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    },
                    labels: 'Temperature',
                    position: 'left'
                },
                'B': {
                    title: {
                        display: true,
                        text: 'Rainfall (mm)'
                    },
                    labels: 'Rainfall',
                    position: 'right',
                }
            }
        }
    };

}
// ------------------------** Laos Chart **------------------------//

// ------------------------** Myanmar Chart **------------------------//
