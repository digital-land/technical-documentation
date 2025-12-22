---
title: Solution design - DNS
---

## Overview

The Domain Name System (DNS) setup for the planning data service involves the delegation of the planning subdomain from the data.gov.uk domain which is managed by GDS (Government Digitial Service).  A name server lookup for the planning name server record reveals the following:

```shell
$ nslookup -q=ns planning.data.gov.uk
Server:		fe80::d686:60ff:fe40:eb3d%15
Address:	fe80::d686:60ff:fe40:eb3d%15#53

Non-authoritative answer:
planning.data.gov.uk	nameserver = ns-519.awsdns-00.net.
planning.data.gov.uk	nameserver = ns-1995.awsdns-57.co.uk.
planning.data.gov.uk	nameserver = ns-79.awsdns-09.com.
planning.data.gov.uk	nameserver = ns-1442.awsdns-52.org.
```

The four nameserver records returned refer to the planning.data.gov.uk Route 53 zone in our production AWS account.  From that zone, further delegations have been made for our non-production environments:

 * staging.planning.data.gov.uk
 * development.planning.data.gov.uk

The delegations correspond to the Route 53 zones in the staging and development AWS accounts.

## DNS Delegation Diagram

![DNS Delegation](/images/dns.drawio.png)