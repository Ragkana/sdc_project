$(document).ready(function() {
 
   
    const MINZZOOM = 3;     // Max Zoom out
    const MAXZOOM = 9;    // Max Zoom in
    const ZOOMLEVEL = 5;
    const ZOOMCTRL = false;
    const SLAT = 11.562108;   //Default to Location
    const SLONG = 104.888535;               
    const MYCENTER = [SLAT, SLONG]; 
    const EQ_COUNT = settings.fields.number_events;
    // console.log(settings.fields.points1);
    const AOR_POLY1 = [[[102.193619,12.43423],[102.083683,13.974383],[102.413492,15.165258],[103.292984,15.927327],[104.632687,16.454854],[105.90795,16.539127],
        [106.985328,16.222916],[107.513023,15.694773],[108.150846,14.251406],[108.304757,12.541494],[108.106871,11.402293],[105.864166,10.517856],[103.929283,9.890731],
        [102.368024,10.712225],[102.193619,12.43423]]]
    const AOR_POLY2 = [[[100.65212,21.787875],[101.267765,21.910241],[101.421676,22.90559],[102.500519,23.107839],[103.797872,21.644983],[105.029161,21.379237],
        [105.952686,19.733421],[106.722242,17.986897],[107.976642,15.85105],[107.976642,14.366178],[106.965226,13.299425],[105.602013,13.299425],[104.018928,13.982712],
        [104.546623,15.131125],[103.799054,16.863034],[101.952121,17.199178],[100.676857,16.863034],[100.193137,18.245655],[98.562707,19.865539],[100.65212,21.787875]]]
    const AOR_POLY3 = [[[98.786447,18.036851],[97.159387,15.977833],[95.268479,15.131125],[92.937824,15.935581],[93.46552,17.785959],[92.058332,19.410259],[91.266789,21.141509],
        [91.531633,23.418518],[93.774338,25.933965],[94.917766,27.504008],[96.896623,28.628528],[99.535099,29.013545],[99.667023,25.101145],[100.060656,23.499144],
        [101.028098,22.569],[102.127463,20.607721],[98.917316,19.036805],[98.786447,18.036851]]]

    const POLY1 = turf.polygon(AOR_POLY1);
    const POLY2 = turf.polygon(AOR_POLY2);
    const POLY3 = turf.polygon(AOR_POLY3);

    const AOI1 = [{
        "type": "Feature",
        "geometry": {
           "type": "Polygon",
           "coordinates": AOR_POLY1
        }
     }];
  
     const L_AOI1 = new L.GeoJSON(AOI1,
        {
           fillColor: '#3dbf34',
           color: '#3dbf34',
           opacity :1,
           fillOpacity: 0.4,
           weight:2
        }
     )
     const AOI2 = [{
        "type": "Feature",
        "geometry": {
           "type": "Polygon",
           "coordinates": AOR_POLY2
        }
     }];
  
     const L_AOI2 = new L.GeoJSON(AOI2,
        {
           fillColor: '#3dbf34',
           color: '#3dbf34',
           opacity :1,
           fillOpacity: 0.4,
           weight:2
        }
     )
     const AOI3 = [{
        "type": "Feature",
        "geometry": {
           "type": "Polygon",
           "coordinates": AOR_POLY3
        }
     }];
  
     const L_AOI3 = new L.GeoJSON(AOI3,
        {
           fillColor: '#3dbf34',
           color: '#3dbf34',
           opacity :1,
           fillOpacity: 0.4,
           weight:2
        }
     )
    const MSG = {
            SEND : {
                type : 'info',
                msg : '<i class="fa-solid fa-paper-plane pr-2"></i>Sending advisory for earthquake <b><u>_REGION_ | _MAG_</b></u. '
            },
            SUCCESS : {
                type : 'success',
                msg : '<i class="fa-solid fa-house-crack"></i> Earthquake Advisory in <b><u>_REGION_</b></u> with magnitude of <b><u>_MAG_</u></b> successfully sent.'
            }, 
            ERROR : {
                type : 'error',
                msg : '<i class="fa-solid fa-circle-exclamation"></i> Error encountered. Please contact web admin.'
            }, 
            EARTHQUAKE : {
                type : 'error',
                msg : '<i class="fa-solid fa-house-crack"></i> _UPDATE_ earthquake is detectd in <b><u>_REGION_</b></u> with magnitude of <b><u>_MAG_</u></b>'
            } 
    } 


    //**** Base maps
    const URLTILEMAP_WHITE = "https://api.mapbox.com/styles/v1/nazmul-rimes/ck9wljpn30kbx1is5a630hmtb/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibmF6bXVsLXJpbWVzIiwiYSI6ImNrOWFzeHNtcDA3MjAzbG50dnB0YmkxNnAifQ.usNB6Kf9PyFtKTUF1XI38g",
        URLTILEMAP_BLACK = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        URLTILEMAP_SATELLITE = "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        URLTILEMAP_OSM = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

    const MWHITE  = L.tileLayer(URLTILEMAP_WHITE, {
        maxZoom: MAXZOOM,
            minZoom: MINZZOOM,
    }), 
    MSATELLITE = L.tileLayer(URLTILEMAP_SATELLITE, {
        maxZoom: MAXZOOM,
        minZoom: MINZZOOM,
    }),
    MOSM =  L.tileLayer(URLTILEMAP_OSM, {
        maxZoom: MAXZOOM,
        minZoom: MINZZOOM,
    }),
    MBLACK =  L.tileLayer(URLTILEMAP_BLACK, {
        maxZoom: MAXZOOM,
             minZoom: MINZZOOM,
    });
    
    let cbasemap = MWHITE // Current basemap

    //**** Initialize Map
    map = L.map('cam_map', {
        attributionControl: false,
        zoomControl: ZOOMCTRL,
        center: MYCENTER,
        zoom: ZOOMLEVEL,
        layers: [cbasemap],
        preferCanvas: true // recommended when loading large layers.
        
    });

    heatmapPoints = eheatpoints.map(function (p) { 
        return [p.fields.latitude, p.fields.longitude, .5];
    });

    
    L_HEATMAP = L.heatLayer(heatmapPoints, {radius: 25});

    LoadEvents(); // Load events


    // Legend
    L.Control.MyControl = L.Control.extend({
            onAdd: function(map) {
                var el = L.DomUtil.create('div', 'leaflet-control-layers leaflet-control c-legend');

                el.innerHTML = `
                    <div class="basemap__dropdown is-open text-center pb-2 " >
                        <span class="options__title lbl-lrecent" style="border-bottom: 1px solid #4B4B4B;font-size:12px">Recent Earthquakes</span>
                        <img id="map_legend" src="${img_path}map_legend.png" class="pt-1 lbl-lrecent" >
                    </div>
                `;

                return el;
            },
            onClick: function(map) {
                // Nothing to do here
            },
            onRemove: function(map) {
                // Nothing to do here
            }
        });

    L.control.myControl = function(opts) {
        return new L.Control.MyControl(opts);
    }

    L.control.myControl({
        position: 'topright'
    }).addTo(map);

    // Long Lat Control
    L.Control.Watermark = L.Control.extend({
        onAdd: function(map) {
            const div = L.DomUtil.create('div', 'leaflet-control-layers leaflet-control');
            div.innerHTML = 
                `
                <div class="text-muted p-1 mt-1" style="color:#667 !important">
                    &nbsp;<i class="fa fa-location-arrow f-14"></i>&nbsp;&nbsp;Latitude:<span class="lbl-lat">0</span>&nbsp;Longitude:<span class="lbl-lon">0</span>
                </div>
                `
            return div;
        },
    });

L.control.watermark = function(opts) {
    return new L.Control.Watermark(opts);
}

L.control.watermark({ position: 'bottomleft' }).addTo(map);

// Basemaps Controls
L.Control.MyControl = L.Control.extend({
    onAdd: function(map) {
        var el = L.DomUtil.create('div', 'leaflet-control-layers leaflet-control');

        el.innerHTML = `
    
            <button class="eq-button button-map-control" id="btn-basemap" ><i class="fa fa-globe f-14"></i>&nbsp;BASEMAPS</button>
    
        `;

        return el;
    },
    onClick: function(map) {
    
    },
    onRemove: function(map) {
        // Nothing to do here
    }
});

L.control.myControl = function(opts) {
    return new L.Control.MyControl(opts);
}

L.control.myControl({
    position: 'bottomright'
}).addTo(map);

// Basemap Selection
L.Control.MyControl = L.Control.extend({
            onAdd: function(map) {
                var el = L.DomUtil.create('div', 'leaflet-control-layers leaflet-control ctrl-basemap');

                el.innerHTML = `
                <div class="basemap__dropdown is-open noselect">
                    <span class="options__title">Basemaps</span>
                    <div class="basemap__options">
                        <div class="basemap b-switch is-active" title=" White Basemap" layer="white">
                            <img src="${img_path}white.jpg">
                            <span class="basemap__title">WHITE</span>
                        
                        </div>
                        <div class="basemap b-switch " title="Black Basemap" layer="black">
                            <img src="${img_path}black.jpg">
                            <span class="basemap__title">BLACK</span>
                            
                        </div>
                        <div class="basemap b-switch " title="Satellite Basemap" layer="satellite">
                            <img src="${img_path}satellite.jpg" >
                            <span class="basemap__title">SATELLITE</span>
                            
                        </div>
                        <div class="basemap b-switch " title="OSM Basemap" layer="osm">
                            <img src="${img_path}osm.jpg" >
                            <span class="basemap__title">OSM</span>
                            
                        </div>
                    </div>
                </div>
                `;

            
                el.style.position = 'absolute';
                el.style.bottom = "50px";
                el.style.right = "0px";
                L.DomEvent.disableClickPropagation(el);

                return el;
            },

            onRemove: function(map) {
                // Nothing to do here
            }
        });

        L.control.myControl = function(opts) {
            return new L.Control.MyControl(opts);
        }

        L.control.myControl({
            position: 'bottomright'
        }).addTo(map);

        // Layer Controls
        L.Control.MyControl = L.Control.extend({
            onAdd: function(map) {
                var el = L.DomUtil.create('div', 'leaflet-control-layers leaflet-control');

                el.innerHTML = `
            
                    <button class="eq-button button-map-control " id="btn-layers"><i class="fa fa-cogs f-14"></i> OPTIONS </button>
            
                `;

                return el;
            },
            onClick: function(map) {
                // Nothing to do here
            },
            onRemove: function(map) {
                // Nothing to do here
            }
        });

        L.control.myControl = function(opts) {
            return new L.Control.MyControl(opts);
        }

        L.control.myControl({
            position: 'bottomright'
        }).addTo(map);


        // Layers Selection
        L.Control.MyControl = L.Control.extend({
            onAdd: function(map) {
                var el = L.DomUtil.create('div', 'leaflet-control-layers leaflet-control ctrl-layers');

                el.innerHTML = `
                    <div class="card-block accordion-block noselect">
                        <div id="accordion" role="tablist" aria-multiselectable="true">
                            <div class="accordion-panel">
                                <div class="accordion-heading" role="tab" id="headingOne">
                                    <h3 class="card-title accordion-title mt-0 mb-0">
                                    <a class="pl-2 p-0 accordion-msg lbl-h-layer" data-toggle="collapse" data-parent="#accordion" href="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
                                        <span class="badge--default lbl-cboundaries">0</span>Layers/Boundaries
                                    </a>
                                </h3>
                                </div>
                                <div id="collapseOne" class="panel-collapse in collapse show" role="tabpanel" aria-labelledby="headingOne">
                                    <div class="accordion-content accordion-desc pb-2 pr-0">
                                        <ul class="eq-ul-layers pl-3 mb-0">
                                            <li>
                                                <label class="eq-switch mt-1">
                                                    <input type="checkbox" class="l-switch s-boundaries" layer="show_heat" ${settings.fields.show_heatmap == 1 ? 'checked="checked"' : '' } >
                                                    <span class="eq-slider round"></span>
                                                </label>
                                                &nbsp;&nbsp;&nbsp;Show Heatmap
                                            </li>
                                            <li>
                                                <label class="eq-switch mt-1">
                                                    <input type="checkbox" class="l-switch s-boundaries" layer="show_aoi"  ${settings.fields.show_aoi == 1  ? 'checked="checked"' : '' } >
                                                    <span class="eq-slider round"></span>
                                                </label>
                                                &nbsp;&nbsp;&nbsp;Area of Interest
                                            </li>
                                        
                                            
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            <div class="accordion-panel">
                                <div class="accordion-heading" role="tab" id="headingTwo">
                                    <h3 class="card-title accordion-title mt-0 mb-0">
                                    <a class="pl-2 p-0 accordion-msg lbl-h-layer" data-toggle="collapse" data-parent="#accordion" href="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                                        <span class="badge--default lbl-cfilter">0</span>Earthquakes
                                    </a>
                                </h3>
                                </div>
                                <div id="collapseTwo" class="panel-collapse in collapse show" role="tabpanel" aria-labelledby="headingTwo">
                                    <div class="accordion-content accordion-desc pb-2 pr-0">
                                    
                                        <ul class="eq-ul-layers pl-3 mb-0">
                                            <li>
                                                <label class="eq-switch mt-1 ">
                                                    <input type="checkbox" class="f-switch s-filter" filter="show_mag0" ${settings.fields.filter_1 == 1 ? 'checked="checked"' : '' }>
                                                    <span class="eq-slider round"></span>
                                                </label>
                                                &nbsp;&nbsp;&nbsp;Show only magnitude 0 - 4.9
                                            </li>
                                            <li>
                                                <label class="eq-switch mt-1">
                                                    <input type="checkbox" class="f-switch  s-filter" filter="show_mag1"  ${settings.fields.filter_2 == 1 ? 'checked="checked"' : '' }>
                                                    <span class="eq-slider round"></span>
                                                </label>
                                                &nbsp;&nbsp;&nbsp;Show only magnitude 5 - 5.9
                                            </li>
                                            <li>
                                                <label class="eq-switch mt-1">
                                                    <input type="checkbox" class="f-switch  s-filter" filter="show_mag2"  ${settings.fields.filter_3 == 1 ? 'checked="checked"' : '' }>
                                                    <span class="eq-slider round"></span>
                                                </label>
                                                &nbsp;&nbsp;&nbsp;Show only magnitude 6 - 6.4
                                            </li>
                                            <li>
                                                <label class="eq-switch mt-1">
                                                    <input type="checkbox" class="f-switch  s-filter" filter="show_mag3"  ${settings.fields.filter_4 == 1 ? 'checked="checked"' : '' }>
                                                    <span class="eq-slider round"></span>
                                                </label>
                                                &nbsp;&nbsp;&nbsp;Show only magnitude >= 6.5 
                                            </li>
                                            <li>
                                                <label class="eq-switch mt-1">
                                                    <input type="checkbox" class="f-switch  s-filter" filter="only_aoi"  ${settings.fields.inside_aoi == 1 ? 'checked="checked"' : '' }>
                                                    <span class="eq-slider round"></span>
                                                </label>
                                                &nbsp;&nbsp;&nbsp;Show only inside AOI 
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        
                        
                        </div>
                    </div>
                `;

            
                el.style.position = 'absolute';
                el.style.bottom = "50px";
                el.style.right = "0px";
                L.DomEvent.disableClickPropagation(el);

                return el;
            },

            onRemove: function(map) {
                // Nothing to do here
            }
        });

        L.control.myControl = function(opts) {
            return new L.Control.MyControl(opts);
        }

        L.control.myControl({
            position: 'bottomright'
        }).addTo(map);

    // FUNCTIONS

    function LoadEvents(){
           
        // Clear Event List
        $('.event-list').empty();
        
        map.createPane("EventMarker");
        map.getPane("EventMarker").style.zIndex = 999;
        // for (let i = 0; i < EQ_COUNT; i++){
        //     const event_li = initEventList(events[i], i);

        //     $('.event-list').append(event_li);
        //     addMarker(events[i], i);
        // }
        events.forEach((event, i) => {
            const event_li = initEventList(event, i);

            $('.event-list').append(event_li);
            addMarker(events[i], i);
        });
    }


    map.on('mousemove', function(e) {
        const latLng = getCoordinates(e.latlng);
        $(".lbl-lat").html(latLng[0]);
        $(".lbl-lon").html(latLng[1]);
    });

    function addMarker(event, index, tocenter =0) {
        let marker;
       
        const latLng = getLatLong( event.fields.latitude, event.fields.longitude );

        if (index === 0) { // Latest
            var ico = L.icon({
                iconUrl: recent_ico,
                iconAnchor:   [0, 0], 
                popupAnchor:  [15, 10]
            });
            marker = new L.marker(latLng, {icon: ico}); 
        }else{
            const t = compute_magnitude(parseFloat(event.fields.magnitude));
            
            marker = new L.circle(latLng, {
                color: t.color,
                fillColor: t.color,
                fillOpacity: .8,
                radius: t.magnitude,
                stroke: false,   
                pane: "EventMarker"                 
            });   
        }

        marker.event = event;
        marker.on('click', eqMarkerClick);
        marker.bindPopup(setEqPopup(event));

        map.addLayer(marker);  

        if (tocenter){
            marker.openPopup();
            map.setView(latLng, 4); 
            setLatLngMarker(latLng);
        }
    }

    function getColor(mag) {
        const t = compute_magnitude(parseFloat(mag));
        return t.color;
    }
    function getLatLong(latitude, longitude){
        return [parseFloat(latitude), parseFloat(longitude) < 0 ? 180+parseFloat(longitude)+180 : parseFloat(longitude)];
    }

    function setEqPopup(event){
        let bulletin_link = "";

        const bulletin_no = ( typeof event.fields !== "undefined" ? event.fields.bulletin_no : event.bulletin_no );
        const event_id =  ( typeof event.fields !== "undefined" ? event.pk : event.event_id );

        if (bulletin_no > 0 ){
            bulletin_link = ` 
                            <button class="btn btn-info btn-pill  btn-view-bulletin float-right dropdown-toggle"  data-toggle="dropdown" href="#" role="button"><i class="fa-solid fa-file-pdf  mr-2"></i>Bulletins
                            </button>
                            <div class="dropdown-menu dropdown-menu-small">
                                
                            `;

            // If has bulletin
            let b_no = 0;
            do {
                bulletin_link += `
                    <a class="dropdown-item" href="earthquake/view-bulletin/${event_id}/${b_no+1}"  target="_blank">Bulletin ${b_no+1}</a>
                `;
               b_no++;
            } while (b_no<bulletin_no);          

            bulletin_link += '</div>';
            
        }

        const event_datetime = moment(event.fields.event_datetime).format("hh:mm:ss MMMM DD, YYYY [(UTC)]");
        const popup = `
                <table class="eq-popup">
                <tbody>
                    <tr class="eq-popup-region">
                        <td colspan="2">
                            <span class="info-title eq-txt-primary">${event.fields.region}</span>
                        <hr class="eq-hr">
                        </td>
                    </tr>
                    <tr>
                        <td><nobr>Origin Time</nobr></td>
                        <td><nobr>: ${event_datetime}</nobr></td>
                    </tr>
                    <tr>
                        <td>Longitude</td>
                        <td>: ${event.fields.longitude}</td>
                    </tr>
                    <tr>
                        <td>Latitude</td>
                        <td>: ${event.fields.latitude}</td>
                    </tr>
                    <tr>
                        <td>Magnitude</td>
                        <td>: ${event.fields.magnitude} ${event.fields.mag_type}</td>
                    </tr>
                    <tr>
                        <td>Depth</td>
                        <td>: ${event.fields.depth} km.</td>
                    </tr>
                    <tr>
                        <td colspan="2" class="p-0"><hr class="eq-hr"></td>
                        
                    </tr>
                    <tr class="eq-popup-menu">
                        
                        <td colspan="2" class="p-0 eq-send-menu">
                            <button class="btn btn-primary btn-pill btn-advisory" data-toggle="modal" data-target="#modal-advisory" data-id="${event.pk}">
                                <i class="fa-solid fa-paper-plane mr-2"></i>
                                Send Advisory
                            </button>
                            ${bulletin_link}
                
                        </td>
                    </tr>
                    
                </tbody>
                </table>
        `;
        return popup;
    }

    function eqMarkerClick(e){    
        const event =  e.target.event;

        const latLng = getLatLong(event.fields.latitude, event.fields.longitude);
        setLatLngMarker(latLng);

        selectListEvent(event.pk);

        map.setView(latLng, 4); 
    }

    function unselectEvents(){
        $('.event-list li.selected').removeClass("selected");
    }
    function selectListEvent(event_id){
        unselectEvents();
        $(`li[data-id="${event_id}"]`).addClass("selected");

        const li = document.getElementById(`tr${event_id}`);
        li.scrollIntoView();
    }

    function setLatLngMarker(latLng){
        $(".lbl-lat").html(latLng[0]);
        $(".lbl-lon").html(latLng[1]);
    }


    function initEventList(event, index){
  
        const event_li = `
                <li id="tr${event.pk}" data-id="${event.pk}" class="li-event ${(index == 0 ? 'selected' : '')}">
                    <table>
                        <tbody>
                            <tr>
                                <td>
                                    <div class="event-mag" style="color:#ffff; background-color: rgba(${getRGB(getColor(event.fields.magnitude))});">${parseFloat(event.fields.magnitude).toFixed(1)}</div>
                                </td> 
                                <td class="pl-2">
                                    <a href="javascript:void(0)" class="event-header">
                                        <h5 class="event-region mt-1 mb-1" style="color:${getColor(event.fields.magnitude)}">${event.fields.region}</h5>
                                    </a> 
                                    <span class="event-info">
                                        OT: ${ event.fields.event_datetime } Depth: ${ event.fields.depth } km.
                                        
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </li>
                           
            `;
        return event_li;
    }


    function compute_magnitude(magnitude) {
        var ret = {};
        var multiplier;
        var color = '#000';

        if      (magnitude >= 6.5) { color = "#ff0000"; multiplier = 4; }
        else if (magnitude >= 6.0) { color = "#FF7D11"; multiplier = 3; }
        else if (magnitude >= 5.0) { color = "#0055BB"; multiplier = 2; }
        else                       { color = "#4C9E00"; multiplier = 1; }
        ret.magnitude = multiplier * parseFloat(magnitude) * 12000;
        ret.color = color;
    
        return ret;
    }

    function getRGB(color){

        var ncolor = "255, 255, 255";
        if      (color == "#ff0000") { ncolor = "252, 129, 129"    ; }
        else if (color == "#FF7D11") { ncolor = "247, 181, 126" ; }
        else if (color == "#0055BB") { ncolor = "120, 179, 250"   ; }
        else                         { ncolor = "124, 173, 78"   ; }

        return ncolor;
    }

    function getCoordinates(latlng){
        var lat = latlng.lat; lat = lat.toFixed(5);
        var lng = latlng.lng; lng = lng.toFixed(5);

        return [lat, lng];
    }

    // PUSHER
    var pusher = new Pusher(PUSHER.KEY, {
        cluster: PUSHER.CLUSTER
    });

    var channel = pusher.subscribe(PUSHER.CHANNEL);
    channel.bind(PUSHER.EVENT, function(new_event) {
        if (typeof new_event.event_id !== "undefined"){

            // Check if inside IOR
            const lngLat =  [new_event.longitude, new_event.latitude] ;
        
            is_inside1 = (turf.booleanPointInPolygon(lngLat, POLY1) ? true : false); // If in aor dont hide
            is_inside2 = (turf.booleanPointInPolygon(lngLat, POLY2) ? true : false); 
            is_inside3 = (turf.booleanPointInPolygon(lngLat, POLY3) ? true : false);
            if (!is_inside1 && !is_inside2 && !is_inside3 ) // Dont add
                return false

            msg = (MSG.EARTHQUAKE.msg).replace('_REGION_', new_event.region).replace('_MAG_', new_event.magnitude.concat(' ').concat(new_event.mag_type));

            new_event.pk = new_event.event_id
            new_event.fields = {
                'source' : new_event.source,
                'latitude': new_event.latitude,
                'longitude' : new_event.longitude,
                'magnitude': new_event.magnitude,
                'mag_type': new_event.mag_type,
                'depth' : new_event.depth,
                'event_datetime' : new_event.event_datetime,
                'region': new_event.region,
                'bulletin_no': new_event.bulletin_no,
                'phase_count': new_event.phase_count,
                'is_fake': new_event.is_fake,
                'bulletin_details': new_event.bulletin_details,
                'status' : new_event.status,
            }
          
           
            
            // Check if event already in the list
         
            const index = events.findIndex(event => event.pk === new_event.event_id);
            
            if (index < 0){   // Event does not exist so add to list
                msg = msg.replace('_UPDATE_', 'New');

                // Check if already max # of events
                if(events.length == EQ_COUNT){

                    // Get last event id
                    const last_event_id = events[EQ_COUNT-1].event_id ;
                    
                    // remove last
                    events.splice(-1);

                    // Remove layer of the last event
                    if (typeof last_event_id !== "undefined"){
                        map.eachLayer(function (layer) { 
                            if (typeof layer.event !== "undefined" && layer.event.pk.event_id === last_event_id){
                                map.removeLayer(layer); 
                                return false;
                            }
                        });
                    }

                    // Remove list of the last event
                    $(`#tr${last_event_id}`).remove();

                }  
                events = [new_event, ...events]; //insert new event
                

                //Remove pulse marker because of the new event will be the new pulse marker
                map.eachLayer(function (layer) { 
                    if (typeof layer.options.icon !== "undefined" && typeof layer.event.pk.event_id !== "undefined"){ 
                        
                        map.removeLayer(layer); 

                        // Change to circle marker
                        addMarker(layer.event, 1);  
                        return false;
                    }
                });
    
                // Create new pulse layer for new event
                addMarker(new_event, 0, 1);

                // List
                const event_index = $('.li-event').length;
                const event_li = initEventList(new_event, 0);

                
                $('.eq-list').prepend(event_li);
                
                // Select List
                $('.eq-list li').removeClass('selected'); // Remove other class
                $(`#tr${new_event.event_id}`).addClass('selected'); // Add active 
                
            }else{ // if exist select the event

                msg = msg.replace('_UPDATE_', 'Updated');

                $('.eq-list li').removeClass('selected'); // Remove other class
                $(`#tr${new_event.event_id}`).addClass('selected'); // Add active 

                // Update marker
                map.eachLayer(function (layer) { 
           
                    if (typeof layer.event !== "undefined" && layer.event.pk.event_id === new_event.event_id ){ 

                        
                        map.removeLayer(layer);

                        // Check if it is the pulse marker
                        if (typeof layer.options.icon !== "undefined")
                            addMarker(new_event, 0, 1);
                        else
                            addMarker(new_event, 1, 1);
                        
                        return false;
                    }
                }.bind(this));

            }
       
            tata[MSG.EARTHQUAKE.type]('', msg, {
                duration: 10000,
                progress: true,
                holding: false,
                animate: 'fade',
                closeBtn: 'slide',
                onClick: null,
                onClose: null
            })

        }
    });

    // END PUSHER 

    // Trigger / Events
    $(document).on('click','.event-list li', function() { 
            
        $('.event-list li').removeClass('selected'); // Remove other class
        $(this).addClass('selected'); // Add active to selected basemap

        const event_id = $(this).attr("data-id");

        // Set focus
        map.eachLayer(function (layer) { 
            if (typeof layer.event !== "undefined" && layer.event.pk === event_id ){ 

                const latLng = getLatLong(layer.event.fields.latitude,layer.event.fields.longitude);
                layer.openPopup();
                map.setView(latLng, 4); 
                setLatLngMarker(latLng);
                return false;
            }
        }.bind(this))

    });

    $('#modal-advisory').on('hidden.bs.modal', function (e) {
        $('.event-list').css("position", "absolute"); // FIXED for scroll not clickable
    })

    $(document).on('click','.btn-advisory', function() { 

        // Remove absolute position // FIXED for scroll not clickable
        $('.event-list').css("position", "unset");

        let opt_bulletin = "";
        const event_id  = $(this).data("id");

        $('#event_id').val(event_id);

        const index = events.findIndex(event => event.pk === event_id);
        const event = events[index];

        $('.div-bulletin').empty();
        $('.text-region').html(event.fields.region);
      
        b_no = 0;
        if (event.fields.bulletin_no > 0 ){
            opt_bulletin += `<div class="custom-control custom-radio mb-3 ml-3">
                <input type="radio" id="bulletin_-1" value="0" name="bulletin" class="custom-control-input" checked>
                <label class="custom-control-label text-primary" for="bulletin_-1">No attachment</label>
            </div>`;
            do {
                opt_bulletin += `<div class="custom-control custom-radio mb-3 ml-3">
                    <input type="radio" id="bulletin_${b_no+1}" value="${b_no+1}" name="bulletin" class="custom-control-input">
                    <label class="custom-control-label text-primary" for="bulletin_${b_no+1}">Bulletin ${b_no+1}</label>
                </div>`;
               b_no++;
            } while (b_no<event.fields.bulletin_no);          
        }

        $('.div-bulletin').append(opt_bulletin);
    
        // Populate Email
        let msg = "SDC Earthquake information :\n\n" +
        `Origin Time = ${event.fields.event_datetime} IST\n` +
        `Magnitude = ${event.fields.magnitude} Depth = ${event.fields.depth} Km\n` +
        `Longitude = ${event.fields.longitude} Latitude = ${event.fields.latitude}\n` +
        `Region = ${event.fields.region}\n\n` +
        `Message sent by SDC automatic Alerting System`;
        
        $('#message').val(msg);
    });

    $(document).on('click','.btn-send', function() { // Send Email

        $('#modal-advisory').modal('hide');
        $(".modal-backdrop").remove();
        
        const event_id = $('#event_id').val();
        const index = events.findIndex(event => event.pk === event_id);
        const event = events[index];
        
        if (index == -1){
            tata[MSG.ERROR.type]('', MSG.ERROR.msg, {
                duration: 5000,
                progress: true,
                holding: false,
                animate: 'fade',
                closeBtn: 'slide',
            })
            return false;
        }

        msg = (MSG.SEND.msg).replace('_REGION_', event.fields.region).replace('_MAG_', event.fields.magnitude.concat(' ').concat(event.fields.mag_type));
       
        tata[MSG.SEND.type]('', msg, {
            duration: 10000,
            progress: false,
            holding: false,
            animate: 'fade',
            closeBtn: 'slide',
            onClick: null,
            onClose: null
        })
        $.ajax({
            type: "POST",
            url: "earthquake/send_advisory",
            data: {
                send_to     : $('#emails').val(),
                bulletin_no : $("input[name='bulletin']:checked").val(),
                event_id    : $('#event_id').val(),
                simulation  : $('#simulation').prop("checked"),
                csrfmiddlewaretoken: window.CSRF_TOKEN,
            },
            dataType: 'json',
            success:function(data){
            
                tata.clear(); // Clear previous notif'
                
                msg = (MSG.SUCCESS.msg).replace('_REGION_', event.fields.region).replace('_MAG_', event.fields.magnitude.concat(' ').concat(event.fields.mag_type));
            
                tata[MSG.SUCCESS.type]('', msg, {
                    duration: 5000,
                    progress: true,
                    holding: false,
                    animate: 'fade',
                    closeBtn: 'slide',
                })
                    
            },error: function(){
                $('.tata.tata-info').css('display','none');
                tata.clear(); // Clear previous notif
            
                tata[MSG.ERROR.type]('', MSG.ERROR.msg, {
                    duration: 5000,
                    progress: true,
                    holding: false,
                    animate: 'fade',
                    closeBtn: 'slide',
                })

            }
        });

    });

    $(document).on('click','#btn-basemap', function() { 
        ctrl_layer =  $(".ctrl-basemap");
        $(".ctrl-layers").hide("slide", {direction: "right"}, 100);
        if (ctrl_layer.is(":visible"))
            ctrl_layer.hide("slide", {direction: "right"}, 100);
        else
            ctrl_layer.show("slide", {direction: "right"}, 100);
    });

    $(document).on('click','#btn-layers', function() { 
        ctrl_layer =  $(".ctrl-layers");
        $(".ctrl-basemap").hide("slide", {direction: "right"}, 100);

        if (ctrl_layer.is(":visible"))
            ctrl_layer.hide("slide", {direction: "right"}, 100);
        else
            ctrl_layer.show("slide", {direction: "right"}, 100);
    });


    let boundaries_count = 0;
    let filter_count = 0;
    if ($("input[layer='show_heat']").prop("checked") == true) { 
        boundaries_count++;
            map.addLayer(L_HEATMAP);  
            $('#map_legend').attr('src', img_path + 'map_heat_legend.png');
    }
    if ($("input[layer='show_aoi']").prop("checked") == true) { 
        boundaries_count++; 
        map.addLayer(L_AOI1);
        map.addLayer(L_AOI2);
        map.addLayer(L_AOI3);
     }
    countOptBoundaries();

    if ($("input[filter='show_mag0']").prop("checked") == true){ filter_count++; }
    if ($("input[filter='show_mag1']").prop("checked") == true){ filter_count++; }
    if ($("input[filter='show_mag2']").prop("checked") == true){ filter_count++; }
    if ($("input[filter='show_mag3']").prop("checked") == true){ filter_count++; }
    if ($("input[filter='only_aoi']").prop("checked") == true){ filter_count++; }

    countOptFilter();

    function countOptBoundaries(){
        $('.lbl-cboundaries').html(boundaries_count);
    }
    function countOptFilter(){
        $('.lbl-cfilter').html(filter_count);
    }
    $(document).on('change','.s-filter', function (){
            
        filter_count += ($(this).prop("checked") == true ? 1 : -1);
        countOptFilter();

        $.ajax({
            type: "POST",
            url: "earthquake/filter-earthquake",
            data: {
                filter1: $("input[filter='show_mag0']").prop("checked"),
                filter2: $("input[filter='show_mag1']").prop("checked"),
                filter3: $("input[filter='show_mag2']").prop("checked"),
                filter4: $("input[filter='show_mag3']").prop("checked"),
                only_aoi: $("input[filter='only_aoi']").prop("checked"),
                csrfmiddlewaretoken: window.CSRF_TOKEN,
            },
            dataType: 'json',
            success:function(data){
                // console.log(JSON.parse(data.earthquakes));
            
                // Clear Layers
                map.eachLayer(function (layer) { 
                    if (typeof layer.event !== "undefined" ){
                        map.removeLayer(layer); 
                        return false;
                    }
                });

                events = JSON.parse(data.earthquakes); // New Events

                // Add Layers
                LoadEvents();
               
            }
        });
    });
    $(document).on('change','.s-boundaries', function (){
        boundaries_count += ($(this).prop("checked") == true ? 1 : -1);
        countOptBoundaries();
    });

    $(document).on('click','.b-switch', function() { 
        const slayer = getLayer($(this).attr('layer'));
        $('.b-switch').removeClass('is-active'); // Remove other class
        $(this).addClass('is-active'); // Add active to selected basemap
        map.removeLayer(cbasemap);	
        map.addLayer(slayer);	
        cbasemap = slayer;
    });
      // Show layers based on switch
      $(document).on('change','.l-switch', function() { 
        const slayer = getLayer($(this).attr('layer'));
        if ($(this).is(":checked")){
            if ($(this).attr('layer') == "show_heat") {
                map.addLayer(slayer);	
                $('#map_legend').attr('src', img_path + 'map_heat_legend.png');
            }else{
                map.addLayer(L_AOI1);
                map.addLayer(L_AOI2);
                map.addLayer(L_AOI3);
            }
        }else{
         	
            if ($(this).attr('layer') == "show_heat") {
                map.removeLayer(slayer);
                $('#map_legend').attr('src', img_path + 'map_legend.png');
            }else{
                map.removeLayer(L_AOI1);
                map.removeLayer(L_AOI2);
                map.removeLayer(L_AOI3);
            }
        }
        
    });

    function getLayer(layer){
        let slayer;
        switch (layer) {
            case "show_heat":
                slayer = L_HEATMAP
                break;
            case "white":
                slayer = MWHITE
                break;
            case "black":
                slayer = MBLACK
                break;
            case "satellite":
                slayer = MSATELLITE
                break;
            case "osm":
                slayer = MOSM;
                break;   
        }
        return slayer;
    }

    if (settings.fields.simulation == 0){
        $('.div-sim').addClass('d-none')
    }
});