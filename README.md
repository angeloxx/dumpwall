## Introduction

In these days ("these" starts yesterday and ends between when singularity comes and the end of the world) I'm planning to move from an old-fashion security model based on old Cisco devices to a new setup based on Sonicwall solution. The first difference between these two solutions (without additional software) is that Cisco can be managed using CLI and the configuration file is a list of instruction; if you manage configuration using a svn/git repository, you can evaluate the difference between configuration easily because they are text files. Sonicwall uses instead a web configuration that can be easier to manage (I'm not so sure because you need more steps to replicate a configuration) but less easy to compare because the configuration export file is a binary and cryptic file.

This dumpwall script will dump the configuration export file to a readable format (text, text expanded and html) that can be paired and saved with the original exp file on a git/svn repo. I'm working on this tool in my spare time and adding features when it is possible; the final target is to convert the whole export file but my experience is limited to the TZ2xx devices. If someone wants to help me, can send me a exp file of a different model with some screenshots of configuration pages.

## Current supported commands

```
dumpwall.py -i sonicwall-TZ_210-5_9_0_4-127o.exp
interface id '0' name 'X0' type 'Physical interface'
interface id '1' name 'X1' type 'Physical interface'
interface id '2' name 'X2' type 'Physical interface'
interface id '3' name 'X3' type 'Physical interface' portshield with 'X0'
interface id '4' name 'X4' type 'Physical interface' portshield with 'X0'
interface id '5' name 'X5' type 'Physical interface' portshield with 'X0'
interface id '6' name 'X6' type 'Physical interface' portshield with 'X0'
interface id '7' name 'U0' type 'Unknown' portshield with 'X0'
interface id '8' name 'U1' type 'Unknown' portshield with 'X0'
interface id '9' name 'X0:V90' type 'Virtual interface' vlan '90'
interface id '10' name 'X0:V100' type 'Virtual interface' vlan '100'
```

## Status

This program is work in progress, I'm planning to switch to Cisco to Sonicwall and I'm writing 
this utility to create a dump (HTML report and txt) of saved configuration that can be printed
and compared with diff to obtain differences between versions.

Me (and this software) is not associated, related or sponsored by Sonicwall or Dell. Use it at
your own risk.

## License

Like all my hobby projects, this is Free Software covered by GPLv3 license.