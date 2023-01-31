//------------------------------------------------------------------------------------------------------//
//--------------------------------------- Addition leaflet Map ----------------------------------------//
//-----------------------------------------------------------------------------------------------------//
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

//-----------------------------------------------------------------------------------------------------//
//--------------------------------------- Province leaflet Map ----------------------------------------//
//----------------------------------------------------------------------------------------------------//
var prov_map;
function Province_MapChart(data) {
    prov_map = L.map('h_province_map', {
        zoomControl: false,
        minZoom: 3,     // Max Zoom out
        maxZoom: 12,    // Max Zoom in
        attributionControl: false, // Remove leaflet logo
        scrollWheelZoom: false, // You can't get the correct screenshot If allow to use scroll.
        preferCanvas: true
    }).setView([12.562108, 104.888535], 7);
    L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
    }).addTo(prov_map);

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

    // Retrieve Map data
    var data_map = data.map_data

    geojson = L.geoJson(data_map, {
        style: style
    }).addTo(prov_map);
}

