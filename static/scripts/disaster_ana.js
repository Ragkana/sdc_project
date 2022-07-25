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
//--------------------------------------------------------------------------------------// 
//--------------------------------------- Tab ------------------------------------------//
//--------------------------------------------------------------------------------------//
$(document).ready(function () {
    $("#myTab a").click(function (z) {
        z.preventDefault();
        $(this).tab("show");
    });
});

//--------------------------------------------------------------------------------------------//
//-------------------------------------- HighChart Map ---------------------------------------//
//--------------------------------------------------------------------------------------------// 
// ----* Default : Variable & Function *---- //
var KHM_MapData;
var LAO_MapData;

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

//------------* Cambodia map Function *------------//
function KHM_MapChart(khm_data) {
    KHM_MapData = khm_data.map_data;
    Highcharts.getJSON(level(khm_data.level), function (geojson) {

        // Initialize the chart
        Highcharts.mapChart('hc_map01_container', {
            chart: {
                map: geojson,
                //borderWidth: 2,
                backgroundColor: false
            },

            title: {
                text: ''
            },

            accessibility: {
                typeDescription: 'Map of Cambodia.'
            },

            mapNavigation: {
                enabled: true,
                buttonOptions: {
                    verticalAlign: 'bottom'
                }
            },

            colorAxis: {
                minColor: '#EEEEFF',
                maxColor: '#000022',
                stops: [
                    [0, '#DAEAF7'],
                    [0.2, '#4FA5D8'],
                    [0.4, '#0754B0'],
                    [0.6, '#010E54'],
                    [0.8, '#00022B']
                ]
            },

            series: [{
                data: KHM_MapData,
                keys: ['code', 'value'],
                joinBy: [Datalevel(khm_data.level), 'code'],
                name: khm_data.dis,
                tooltip: {
                    pointFormat: '{point.code}: {point.value}'
                },
                states: {
                    hover: {
                        color: '#F7E8CE'
                    }
                },
                dataLabels: {
                    enabled: true,
                    format: '{point.code}'
                }
            }]
        });
    });
}

//------------* Laos map Function *------------//

// choose which map level will show on site by dropdown selection.
function Twolevel(lev) {
    if (lev == 'district_name') {
        return laoMap_d;
    }
    else {
        return laoMap_p;
    }
}

function TwoDatalevel(dlev) {
    if (dlev == 'district_name') {
        return 'District';
    }
    if (dlev == 'province_name') {
        return 'Province';
    }
}


function LAO_MapChart(lao_data) {
    LAO_MapData = lao_data.map_data;
    Highcharts.getJSON(Twolevel(lao_data.level), function (geojson) {

        // Initialize the chart
        Highcharts.mapChart('hc_map02_container', {
            chart: {
                map: geojson,
                //borderWidth: 2,
                backgroundColor: false
            },

            title: {
                text: ''
            },

            accessibility: {
                typeDescription: 'Map of Laos.'
            },

            mapNavigation: {
                enabled: true,
                buttonOptions: {
                    verticalAlign: 'bottom'
                }
            },

            colorAxis: {
                minColor: '#EEEEFF',
                maxColor: '#000022',
                stops: [
                    [0, '#DAEAF7'],
                    [0.2, '#4FA5D8'],
                    [0.4, '#0754B0'],
                    [0.6, '#010E54'],
                    [0.8, '#00022B']
                ]
            },

            series: [{
                data: LAO_MapData,
                keys: ['code', 'value'],
                joinBy: [TwoDatalevel(lao_data.level), 'code'],
                name: lao_data.dis,
                tooltip: {
                    pointFormat: '{point.code}: {point.value}'
                },
                states: {
                    hover: {
                        color: '#F7E8CE'
                    }
                },
                dataLabels: {
                    enabled: true,
                    format: '{point.code}'
                }
            }]
        });
    });
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
function KMH_EventChart(khm_data) {
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

