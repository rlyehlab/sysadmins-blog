function getPostslist() {
    $.get('/posts.json', function(posts) {
        var list = '';
        if (posts.length > 0) {
            var i;
            list = '<p class="lead">Here are our posts:</p>';
            list += '<ul>';
            for (i = 0; i < posts.length; i++) {
                var post = posts[i]
                list += '<li>';
                list += post.publication + ') ';
                list += post.author + ' - ';
                list += '<a href="/post.html?post=' + post.id + '">' + post.title + '</a>';
                if (post.description.length > 0) {
                    var description = post.description;
                    if (description.length > 50) {
                        description = description.slice(0, 50) + '...';
                    }
                    list += ': ' + description;
                }
                list += '</li>';
            }
            list += '</ul>';
        } else {
            list = '<p class="lead"><strong>There are no posts yet, come back tomorrow!</strong></p>'
        }
        $('#postslist').html(list);
    });
}

$(document).ready(function() {
    getPostslist();
});
