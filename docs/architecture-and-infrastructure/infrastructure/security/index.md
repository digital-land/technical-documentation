# Infrastructure Security

## Overview

To help secure the infrastructure Planning Data Service, the team have adopted the recommendations of certain security 
frameworks and employed continuous compliance and monitoring tools to automate the significant task of understanding the security posture
of our hosting estate.

## Frameworks

The following frameworks have been adopted.

### CIS AWS Benchmark

#### Description

The Center for Internet Security (CIS) AWS Foundations Benchmark serves as a set of security configuration best practices for AWS. These industry-accepted best practices provide you with clear, step-by-step implementation and assessment procedures. Ranging from operating systems to cloud services and network devices, the controls in this benchmark help you protect specific systems that an organization uses.

#### Monitoring approach

Automatic via AWS Security Hub tool.

### NCSC Cloud security guidance

#### Description

The UK Government's National Cyber Security Centre have provided [guidance on how to choose, configure and use cloud services securely](https://www.ncsc.gov.uk/collection/cloud). The  guidance also contains [14 principles](https://www.ncsc.gov.uk/collection/cloud/the-cloud-security-principles) to instruct technical implementations.

#### Monitoring approach

Manual via internal security reviews.

### GDS Service Standard

#### Description

[Point 9 of the Service Standard](https://www.gov.uk/service-manual/service-standard/point-9-create-a-secure-service) provided by UK Government Digital Services instructs service owners to "Create a secure service which protects users’ privacy".

#### Monitoring approach

Manual via internal service reviews.

### AWS Well-Architected Framework - Security foundations

#### Description

The [security pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/security.html) of the AWS Well-Architected framework describes how to take advantage of cloud technologies to protect data, systems, and assets in a way that can improve your security posture.

We have chosen to apply the seven principles from this framework:

 * Security foundations
 * Identity and access management
 * Detection
 * Infrastructure protection
 * Data protection
 * Incident response
 * Application security

#### Monitoring approach

Automatic via AWS Well-Architected tool.


## Tools

### AWS Security Hub

See https://aws.amazon.com/security-hub/ 

Automates security best practice checks, aggregates security alerts into a single place and format, and provides insight into the overall security posture across AWS accounts.  Chargeable service

### AWS GuardDuty

See https://aws.amazon.com/guardduty/

An AWS service which protects AWS accounts, workloads, and data with intelligent threat detection. When GuardDuty and Security Hub are enabled in the same account within the same AWS Region, GuardDuty starts sending all the generated findings to Security Hub. Chargeable service.

### AWS Well-Architected tool

See https://aws.amazon.com/well-architected-tool/

Provides a trusted framework to evaluate cloud architecture and implement designs that scale over time.  Free to use.

### Future

Tools which could be considered for adoption in future include:

 * [AWS Inspector](https://aws.amazon.com/inspector/?nc=sn&loc=0)
 * [AWS Detective](https://aws.amazon.com/detective/)