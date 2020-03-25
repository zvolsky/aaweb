function submitted() {
    $('form#createForm').addClass('hidden');
    $('p#submittedMsg').removeClass('hidden');  // msg: this will take a while..
}
$('button#submitBtn').click(submitted);
