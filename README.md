## Introduction

TBD

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

## License

Like all my hobby projects, this is Free Software covered by GPLv3 license.