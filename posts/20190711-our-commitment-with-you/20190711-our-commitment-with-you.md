# Our commitment with you

At R'lyeh Hacklab we take security and privacy very seriously and we do all in our power to protect our users' data. We encrypt all the things, deal with good security practices, we use security keys, random passwords, passwords managers and so on and so forth. Yeah, we're friggin' paranoid, intense and crazy about it.

So we decided to sign and enforce to ourselves a commitment with our users, our community. And in the way we revamped [our site](https://adm.rlab.be) and wrote the [security policy](https://adm.rlab.be/security). Additionaly, we implemented [security.txt](https://rlab.be/.well-known/security.txt) (a proposed standard which allows websites to define security policies).

We didn't do it all at once, it took time. And now we are ready to publicly anounce it :)

Here's how the signed commitment should look (and a "one-liner" for you to use):

```
sysadmins@rlyeh:~$ tmpfile="$(mktemp)"; curl -s 'https://adm.rlab.be/assets/data/sysadmins-commitment.txt' -o "$tmpfile" && cat "$tmpfile" && curl -s 'https://adm.rlab.be/assets/data/sysadmins-commitment.txt.sig' | gpg --verify - "$tmpfile"; rm "$tmpfile"
R'lyeh Hacklab Sysadmin Commitment

At R'lyeh Hacklab we take security and privacy very seriously and we do all in our power to protect our users.

I, a R'lyeh Hacklab sysadmin, fully commit to:

* Never read our users' data.
* Protect our users' data at all costs, preferring losing it than disclosing it.
* Adopt and follow good security practices.
* Be transparent with our actions and methods.
* Promote social ownership and democratic control over information, ideas, technology, and the means of communication.
* Rely on open source and open hardware whenever possible.
* Responsibly notify in any possible way if our users' data is compromised.

For which I sign this commitment.

gpg: Signature made Fri 05 Jul 2019 12:07:45 AM -03
gpg:                using EDDSA key 197A52B343BB83FF5400FA365ADA150C4928D850
gpg: Good signature from "R'lyeh Sysadmins <admin@rlab.be>" [ultimate]
Primary key fingerprint: F603 8EC8 6F6D 82AB 8C12  8D31 DAA3 DB31 FCB1 16DC
     Subkey fingerprint: 197A 52B3 43BB 83FF 5400  FA36 5ADA 150C 4928 D850
...
```

It's signed by out main key and the key of each one of us. The more we are, the more signatures will appear.

And the *security.txt* should look like this (one-liner included):

```
sysadmins@rlyeh:~$ curl -s 'https://rlab.be/.well-known/security.txt' | gpg --decrypt -
Canonical: https://rlab.be/.well-known/security.txt
Policy: https://adm.rlab.be/security
Preferred-Languages: es, en
Contact: mailto:admin@rlab.be
Encryption: openpgp4fpr:f6038ec86f6d82ab8c128d31daa3db31fcb116dc
Acknowledgments: https://adm.rlab.be/security/hof
gpg: Signature made Wed 20 Mar 2019 02:19:22 AM -03
gpg:                using EDDSA key 197A52B343BB83FF5400FA365ADA150C4928D850
gpg: Good signature from "R'lyeh Sysadmins <admin@rlab.be>" [ultimate]
Primary key fingerprint: F603 8EC8 6F6D 82AB 8C12  8D31 DAA3 DB31 FCB1 16DC
     Subkey fingerprint: 197A 52B3 43BB 83FF 5400  FA36 5ADA 150C 4928 D850
```

Of course YMMV and you will probably get a message like `WARNING: This key is not certified with a trusted signature!` which means that you haven't signed the key in question, but the important message is `Good signature from ...`. You can find our keys in the [first post](/post.html?id=20181009-about-us#who-you-gonna-call).

So, there's that. I hope you are as happy as we are with this. Feel free to get in touch with us if you have any questions whatsoever.

Cheers!!

**-- R'lyeh Sysadmins**

