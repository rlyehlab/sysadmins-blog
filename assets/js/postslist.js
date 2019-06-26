function getPostslist() {
    $('#postslist').html('<p class="lead text-center"><strong>There are no posts yet, come back tomorrow!</strong></p>');
    $.get('/posts.json', function(posts) {
        if (posts.length > 0) {
            let list;
            list = '<p class="lead text-center">Here are our posts:</p>';
            list += '<ul class="col-md-12 offset-md-1">';
            for (let i = 0; i < posts.length; i++) {
                let post = posts[i];
                list += '<li>';
                list += post.publication + ' | ';
                list += '<a href="/post.html?id=' + post.id + '">' + post.title + '</a>';
                if (post.description.length > 0) {
                    let description = post.description;
                    if (description.length > 70) {
                        description = description.slice(0, 70) + '...';
                    }
                    list += '<br /><em>' + description + '</em>';
                }
                list += '<br />by ' + post.author;
                list += '</li>';
            }
            list += '</ul>';
            $('#postslist').html(list);
        }
    });
}

$(document).ready(function() {
    getPostslist();
});
