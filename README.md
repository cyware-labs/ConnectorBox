
#  Connector Box - Connect to services via command line
### Table of contents

------------
- [Introduction](#Introduction)
- [Scripts provided](#Scripts)
- LeakIX
- Recon.dev
- MITRE ATT&CK
- CVE
- Github
- Verify Email
- [Usage](#Usage)
- [Contributing](#Contributing)
------------
## Introduction

Over the last decade, the cybersecurity landscape has grown exponentially along with the growth of unique cyber services and websites. These unique services give the analyst an edge in the analysis by providing information that improves speed and accuracy.

These tools and services are often web hosted and to query data we need to use their web interface, which is both taxing and inefficient when we want to analyze a large volume of data or automate workflows.

This project is aimed at giving a command line interface to these services, allowing easy integration and automation in a defender’s workflow. This repository is actively maintained by Cyware Labs, offering cutting edge services to the defender right at their command line.

It is to be noted that Cyware does not own these services and one may or may not require an api key to access them. Services that need an API key are marked below.

## Scripts
### LeakIX [No API key needed]

This project goes around the internet and finds services to index them.

#### 2 scopes
- ##### Services
In this scope, LeakIX grabs the banners from open services and make them available for search in the service scope.

- ##### Leaks
In this scope LeakIX inspects found services for weak credentials, meaning :

- No credentials
- Weak credentials, widely used by botnets ( eg: root:root, admin:admin, 123456 )

### Recon.dev [API needed]

Recon.dev collects detailed domain to IP mappings of the entire IPv4 public space resulting in a data set of over 1 Million bounty eligible targets updated every Monday. This data is provided via this script

Recon.dev uses custom built tools so each new scan is enriched to provide a deeper understanding of the indicator.

Dubbed as the 'easy to use platform for hackers to easily discover a target's assets across the entire public internet' Recon.dev, proves to be an effective platform for defenders to get a wholesome perspective.

### MITRE ATT&CK [No API needed]
MITRE ATT&CK is a globally-accessible knowledge base of adversary tactics and techniques based on real-world observations. The ATT&CK knowledge base is used as a foundation for the development of specific threat models and methodologies in the private sector, in government, and the cybersecurity product and service community.

Here, we offer the script to connect to MITRE's data via their TAXII server

### CVE [No API needed]
CVE is a [list](https://cve.mitre.org/cve/) of records—each containing an identification number, a description, and at least one public reference—for publicly known cybersecurity vulnerabilities.

CVE Records are used in numerous cybersecurity [products and services](https://cve.mitre.org/about/faqs.html#what_types_of_products_use_cve) from around the world,

including the U.S. National Vulnerability Database ([NVD](https://cve.mitre.org/about/cve_and_nvd_relationship.html)).

This script offers a command line version to access CVE's data.

### Github [No API needed]

Github is where the world codes. Github is also the place where often millions of keys are exposed by a company. This connector is aimed at giving a command line interface to search top repositories on Github via a keyword.

### Verify Email [API Key Needed]

Verify Email Service allows a user to verify any email like is the email correct, and is from valid domain and as well as it also checks out if the mailbox box really exists from which the Email came. This connector is aimed at giving a command line interface to check out the emails legitimacy.

## Usage

To use a connector, navigate to its particular repository. After navigating, if required fill the needed API keys in config.py. After filling the API keys, run connector.py to work with the connector!

## Contributing

We are constantly on the lookout for newer services/ tools to add to our repo. If you would like to contribute the easiest way to do so would be to open an issue and suggest the tool you would like.

You can also pull this repo, add your connector and submit a merge request for adding your code directly in our repo!
