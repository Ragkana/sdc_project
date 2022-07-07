//----------------------------------------------------------------------------------------------//
//--------------------------------------------- Tab --------------------------------------------//
//----------------------------------------------------------------------------------------------//
$(document).ready(function () {
    $("#myTab a").click(function (e) {
        e.preventDefault();
        $(this).tab("show");
    });
});
//-------------------------------------------------------------------------------------------------------//
//--------------------------------------------- Date Picker  --------------------------------------------//
//------------------------------------------------------------------------------------------------------//
  // Date picker
  $('#datepicker').datepicker({
    clearBtn: true,
    todayHighlight: true,
    autoclose: true, // When date has been selected
    immediateUpdates: true,
    orientation: 'auto bottom',
    language: 'en',
    endDate: new Date(), // cant select tomorrow on date-picker
    format: 'yyyy-mm-dd'
  });

  $('#datepicker').datepicker('setDate', 'today').date();