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

const locationIcon = new L.icon({
    iconUrl: '/static/images/tower.png',

    iconSize: [34, 34], // size of the icon
    // remember that iconAnchor must always relate to iconSize by [x=x/2,y=y]
    iconAnchor: [17, 34], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -25] // point from which the popup should open relative to the iconAnchor
});

const LAO_locationIcon = new L.icon({
    iconUrl: '/static/images/tower.png',

    iconSize: [30, 30], // size of the icon
    // remember that iconAnchor must always relate to iconSize by [x=x/2,y=y]
    iconAnchor: [15, 30], // point of the icon which will correspond to marker's location
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

    // --- Add Station marker and AJAX on click --- //
    L.marker([13.0957, 103.2022], { icon: locationIcon }).addTo(cam_map).bindTooltip("Battambang Station").bindPopup("Battambang Station").openPopup().on('click', function () {
        KHM_ajaxStation('Battambang');
    });
    L.marker([11.4650, 104.5073], { icon: locationIcon }).addTo(cam_map).bindTooltip("Kampong Speu Station").bindPopup("Kampong Speu Station").on('click', function () {
        KHM_ajaxStation('Kampong Speu');
    });
    L.marker([12.8222, 105.1259], { icon: locationIcon }).addTo(cam_map).bindTooltip("Kampong Thom Station").bindPopup("Kampong Thom Station").on('click', function () {
        KHM_ajaxStation('Kampong Thom');
    });
    L.marker([10.5942, 104.1640], { icon: locationIcon }).addTo(cam_map).bindTooltip("Kampot Station").bindPopup("Kampot Station").on('click', function () {
        KHM_ajaxStation('Kampot');
    });
    L.marker([11.5564, 104.9282], { icon: locationIcon }).addTo(cam_map).bindTooltip("Phnom Penh Station").bindPopup("Phnom Penh Station").on('click', function () {
        KHM_ajaxStation('Phnom Penh');
    });
    L.marker([10.6268, 103.5116], { icon: locationIcon }).addTo(cam_map).bindTooltip("Preah Sihanouk Station").bindPopup("Preah Sihanouk Station").on('click', function () {
        KHM_ajaxStation('Preah Sihanouk');
    });
    L.marker([12.4652, 103.8912], { icon: locationIcon }).addTo(cam_map).bindTooltip("Pursat Station").bindPopup("Pursat Station").on('click', function () {
        KHM_ajaxStation('Pursat');
    });
    L.marker([13.5069, 105.9677], { icon: locationIcon }).addTo(cam_map).bindTooltip("Stung Treng Station").bindPopup("Stung Treng Station").on('click', function () {
        KHM_ajaxStation('Stung Treng');
    });
    L.marker([13.3633, 103.8564], { icon: locationIcon }).addTo(cam_map).bindTooltip("Siem Reap Station").bindPopup("Siem Reap Station").on('click', function () {
        KHM_ajaxStation('Siem Reap');
    });


    // Add Zoom button
    L.control.zoom({
        position: 'topleft'
    }).addTo(cam_map);

  
    L.geoJson(json, {
        style: style
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

    // --- Add Station marker and AJAX on click --- //
    L.marker([14.8194, 106.8208], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Attapeu Station").bindPopup("Attapeu Station").on('click', function () {
        LAO_ajaxStation('Attapeu');
    });
    L.marker([20.2873, 100.7098], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Bokeo Station").bindPopup("Bokeo Station").on('click', function () {
        LAO_ajaxStation('Bokeo');
    });
    L.marker([20.9709, 101.4112], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Luangnamtha Station").bindPopup("Luangnamtha Station").on('click', function () {
        LAO_ajaxStation('Luangnamtha');
    });
    L.marker([19.8833, 102.1387], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Luang Prabang Station").bindPopup("Luang Prabang Station").on('click', function () {
        LAO_ajaxStation('Luang Prabang');
    });
    L.marker([20.4922, 101.8892], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Oudomxay Station").bindPopup("Oudomxay Station").on('click', function () {
        LAO_ajaxStation('Oudomxay');
    });
    L.marker([18.3983, 103.6652], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Paksanh Station").bindPopup("Paksanh Station").on('click', function () {
        LAO_ajaxStation('Paksanh');
    });
    L.marker([15.1172, 105.8159], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Pakse Station").bindPopup("Pakse Station").on('click', function () {
        LAO_ajaxStation('Pakse');
    });
    L.marker([21.6819, 102.1090], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Phongsaly Station").bindPopup("Phongsaly Station").on('click', function () {
        LAO_ajaxStation('Phongsaly');
    });
    L.marker([18.5054, 102.4180], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Phonehong Station").bindPopup("Phonehong Station").on('click', function () {
        LAO_ajaxStation('Phonehong');
    });
    L.marker([15.7166, 106.4141], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Saravane Station").bindPopup("Saravane Station").on('click', function () {
        LAO_ajaxStation('Saravane');
    });
    L.marker([16.5721, 104.7687], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Savannakhet Station").bindPopup("Savannakhet Station").on('click', function () {
        LAO_ajaxStation('Savannakhet');
    });
    L.marker([19.3908, 101.5248], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Sayabouly Station").bindPopup("Sayabouly Station").on('click', function () {
        LAO_ajaxStation('Sayabouly');
    });
    L.marker([18.9181, 102.9896], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Saysomboun Station").bindPopup("Saysomboun Station").on('click', function () {
        LAO_ajaxStation('Saysomboun');
    });
    L.marker([15.3444, 106.7176], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Sekong Station").bindPopup("Sekong Station").on('click', function () {
        LAO_ajaxStation('Sekong');
    });
    L.marker([17.9757, 102.6331], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Vientiane Station").openTooltip().bindPopup("Vientiane Station").on('click', function () {
        LAO_ajaxStation('Vientiane');
    });
    L.marker([20.4171, 104.0479], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Xam Neua Station").bindPopup("Xam Neua Station").on('click', function () {
        LAO_ajaxStation('Xam Neua');
    });
    L.marker([19.6375, 103.3587], { icon: LAO_locationIcon }).addTo(lao_map).bindTooltip("Xiangkhouang Station").bindPopup("Xiangkhouang Station").on('click', function () {
        LAO_ajaxStation('Xiangkhouang');
    });

    // Add Zoom button
    L.control.zoom({
        position: 'topleft'
    }).addTo(lao_map);


    L.geoJson(json, {
        style: style
    }).addTo(lao_map);

}

