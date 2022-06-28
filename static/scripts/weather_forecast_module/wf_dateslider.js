//---------------------------------------* Global function for date slider *----------------------------------------//
// Destroy previous date slider function
function destroyExistingSlider(slider) {
    if (slider && slider.noUiSlider) {
        slider.noUiSlider.destroy();
    }
}

// Get Time in milli sec
function timestamp(str) {
    return new Date(str).getTime();
}
// Format date to show in tooltips and pips
function formatDate_view(date) {
    return date.getDate() + " " +
        months[date.getMonth()] + " " +
        date.getFullYear();
}

function toFormat_view(v) {
    return formatDate_view(new Date(v));
}

// Format date for sending to backend 
function formatDate_back(date) {
    return date.getFullYear() + "-" +
        months_num[date.getMonth()] + "-" +
        date.getDate();
}

function toFormat_back(v) {
    return formatDate_back(new Date(v));
}

// set today date
var TodayDate = new Date();
// Set month
var months_num = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'];
var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

var KHM_DateSlider;
var LAO_DateSlider;
var MYA_DateSlider;
//-----------------------------------------------------------------------------------------------------//
//--------------------------------------------- Cambodia ----------------------------------------------//
//---------------------------------------------------------------------------------------------------//

//---------------* Cambodia Date Slider *----------------//
$(document).ready(function () {
    var khm_date_selected;

    KHM_DateSlider = document.getElementById('khm_date_slider');

    noUiSlider.create(KHM_DateSlider, {
        behaviour: 'tap',
        connect: [true, false],
        tooltips: { to: toFormat_view, from: Number },
        //format: { to: toFormat, from: Number },
        range: {
            min: timestamp(TodayDate),
            // max 10 days forecast
            max: timestamp(TodayDate) + (10 * 24 * 60 * 60 * 1000)
        },
        // Step 1 day
        step: 1 * 24 * 60 * 60 * 1000,
        start: [timestamp(TodayDate)],
        pips: {
            mode: 'positions',
            values: [0, 50, 100],
            format: {
                to: toFormat_view,
                from: Number
            }
        }
    });

    // retrieve start to end date value from slider
    KHM_DateSlider.noUiSlider.on('change', function (v, handle) {
        // remove digits
        khm_date_selected = Number(v[handle]);
        // Change data type to date the same as database
        khm_date_selected = toFormat_back(new Date(khm_date_selected));
        //console.log(khm_date_selected);

        // Add AJAX for selection
        KHMSubmitAJAX(khm_date_selected, khm_wf_param);
    });
});
//---------------------------------------------------------------------------------------------------------//
//------------------------------------------ Laos Date Slider --------------------------------------------//
//-------------------------------------------------------------------------------------------------------//
$(document).ready(function () {
    var lao_date_selected;

    LAO_DateSlider = document.getElementById('lao_date_slider');

    noUiSlider.create(LAO_DateSlider, {
        behaviour: 'tap',
        connect: [true, false],
        tooltips: { to: toFormat_view, from: Number },
        //format: { to: toFormat, from: Number },
        range: {
            min: timestamp(TodayDate),
            // max 10 days forecast
            max: timestamp(TodayDate) + (10 * 24 * 60 * 60 * 1000)
        },
        // Step 1 day
        step: 1 * 24 * 60 * 60 * 1000,
        start: [timestamp(TodayDate)],
        pips: {
            mode: 'positions',
            values: [0, 50, 100],
            format: {
                to: toFormat_view,
                from: Number
            }
        }
    });

    // retrieve start to end date value from slider
    LAO_DateSlider.noUiSlider.on('change', function (v, handle) {
        // remove digits
        lao_date_selected = Number(v[handle]);
        // Change data type to date the same as database
        lao_date_selected = toFormat_back(new Date(lao_date_selected));
        //console.log(khm_date_selected);

        // Add AJAX for selection
        LAOSubmitAJAX(lao_date_selected, lao_wf_param);
    });
});
//-----------------------------------------------------------------------------------------------------//
//--------------------------------------- Myanmar Date Slider ----------------------------------------//
//---------------------------------------------------------------------------------------------------//
$(document).ready(function () {
    MYA_DateSlider = document.getElementById('mya_date_slider');

    noUiSlider.create(MYA_DateSlider, {
        behaviour: 'tap',
        connect: [true, false],
        tooltips: { to: toFormat_view, from: Number },
        //format: { to: toFormat, from: Number },
        range: {
            min: timestamp(TodayDate),
            // max 10 days forecast
            max: timestamp(TodayDate) + (10 * 24 * 60 * 60 * 1000)
        },
        // Step 1 day
        step: 1 * 24 * 60 * 60 * 1000,
        start: [timestamp(TodayDate)],
        pips: {
            mode: 'positions',
            values: [0, 50, 100],
            format: {
                to: toFormat_view,
                from: Number
            }
        }
    });

});


