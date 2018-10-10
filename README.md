# R'lyeh Sysadmins Blog

This blog allows us to exteriorize our madness to the outside world, and maybe
share usefull information.

It works on **FemtoBlog**, a simple *blogging platform* (if it can be called like
that) that empowers markdown blogging.

## How to Post

FemtoBlog needs two things to display a post: the post per se and its
metadata.

### The Post

To create a post, simply write your thoughts in a markdown file and name it
whatever you want. However, to keep an order of things, and to keep all of the
post's assets along, a directory with the same name is used.

There's no strict rule for naming, except that it can only contain alphanumeric
characters, `-` and `_`. As a convention, it's preferred to name it with
the publication date first followed by a slugyfied title, so that it's easier
to view, find and read posts directly through git.

Example: for a post named *A Nice Post* created on 9 October, 2018, the name
would be `20181009-a-nice-post.md`, and it would be located at
`posts/20181009-a-nice-post/20181009-a-nice-post.md`.  
The *post id* is the file name without the `.md` extension, which for the
example above would be `20181009-a-nice-post`.

All of the post assets, such as pictures, videos, files or whatever, should be
located in the same dir, optionally in subdirectories as wanted (there's no
further criteria).

### The Posts Metadata File

There's no server API, no directory listing and no database here, so there's no
way to actually retrieve the posts list (it could be done using GH API, but I
didn't want to be tied to GH), so I opted for a simple metadata file:
`posts.json`.  
The file is a JSON list of JSON objects that defines and order the posts, so
that the first post is the first object, which should be the newest one (this
is reverse date ordering).  
The object has the following values:

* `id`: the post ID, which can be any string containing only alphanumeric
  characters, `-` and `_`.
* `title` the post title, which should conveniently be shorter than 25
  characters (but there's no real limit).
* `author`: the post author or author list, comma-separated.
* `description`: a short post description which should be shorter than 50
  characters and is ellipsed if it's longer.
* `publication`: the post publication date, preferrably in ISO8601
  (YYYY-MM-DD) format but it will be displayed as is.
* `modification`: the post modification date, preferrably in ISO8601
  (YYYY-MM-DD) format but it will be displayed as is (currently not
  implemented).

Continuing with the example, the JSON object for the post would be:

```json
{
    "id": "20181009-a-nice-post",
    "title": "A Nice Post",
    "author": "Me",
    "description": "A very nice post about something",
    "publication": "2018-10-09",
    "modification": "2018-10-09"
}
```

# FemtoBlog

A tini tiny *blogging platform* based on Bootstrap, JQuery and
[ShowdownJS](https://github.com/showdownjs/showdown).

It's based on the concept of simplicity and the wonder of writing Markdown.
Comprised by just two HTML files (the posts index and a post template), it uses
JQuery/Ajax to retrieve the post content and ShowdownJS to convert it to HTML
effortlessly.

## Inner workings

The index shows a dinamically generated posts list, which is done parsing the
posts metadata file, a JSON file containing a JSON list of JSON objects (you
got it, right?). This list is displayed in the DOM element with id
`postslist`, and is done by [postslist.js](assets/js/postslist.js).  
The order of the posts is determined by the order of the
elements in the list. A logical order is the chronological one: to keep the
newest post first, and so on.

The index listing will produce a link in the form of
`/post.html?post=some-post-id`. Then the post page template checks the GET
parameter `post` and tries to retrieve the corresponding post content file,
which should be `/posts/some-post-id/some-post-id.md`. This is done by
[post.js](assets/js/post.js). If it's found, it's parsed with ShowdownJS and
displayed in the DOM element with the id `post`. If something goes bad, an
error is shown, displaying the error message in the DOM element with id
`error`. This is done by [errors.js](assets/js/errors.js).

So basically, the minimal HTML files would be:

*index.html*:

```html
<body>
    <div id="postslist">
    </div>
    <script src="/assets/js/postslist.js" defer></script>
</body>
```

*post.html*:

```html
<body>
    <div id="post">
    </div>
    <div id="error">
    </div>
    <script src="/assets/js/errors.js"></script>
    <script src="/assets/js/post.js" defer></script>
</body>
```

# License

[![CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/) All contents are licensed under *[Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)*.

