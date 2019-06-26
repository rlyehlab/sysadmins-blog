function findGetParameter(parameterName) {
    // Throws URIError
    // https://stackoverflow.com/a/5448595/3626032
    let result = null,
        tmp = [];
    let items = location.search.substr(1).split("&");
    for (let index = 0; index < items.length; index++) {
        tmp = items[index].split("=");
        if (tmp[0] === parameterName) {
            result = decodeURIComponent(tmp[1]);
            break;
        }
    }
    return result;
}

function loadPost() {
    let postid = null;

    try {
         postid = findGetParameter('id');
    } catch(e) {
        console.error(
            'Exception caught trying to find the "id" parameter: '
            + e.toLocaleString()
        );
        errUnknown("(message in your browser's console)");
    }

    if (postid) {
        // Filter unwanted characters
        postid = postid.replace(/([^a-zA-Z0-9_\-])/g, '');
    }

    if (!postid) {
        err404();
        return;
    }

    $.get('/posts/' + postid + '/' + postid + '.md?cache=20190626', function(postdata) {
        if (postdata.length > 0) {
            let converter = new showdown.Converter({ghCompatibleHeaderId: true}),
            html = converter.makeHtml(postdata);
            $('#post').html(html);
            $('#error').addClass('d-none').html('');
        }
    }).fail(function() {
        err404();
    });
}

$(document).ready(function(){
    loadPost();
});
