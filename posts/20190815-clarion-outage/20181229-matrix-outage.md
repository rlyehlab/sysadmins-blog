## On July 18 we experience issues with our reverse proxy server .
* That day we were trying to add a new page for our reverse proxy. So for that process we stop the nginx service and rebuild all the ssl certificates with certbot.
For our surprise this process return with an error and the nginx service wont get up again.
* So we start to debug the problem and we find that the openssl version that was running on the VM uses a version of phyton that the Alpine SO (which runs over the VM) wasnt supported.
* The problem was originated a week ago when we upgraded the alphine packages on our scheduled system upgrade. But at that moment we didn't realize that it could be a problem.
* We tried unsuccesfully to downgrade the version of openssl.  So we restore an image backup just before the system upgrade and the already working sites start working again. At this point we call the day and return to our homes.
* The next day we try to add the new page again. This time the openssl and certbot worked just fine, but when we tried to open the port on the firewall we discovered a new problem with the ufw service. It seems that the service dissapeared as well as in the server and the repositories. 
* At this point we had a broken server unable to upgrade, so we took the drastic measure to rebuild the server with slim debian and abandon alphine for good. 
* At next day we create Aixi, new reverse proxy VM with slim debian. We migrate all the configurations on the new server and stop the old one (Clarion) to never be started again.
* Then we add the new page and it's port and everythig goes smoothly.
### Estimated downtime 1 hr.
