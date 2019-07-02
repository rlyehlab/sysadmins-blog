Both Github and Gitlab automatically generates .tar.gz and .zip packages (and some others) of the repository when a release or pre-release is created under *releases*. However, these packages are not signed! The tag might be signed but if a user downloads one of those, there's no true certification of its content, rather than pure trust on Github/Gitlab which is of course not correct.

However, you can edit a release after it's generated to upload files, and this is how you upload signature files for those packages (as I usually do). But, to sign them, you need to first download them and, of course, verify them! Otherwise, you'll be signing your trust to Github/Gitlab without checking!

I will be using a tool I created to do recursive blake2 checksums called [b2rsum](https://github.com/HacKanCuBa/b2rsum). You can use any other tool that does the same if you want.

To properly verify those packages, do the following:

1. Create a temporal directory to store all files, lets call it `/tmp/check`.
2. Copy your source code to a subdirectory there: `cp -r ~/code/myproject /tmp/check/orig`.
3. Remove files that aren't used (such as compiled files and gitignored files) and the .git directory in `/tmp/check/orig`. This is to make verification easier with no false positives.
4. Go into the directory and create a checksum file:  
```
cd /tmp/check/orig
b2rsum -o .
```
5. Go back up and download a Github/Gitlab package, then extract it:  
```
cd /tmp/check
# For Github:
wget -O {package}.tar.gz https://github.com/{user}/{project}/archive/{tag}.tar.gz
# For Gitlab
wget -O {package}.tag.gz https://gitlab.com/{user}/{project}/-/archive/{tag}/{project}-{tag}.tar.gz
tar -xf {package}.tar.gz
```
6. Go into the extracted directory and verify that all the files that are supposed to be there, are there. And that they are the exact same as intended:  
```
cd /tmp/check/{project-dir}
b2rsum -c /tmp/check/orig/BLAKE2SUMS
```
7. Create a checksums file for this directory: `b2rsum -o .`.
8. Go into the *orig* dir and check against that checksums file that no extra file was added to the package:  
```
cd /tmp/check/orig
b2rsum /tmp/check/{project-dir}/BLAKE2SUMS
```
9. If all checks went well, now the package can be signed. Discard the extracted dir:
```
cd /tmp/check
rm -rf {project-dir}
gpg --sign --detach-sign --interactive --verbose --digest-algo sha512 -o {package}.tar.gz.sig {package}.tar.gz
```
10. That's it! Repeat for the other packages (.zip, .tar.bz, etc) and upload the signatures to the release.
11. Optionally, check that all files are correct by downloading signatures and packages and verifying them all.


*This post was originally published as a [Gist](https://gist.github.com/HacKanCuBa/6fabded3565853adebf3dd140e72d33e)*.

