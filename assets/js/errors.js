function err404() {
    $('#post').html('');
    $('#error').removeClass('d-none').html('<p class="lead"><strong>Post not Found</strong><br />The selected post was not found! Did you follow the correct link?</p>');
}

function err505() {
    $('#post').html('');
    $('#error').removeClass('d-none').html('<p class="lead"><strong>Internal Server Error</strong><br />Someting bad happened in our side, sorry! Try again and if it repeats, please send us an email</p>');
}

function errUnknown(err='') {
    $('#post').html('');
    var errtext = '<p class="lead"><strong>Unknown Error</strong><br />Hmmm OK, this is weird. '
    if (err.length > 0) {
        errtext += 'Here is what I know: ' + err;
    } else {
        errtext += 'I have no idea what happened!';
    }
    errtext += '<br />Try again and if it repeats, please send us an email</p>';
    $('#error').removeClass('d-none').html(errtext);
}
