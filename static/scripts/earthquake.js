$(document).ready(function() {
 
   
    const MINZZOOM = 3;     // Max Zoom out
    const MAXZOOM = 9;    // Max Zoom in
    const ZOOMLEVEL = 5;
    const ZOOMCTRL = false;
    const SLAT = 11.562108;   //Default to Location
    const SLONG = 104.888535;               
    const MYCENTER = [SLAT, SLONG]; 
    const EQ_COUNT = settings.fields.number_events;
    const AOR_POLY = turf.polygon([[[72.268492,39.827522],[80.182943,40.096983],[92.671651,33.927409],[109.030101,20.202924],[115.010609,-7.294363],
        [105.16036,-14.368173],[85.108067,-14.02735],[64.879645,-12.315853],[58.371445,7.081814],[61.361699,32.159338],[72.268492,39.827522]]]);
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
    const MAP_BMAP  = L.tileLayer("https://api.mapbox.com/styles/v1/nazmul-rimes/ck9wljpn30kbx1is5a630hmtb/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoibmF6bXVsLXJpbWVzIiwiYSI6ImNrOWFzeHNtcDA3MjAzbG50dnB0YmkxNnAifQ.usNB6Kf9PyFtKTUF1XI38g",
        {
            maxZoom: MAXZOOM,
            minZoom: MINZZOOM,
        });

    //**** Initialize Map
    map = L.map('cam_map', {
        attributionControl: false,
        zoomControl: ZOOMCTRL,
        center: MYCENTER,
        zoom: ZOOMLEVEL,
        layers: [MAP_BMAP],
        preferCanvas: true // recommended when loading large layers.
        
    });

    heatmapPoints = events.map(function (p) { 
        return [p.fields.latitude, p.fields.longitude, 1];
    });

    
    L.heatLayer(heatmapPoints, {radius: 25}).addTo(map);

    LoadEvents(); // Load events

    // FUNCTIONS

    function LoadEvents(){
           
        // Clear Event List
        $('.event-list').empty();
        
        map.createPane("EventMarker");
        map.getPane("EventMarker").style.zIndex = 999;
        for (let i = 0; i < EQ_COUNT; i++){
            const event_li = initEventList(events[i], i);

            $('.event-list').append(event_li);
            addMarker(events[i], i);
        }
    }

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
        
            is_inside = (turf.booleanPointInPolygon(lngLat, AOR_POLY) ? true : false); // If in aor dont hide
            is_inside = true;
            if (!is_inside) // Dont add
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

    $(document).on('click','.btn-advisory', function() { 

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
        let msg = "SATARK - OSDMA Earthquake information :\n\n" +
        `Origin Time = ${event.fields.event_datetime} IST\n` +
        `Magnitude = ${event.fields.magnitude} Depth = ${event.fields.depth} Km\n` +
        `Longitude = ${event.fields.longitude} Latitude = ${event.fields.latitude}\n` +
        `Region = ${event.fields.region}\n\n` +
        `Massage sent by SATARK automatic Alerting System`;
        
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




});