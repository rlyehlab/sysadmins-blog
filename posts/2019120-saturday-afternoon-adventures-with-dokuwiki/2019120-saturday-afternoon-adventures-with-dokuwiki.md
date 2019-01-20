# Saturday afternoon adventures with Dokuwiki

Yesterday, while copying our current wiki service
([dokuwiki](https://www.dokuwiki.org/)) to create the Antifa GLUG
(*link pending*) wiki, we discovered some things related to that service:

1. The wiki was outdated, so we emailed the docker maintainer to upgrade its
   build.
2. docker-compose has some not-so-funny behaviour when you try to `up` a
   service named the same as one that's already up: errors everywhere!.
3. The wiki was storing passwords in salted MD5 format!! REALLY!? WTF.

## Let's dig a bit deeper.

1. There's not much to say about the first point, except
that a typo in the Dockerfile caused that the latest build actually build the
previous dokuwiki version. Nothing to do, but to email the mainteiner and hope
she/he updates soon. Or to fork it and mantain it by ourselfs. We'll see what
happens.

2. We created a subdirectory in our VM and copyied the wiki service dir to it.
But then, docker-copose took it as the service has the exact same name as
the other one! Because docker-compose generates containters names as *<parent
dir>\_<service name>\_1`*. One would think that perhaps it will detect that other
one exists and will use \_2 or whatsoever... but no! it won't! it will just
wonderfully crash :)
Solution? Rename the parent dir and move on.

3. This really anoyed us. We read the documentation and choose *bcrypt* as it
was the best choice available. However, until every user manually updates
its password, the hashing won't change. So we took a more active aproach: reset
every users passwords to a random one and let them generate a new one. We tried
to email every user its own reset link, but in the process discovered that our
mail server imposed a really low burst email rate. So we couldn't complete this
task, and instead choose to announce the situation at our Telegram groups. We
know, lazy way out.

Finally, we upgraded some VMs and servers and stuff. The usual R'lyeh
sysadmins' Saturday afternoon. Yay!

