//-----------------------------------------------------------------------------------------------------------------//
//--------------------------------------------- Font Limiter function  --------------------------------------------//
//-----------------------------------------------------------------------------------------------------------------//
// ----------** Cambodia **---------- //
$('#lao_Objective').keyup(function () {
    var lao_obj_characterCount = $(this).val().length,
        lao_obj_current = $('#lao_obj_current'),
        lao_obj_maximum = $('#lao_obj_maximum'),
        lao_obj_theCount = $('#lao_obj_count');

    lao_obj_current.text(lao_obj_characterCount);
});
$('#lao_Budget').keyup(function () {
    var lao_bud_characterCount = $(this).val().length,
        lao_bud_current = $('#lao_bud_current'),
        lao_bud_maximum = $('#lao_bud_maximum'),
        lao_bud_theCount = $('#lao_bud_count');

    lao_bud_current.text(lao_bud_characterCount);
});
$('#lao_Location').keyup(function () {
    var lao_loc_characterCount = $(this).val().length,
        lao_loc_current = $('#lao_loc_current'),
        lao_loc_maximum = $('#lao_loc_maximum'),
        lao_loc_theCount = $('#lao_loc_count');

    lao_loc_current.text(lao_loc_characterCount);
});
$('#lao_Outcome').keyup(function () {
    var lao_out_characterCount = $(this).val().length,
        lao_out_current = $('#lao_out_current'),
        lao_out_maximum = $('#lao_out_maximum'),
        lao_out_theCount = $('#lao_out_count');

    lao_out_current.text(lao_out_characterCount);
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