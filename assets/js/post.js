function findGetParameter(parameterName) {
    // https://stackoverflow.com/a/5448595/3626032
    var result = null,
        tmp = [];
    var items = location.search.substr(1).split("&");
    for (var index = 0; index < items.length; index++) {
        tmp = items[index].split("=");
        if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
    }
    return result;
}

$(document).ready(function(){
    postid = findGetParameter('post').replace(/([^a-zA-Z0-9\._-])/g, '');
    console.log(postid);
    if (postid.length > 0) {
        $.ajax({
            url: '/posts/' + postid.split('.')[0] + '/' + postid,
            success: function(postdata) {
                if (postdata.length > 0) {
                    var converter = new showdown.Converter({ghCompatibleHeaderId: true}),
                    html = converter.makeHtml(postdata);
                    $('#post').html(html);
                } else {
                    // 404
                    err404();
                }
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                if (XMLHttpRequest.status == 0) {
                    alert('Check Your Network.');
                } else if (XMLHttpRequest.status == 404) {
                    err404();
                } else if (XMLHttpRequest.status == 500) {
                    err500();
                } else {
                    errUnknown(XMLHttpRequest.responseText);
                }
            }
        });
    } else {
        // 404
        err404();
    }
});
