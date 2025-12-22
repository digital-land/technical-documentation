---
title: Google Analytics User Tracking Documentation
---

## Overview

This document outlines how we use Google Analytics to track user interactions on our GOV.UK services. Google Analytics helps us gather insights into user behaviour, measure website performance, and improve the overall user experience.

## Prerequisites

Before implementing Google Analytics tracking, ensure that:

- The GOV.UK cookie banner is implemented correctly and adheres to the [Planning Data Service Cookie Policy](https://submit.planning.data.gov.uk/cookies#google-analytics-cookies-optional).
- Users have explicitly consented to analytics cookies.
- The appropriate Google Analytics property is configured and permissions are correctly assigned.

## Enabling Google Analytics Tracking

### Step 1: Implement Google Tag Manager (GTM)

We use **Google Tag Manager (GTM)** to manage and deploy Google Analytics tracking scripts efficiently. This ensures that tracking is only enabled after a user has accepted analytics cookies.

#### Steps to set up GTM:

1. Log in to **Google Tag Manager** and navigate to your **GOV.UK service container**.
2. Create a new tag for Google Analytics:
   - Choose **Google Analytics: GA4 Configuration**.
   - Enter the **Measurement ID** (found in your GA4 property settings).
   - Set the **trigger** to fire only when analytics cookies have been accepted.
3. Publish the changes.

### Step 2: Configure Google Analytics Events

To track user interactions, set up Google Analytics **events** in GTM.

#### Example event setup:

To track when users submit a form:

1. In **GTM**, create a new event tag.
2. Select **Google Analytics: GA4 Event**.
3. Enter the event name (e.g., `form_submission`).
4. Set parameters such as `form_id` or `page_path`.
5. Configure the trigger to fire on form submissions.
6. Save and publish the changes.

## Ensuring Cookie Consent Compliance

### GOV.UK Cookie Banner Requirement

Google Analytics tracking **must only be enabled if a user has explicitly opted in via the GOV.UK cookie banner**.

#### Key implementation points:

- The default state of analytics cookies should be **disabled** until consent is given.
- Consent preferences should be stored and respected across user sessions.
- The analytics script should only execute if consent is granted.

### Example Consent Implementation

Using **GOV.UK Frontend**, the following approach ensures compliance:

```javascript
if (GOVUK.cookie("cookies_policy") === "true") {
  // Load Google Analytics script dynamically
  var script = document.createElement("script");
  script.src = "https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX";
  script.async = true;
  document.head.appendChild(script);

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    dataLayer.push(arguments);
  }
  gtag("js", new Date());
  gtag("config", "G-XXXXXXXXXX", { anonymize_ip: true });
}
```

## Data Privacy and Anonymisation

To align with **GDPR** and **GOV.UK privacy policies**, the following measures are taken:

- **IP anonymisation** is enabled (`anonymize_ip` flag in GA4 settings).
- Personal data (e.g., names, emails) should **never** be sent to Google Analytics.
- Data retention settings are configured to store data for the minimum period required.

## Testing and Validation

Before deploying changes, validate Google Analytics tracking:

1. Use **Google Tag Assistant** to check if the tags fire correctly.
2. Enable **Google Analytics Debug Mode** to verify event tracking.
3. Test cookie banner functionality to ensure compliance.

## Monitoring and Reporting

Analytics reports can be accessed via the **Google Analytics dashboard**. Key metrics include:

- **Pageviews**: Number of times a page is loaded.
- **Sessions**: User visits within a given timeframe.
- **Events**: User interactions such as form submissions, button clicks.
- **User Demographics**: Aggregated insights (if consented).

For advanced reporting, **Looker Studio** can be used to create custom dashboards.

## Conclusion

Google Analytics tracking is a valuable tool for understanding user behaviour but must be implemented responsibly. Adhering to **GOV.UK cookie policies** and **GDPR compliance** ensures transparency and user trust. Always verify consent before enabling tracking and continuously monitor compliance.

For further guidance, refer to [Planning Data Service Cookie Policy](https://submit.planning.data.gov.uk/cookies#google-analytics-cookies-optional).
