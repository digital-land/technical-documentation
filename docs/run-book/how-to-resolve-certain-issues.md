---
title: How to resolve certain issues
---

This outlines the steps and processes to take for many issues the platform may experience.

1. [If the service is slow](#1.if-the-service-is-slow)
2. [If the service suffers an outage](#2.if-the-service-suffers-an-outage)
3. [If a deployment fails](#3.if-a-deployment-fails)
4. [If DNS or the CDN is the issue](#4.-if-dns-or-the-cdn-is-the-issue)
5. [Handling critical alerts](#5.-handling-critical-alerts)
6. [Restoring backups](#6.-restoring-backups)
7. [If there is a security breach](#7.-if-there-is-a-security-breach)
8. [Emergency response checklist](#8.-emergency-response-checklist)
9. [Summary of common failure scenarios](#9.-summary-of-common-failure-scenarios)
10. [Worst case scenario](#10.-worst-case-scenario)

## 1. If the service is slow

1. Check if the cache is warmed up  
   1. If not, warm it up  
2. Check if servers are running out of resources  
   1. If they are, increase the number of nodes in the cluster to 15  
   2. Turn off scaling down  
3. Check if database read replicas are running out of CPU  
   1. Increase the number of read replicas to 15  
   2. Check if any queries are locking the database

### Locking queries

**Warning: This may not be possible as not everyone has database access.**

1. Identify if there are locking queries:
   - Connect to the database and run:
     ```
     SELECT pid, usename, query, state, wait_event_type, wait_event, now() - query_start AS duration
     FROM pg_stat_activity
     WHERE wait_event_type = 'Lock';
     ```
2. Review the blocking queries:
   - To find blocking processes:
     ```
     SELECT blocked.pid AS blocked_pid, blocked.query AS blocked_query,
            blocking.pid AS blocking_pid, blocking.query AS blocking_query
     FROM pg_stat_activity blocked
     JOIN pg_locks blocked_locks ON blocked.pid = blocked_locks.pid
     JOIN pg_locks blocking_locks
       ON blocked_locks.locktype = blocking_locks.locktype
      AND blocked_locks.database IS NOT DISTINCT FROM blocking_locks.database
      AND blocked_locks.relation IS NOT DISTINCT FROM blocking_locks.relation
      AND blocked_locks.page IS NOT DISTINCT FROM blocking_locks.page
      AND blocked_locks.tuple IS NOT DISTINCT FROM blocking_locks.tuple
      AND blocked_locks.virtualxid IS NOT DISTINCT FROM blocking_locks.virtualxid
      AND blocked_locks.transactionid IS NOT DISTINCT FROM blocking_locks.transactionid
      AND blocked_locks.classid IS NOT DISTINCT FROM blocking_locks.classid
      AND blocked_locks.objid IS NOT DISTINCT FROM blocking_locks.objid
      AND blocked_locks.objsubid IS NOT DISTINCT FROM blocking_locks.objsubid
     JOIN pg_stat_activity blocking ON blocking_locks.pid = blocking.pid
     WHERE NOT blocked_locks.granted;
     ```
3. If critical services are impacted:
   - Kill the blocking process carefully:
     ```
     SELECT pg_terminate_backend(<blocking_pid>);
     ```
4. Investigate and resolve the root cause:
   - Common causes:
     - Long-running transactions
     - Missing indexes
     - Inefficient queries
   - Actionable solutions:
     - Optimise queries
     - Add appropriate indexes
     - Review application transaction management


## 2. If the service suffers an outage

1. Confirm outage
   - Check uptime monitoring alerts
   - Try accessing service from different networks (e.g., mobile hotspot)
2. Investigate:
   - Check AWS Cloud status (e.g., EC2, RDS, ALB services)
   - Check ECS cluster status
   - Check database availability (connect manually if needed)
   - Check DNS records for unexpected changes
3. Actions:
   - Restart ECS services manually
   - Restart RDS database if needed
   - Check load balancer health checks
4. Communication:
   - Immediately send Incident Alert to team (see Communication Template)
5. If recovery not possible:
   - Move to DR (Disaster Recovery) plan (TBC if available)

## 3. If a deployment fails

1. Confirm the deployment has caused the issue:
   - Look for increase in 5xx errors after deployment
   - Look for rollback triggers in ECS/CI logs
2. Actions:
   - Rollback ECS service to previous task definition
     - In AWS Console → ECS → Service → Deployments → Force New Deployment
   - Rollback database changes manually if migrations were deployed (confirm with Dev lead)
3. Validate:
   - Confirm service is healthy (low error rates, normal load times)
4. Communication:
   - Notify team and log rollback in incident document
5. Post-incident:
   - Document the failed deployment and reason
   - Open tickets for code fixes

## 4. If DNS or the CDN is the issue

1. Confirm issue:
   - Use `dig`, `nslookup`, or `whois` to check DNS health
   - Check CDN error rates (e.g., 5xx from CloudFront)
2. Actions:
   - If DNS record is wrong or missing:
     - Update or restore DNS A/AAAA/CNAME record
     - Use Route53 or domain registrar as necessary
   - If CDN cache corrupted:
     - Invalidate caches immediately
   - If SSL certificate expired:
     - Renew certificate manually
3. Validate:
   - Confirm site reachable via browser and `curl`
4. Communication:
   - Inform team of DNS/CDN resolution

**NOTE: THIS MAY TAKE UP TO 24 HOURS TO PROPAGATE**

## 5. Handling critical alerts

1. Triage:
   - Review the alert (metrics, thresholds, graphs)
   - Classify: Critical / Warning / False Positive
2. Actions:
   - If Critical:
     - Assign a responder immediately
     - Open incident channel
   - If Warning:
     - Monitor closely, prepare pre-emptive scaling
   - If False Positive:
     - Adjust alert rule after incident (never during active incident)
3. Communication:
   - Update the team every 15 minutes
   - Escalate if no resolution in 30 minutes
4. Close alert:
   - Confirm metrics return to normal

## 6. Restoring backups

1. Database Backup:
   - Confirm latest snapshot exists (RDS snapshots auto-scheduled)
   - Manual trigger:
     - RDS → Databases → Snapshots → Create snapshot
2. Restore Procedure:
   - For Database:
     - Create new RDS instance from snapshot
     - Redirect application to use new endpoint
   - For Cache:
     - Invalidate DNS Cache
3. Validation:
   - Run application smoke tests
   - Monitor database connections and error logs

## 7. If there is a security breach

1. Detection:
   - Look for suspicious logs (login attempts, API usage)
   - Confirm if known vulnerability or 0-day
2. Actions:
   - Revoke exposed API keys / credentials immediately
   - Rotate passwords and secrets (AWS Secrets Manager)
   - Update firewall or WAF rules to block IP/ranges
3. Communication:
   - Notify internal security team
   - Escalate to AWS support if needed
4. Documentation:
   - Keep detailed timeline of events
   - Post-incident review required within 24 hours

## 8. Emergency response checklist

- [ ] Confirm incident severity (minor slowdown vs major outage)
- [ ] Check application logs and system metrics
- [ ] Validate if cache is warm
- [ ] Check ECS cluster CPU/memory usage
- [ ] Check read replicas CPU usage
- [ ] Identify if any database locks exist
- [ ] If database locks are found:
  - [ ] Identify and terminate blocking queries if needed
- [ ] Scale up:
  - [ ] ECS nodes to 15 if needed
  - [ ] Read replicas to 15 if needed
- [ ] Disable any automatic scaling down temporarily
- [ ] Post-incident:
  - [ ] Document the root cause
  - [ ] Add any lessons learned to the retrospective
  - [ ] Implement longer-term fixes (optimisation, scaling policies)

## 9. Summary of common failure scenarios

| Symptom                         | Likely Cause                                | First Action                                   |
|----------------------------------|---------------------------------------------|------------------------------------------------|
| High response times             | Cache cold / missing                       | Run cache warm-up script                      |
| ECS cluster CPU over 80%         | Under-provisioned nodes                    | Increase ECS nodes and turn off scaling down  |
| Database CPU over 80% on reads   | Too few read replicas                      | Add more read replicas (scale to 15)          |
| Queries stuck or timeout errors  | Database lock contention                   | Find and terminate blocking queries           |
| 502/504 Gateway errors           | Application crash or overload              | Check ECS cluster health, restart services if needed |
| High database connection counts | Inefficient connection pooling             | Optimise application DB pooling configuration |
| Long-running transactions       | Application bug or misuse                  | Investigate slow transactions and resolve     |
| Sudden surge in traffic          | External factors (e.g., social media post)  | Scale up ECS cluster nodes and read replicas  |
| High memory usage on nodes       | Memory leaks or large requests             | Redeploy services, investigate logs           |
| ECS service restarts repeatedly  | Crash loops due to bad deployment or config | Roll back to last stable deployment           |
| High error rate (5xx responses)  | API backend issues                         | Check backend service health and restart if necessary |
| Cache hit rate drops             | Cache invalidation or config error         | Warm cache again and investigate eviction policy |
| Increased latency on single endpoint | Slow DB query or N+1 queries          | Profile queries and optimise, add indexes     |
| Database disk IO spikes          | Heavy queries / missing indexes            | Optimise slow queries, review indexing        |
| Unable to scale ECS nodes        | AWS resource limit hit                     | Raise AWS service limits via console          |
| ECS CPU utilisation 100% even after scaling | Application bottleneck / bad code  | Profile application, identify bottlenecks     |
| Database storage almost full     | Log accumulation or bloated tables         | Clear old data, archive, or increase storage  |
| Very slow cold start on new containers | Large container images                  | Optimise Dockerfile, reduce image size        |
| TLS/SSL errors reported by clients | Certificate expiry or misconfiguration   | Check certificate validity and update         |
| High network error rates         | Load balancer issues or bad deployments    | Check ALB/NLB health and ECS task networking  |

## 10. Worst case scenario

If none of the above works. Do the following, after each step, monitor for 5 minutes before doing anything:

1. Force a database restart
2. Force restart the tasks/nodes
3. Invalidate the cache