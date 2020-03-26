function submitted() {
    $('form#createForm').addClass('d-none');
    $('p#submittedMsg').removeClass('d-none');  // msg: this will take a while..
}
$('button#submitBtn').click(submitted);
