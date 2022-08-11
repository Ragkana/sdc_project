//-----------------------------------------------------------------------------------------------------------------//
//--------------------------------------------- Font Limiter function  --------------------------------------------//
//-----------------------------------------------------------------------------------------------------------------//
// ----------** Cambodia **---------- //
$('#KHM_Objective').keyup(function () {
    var khm_obj_characterCount = $(this).val().length,
        khm_obj_current = $('#khm_obj_current'),
        khm_obj_maximum = $('#khm_obj_maximum'),
        khm_obj_theCount = $('#khm_obj_count');

    khm_obj_current.text(khm_obj_characterCount);
});
$('#KHM_Budget').keyup(function () {
    var khm_bud_characterCount = $(this).val().length,
        khm_bud_current = $('#khm_bud_current'),
        khm_bud_maximum = $('#khm_bud_maximum'),
        khm_bud_theCount = $('#khm_bud_count');

    khm_bud_current.text(khm_bud_characterCount);
});
$('#KHM_Location').keyup(function () {
    var khm_loc_characterCount = $(this).val().length,
        khm_loc_current = $('#khm_loc_current'),
        khm_loc_maximum = $('#khm_loc_maximum'),
        khm_loc_theCount = $('#khm_loc_count');

    khm_loc_current.text(khm_loc_characterCount);
});
$('#KHM_Outcome').keyup(function () {
    var khm_out_characterCount = $(this).val().length,
        khm_out_current = $('#khm_out_current'),
        khm_out_maximum = $('#khm_out_maximum'),
        khm_out_theCount = $('#khm_out_count');

    khm_out_current.text(khm_out_characterCount);
});
//-----------------------------------------------------------------------------------------------------------------//
//--------------------------------------------- invalid form function  --------------------------------------------//
//-----------------------------------------------------------------------------------------------------------------//
(function () {
    'use strict';
    window.addEventListener('load', function () {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();