// --------------** Myanmar Map **--------------//


//------------------------------------------------------------------------------------------------------------//
//--------------------------------------------- Time series Chart --------------------------------------------//
//-----------------------------------------------------------------------------------------------------------//

var KHM_Chart;
var LAO_Chart;

// Setup Block
var month_labels = [
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

// Destroy previous date slider function
function destroyExistingChart(chart) {
    if (chart && chart) {
        chart.destroy();
    }
}


// ------------------------** Cambodia Chart **------------------------//

function KHM_tsChart(khm_data) {
    destroyExistingChart(KHM_Chart);
    var ctx = document.getElementById('khm_chart');

    var wfdata = {
        labels: month_labels,
        datasets: [{
            label: 'Min Temp',
            backgroundColor: '#0b2d5a',
            borderColor: '#0b2d5a',
            data: khm_data.min_temp,
            yAxisID: 'y'
        },
        {
            label: 'Max Temp',
            backgroundColor: '#9B0103',
            borderColor: '#9B0103',
            data: khm_data.max_temp,
            yAxisID: 'y'
        }, {
            label: 'Rainfall',
            type: 'bar',
            backgroundColor: '#2f96b2',
            borderColor: '#2f96b2',
            data: khm_data.rainfall,
            yAxisID: 'y1',
        }
        ]
    };

    // Rander Chart
    KHM_Chart = new Chart(ctx, {
        display: true,
        type: 'line',
        data: wfdata,
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            stacked: false,
            plugins: {
                title: {
                    display: true,
                    //text: 'Chart.js Line Chart - Multi Axis'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    display: true,
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    },
                    type: 'linear',
                    labels: 'Temperature',
                    position: 'left'
                },
                y1: {
                    beginAtZero: true,
                    display: true,
                    title: {
                        display: true,
                        text: 'Rainfall (mm)'
                    },
                    type: 'linear',
                    labels: 'Rainfall',
                    position: 'right',
                }

            },
        }

    });

}
// ------------------------** Laos Chart **------------------------//
function LAO_tsChart(lao_data) {
    destroyExistingChart(LAO_Chart);
    var ctx = document.getElementById('lao_chart');

    var wfdata = {
        labels: month_labels,
        datasets: [{
            label: 'Min Temp',
            backgroundColor: '#0b2d5a',
            borderColor: '#0b2d5a',
            data: lao_data.min_temp,
            yAxisID: 'y'
        },
        {
            label: 'Max Temp',
            backgroundColor: '#9B0103',
            borderColor: '#9B0103',
            data: lao_data.max_temp,
            yAxisID: 'y'
        }, {
            label: 'Rainfall',
            type: 'bar',
            backgroundColor: '#2f96b2',
            borderColor: '#2f96b2',
            data: lao_data.rainfall,
            yAxisID: 'y1',
        }
        ]
    };

    // Rander Chart
    LAO_Chart = new Chart(ctx, {
        display: true,
        type: 'line',
        data: wfdata,
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            stacked: false,
            plugins: {
                title: {
                    display: true,
                    //text: 'Chart.js Line Chart - Multi Axis'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    display: true,
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    },
                    type: 'linear',
                    labels: 'Temperature',
                    position: 'left'
                },
                y1: {
                    beginAtZero: true,
                    display: true,
                    title: {
                        display: true,
                        text: 'Rainfall (mm)'
                    },
                    type: 'linear',
                    labels: 'Rainfall',
                    position: 'right',
                }

            },
        }

    });
}

