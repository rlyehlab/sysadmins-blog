## On december 6 20:30 riot server stop working.
* We check the VM [Samantha] and the root disk where full.
* We stop and start the VM, and delete old containers versions
* then we deploy a fresh container
* This get riot working but we still can't send any messages.
* So we check on the Reverse Proxy [clarion] and it's also has the root disk full due login. We delete the logs and stop the log deamon
* Then riot start to work properly.
### Restored at December 7 14:40.
### Estimated downtime 18 hrs.
