*Tl;Dr: you crazy!? Of course you need monitoring!! This is more of a toy tool, useful while you decide which monitoring solution implement.*

So, we have been manually updating our status site since we created it, around three or four months ago. Which is sad. For that reason, I decided it was time to do something about it and code a very simple tool that executes GET requests to given service's URL to assert whether they're alive or not. Additionally, it does simple checks over the plain text body of the response (or it will do so, soon).

[HealtChecker](https://git.rlab.be/sysadmins/healthchecker) is the python app I wrote that does this and a bit more: we have our [status](https://status.rlab.be) page hosted on [Github](https://github.com/rlyehlab/status), and the page reads a file containing a list of JSON objects having the URL of each service and its status. Therefore HealthChecker uses Github API (thanks to [PyGithub](https://github.com/PyGithub/PyGithub)) to write the checks results there.

Its a very simple tool, and requires only Python 3.7+ and two libraries: `requests` and `pygithub`.

A docker image exists in [our registry](https://git.rlab.be/sysadmins/healthchecker/container_registry) and info on how use, build or deploy is found on [its repo](https://git.rlab.be/sysadmins/healthchecker).