// ------------------------** Myanmar Chart **------------------------//

//------------------------------------------------------------------------------------------------------------//
//--------------------------------------------- Year Range Slider --------------------------------------------//
//------------------------------------------------------------------------------------------------------------//
// Default
var KHM_YearSlider;
var khm_y_start;
var khm_y_end;

var LAO_YearSlider;
var lao_y_start;
var lao_y_end;
// Destroy previous date slider function
function destroyExistingSlider(slider) {
    if (slider && slider.noUiSlider) {
        slider.noUiSlider.destroy();
    }
}
// ------------------------** Cambodia year slider **------------------------//
function KHM_YearSelect(khm_data) {
    destroyExistingSlider(KHM_YearSlider);
    KHM_YearSlider = document.getElementById('khm_year_slider');

    noUiSlider.create(KHM_YearSlider, {
        start: [khm_data.year_start, khm_data.year_end],
        tooltips: [true, true],
        connect: true,
        behaviour: 'tap',
        //step: 10,
        range: {
            'min': khm_data.year_start,
            'max': khm_data.year_end
        },
        format: wNumb({
            decimals: 0
        }),
        pips: {
            mode: 'positions',
            values: [0, 25, 50, 75, 100],
            density: 3
        }
    });

    // retrieve start to end year value from slider
    $(KHM_YearSlider)[0].noUiSlider.on('change', function (v, handle) {
        khm_y_start = v[0];
        khm_y_end = v[1];
        //alert(khm_y_start + ' + ' + khm_y_end);
        // Use secound AJAX to send start and end year back to views.py
        KHM_ajaxYearSel(khm_y_start, khm_y_end, khm_data.station);
    });

}

// ------------------------** Laos year slider **------------------------//
function LAO_YearSelect(lao_data) {
    destroyExistingSlider(LAO_YearSlider);
    LAO_YearSlider = document.getElementById('lao_year_slider');

    noUiSlider.create(LAO_YearSlider, {
        start: [lao_data.year_start, lao_data.year_end],
        tooltips: [true, true],
        connect: true,
        behaviour: 'tap',
        //step: 10,
        range: {
            'min': lao_data.year_start,
            'max': lao_data.year_end
        },
        format: wNumb({
            decimals: 0
        }),
        pips: {
            mode: 'positions',
            values: [0, 25, 50, 75, 100],
            density: 3
        }
    });

    // retrieve start to end year value from slider
    $(LAO_YearSlider)[0].noUiSlider.on('change', function (v, handle) {
        lao_y_start = v[0];
        lao_y_end = v[1];
        //alert(lao_y_start + ' + ' + lao_y_end);
        // Use secound AJAX to send start and end year back to views.py
        LAO_ajaxYearSel(lao_y_start, lao_y_end, lao_data.station);
    });

}
// ------------------------** Myanmar year slider **------------------------//