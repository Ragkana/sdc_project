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

//-----------------------------------------------------------------------------------------------------------//
//--------------------------------------------- Dropdown Search  --------------------------------------------//
//-----------------------------------------------------------------------------------------------------------//

function DropdownFilter(search, dropdown) {
  var input, filter, ul, li, a, i;
  input = document.getElementById(search);
  filter = input.value.toUpperCase();
  div = document.getElementById(dropdown);
  a = div.getElementsByTagName("option");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

//-----------------------------------------------------------------------------------------------------------------//
//--------------------------------------------- Font Limiter function  --------------------------------------------//
//-----------------------------------------------------------------------------------------------------------------//
// Comment
function CommentLimiter() {
$('#comment_box').keyup(function () {
  var cm_characterCount = $('#comment_box').val().length;
    $('#cm_current').text(cm_characterCount);
});
}





