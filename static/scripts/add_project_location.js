//-------------------------------------------------------------------------------------------------------------------//
//--------------------------------------- Addition function for location Map ----------------------------------------//
//-------------------------------------------------------------------------------------------------------------------//
/* ----- Destroy the old map and create the new one -----*/
function destroyExistingMap(map) {
    if (map != undefined || map != null) {
        map.remove();
    }
}

/* ----- variable for country location -----*/
const KHM_locset = [12.562108, 104.888535],
    LAO_locset = [17.6384, 105.2195],
    MYA_locset = [21.9162, 95.9560];

/* ----- Country location change after select -----*/
function countryLocation(cvar) {
    if (cvar == 'KHM') {
        return KHM_locset;
    }
    if (cvar == 'LAO') {
        return LAO_locset;
    }
    if (cvar == 'MYA') {
        return MYA_locset;
    }
}

function countryMapZoom(cvar) {
    if (cvar == 'KHM') {
        return 7;
    }
    if (cvar == 'LAO') {
        return 6;
    }
    if (cvar == 'MYA') {
        return 6;
    }
}
//------------------------------------------------------------------------------------------------// 
//---------------------------------- Location Map Function ---------------------------------------//
//------------------------------------------------------------------------------------------------//
var loc_map;

/* ----- Location marker icon -----*/
const loc_marker = new L.icon({
    iconUrl: '/static/images/location.png',
    iconSize: [40, 40] // size of the icon
});

function locationMap(cvar) {
    destroyExistingMap(loc_map);
    var latSpan = $('#lat'),
        longSpan = $('#long');
        
    loc_map = L.map('location_map', {
        zoomControl: false,
        minZoom: 3,     // Max Zoom out
        maxZoom: 12,    // Max Zoom in
        attributionControl: false, // Remove leaflet logo
        scrollWheelZoom: true, // You can't get the correct screenshot If allow to use scroll.
        preferCanvas: true
    }).setView(countryLocation(cvar), countryMapZoom(cvar));
    //L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(loc_map);
    L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png').addTo(loc_map);

    var marker = L.marker(countryLocation(cvar), { icon: loc_marker }).addTo(loc_map);

    loc_map.on('click', function (e) {
        longSpan.text(e.latlng.lng);
        latSpan.text(e.latlng.lat);
        document.getElementById('longitude').value= e.latlng.lng;
        document.getElementById('latitude').value= e.latlng.lat;
        marker.setLatLng(e.latlng);
    });

    // Change location on map after type latitude
    $(document).on('change', '[name=latitude]', function() {
        var lat_input = $('[name=latitude]').val();
        var lon_input = $('[name=longitude]').val();
        marker.setLatLng([lat_input,lon_input]);
    });

    // Change location on map after type longitude
    $(document).on('change', '[name=longitude]', function() {
        var lat_input = $('[name=latitude]').val();
        var lon_input = $('[name=longitude]').val();
        marker.setLatLng([lat_input,lon_input]);
    });
}

//------------------------------------------------------------------------------------------------------------------------//
//--------------------------------------------- Detail Font Limiter function  --------------------------------------------//
//------------------------------------------------------------------------------------------------------------------------//
function DetailFontLimiter() {
    $('#detail').keyup(function () {
      var detail_characterCount = $('#detail').val().length;
        $('#detail_current').text(detail_characterCount);
    });
    }

//----------------------------------------------------------------------------------------------------------------------------//
//--------------------------------------------- Append project dropdown function  --------------------------------------------//
//----------------------------------------------------------------------------------------------------------------------------//
function DropdownAjax(html_id, list) {
    $(html_id).find('option').remove();
    $.each(list, function (key, value) {
        $(html_id).append('<option value="' + value + '" data-tokens="' + value + '">' + value + '</option>');
        //$('<option>').val(value).text(value).appendTo($('#province_selected'));
    });
}


