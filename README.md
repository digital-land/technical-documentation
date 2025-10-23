# Technical Documentation

Technical Documentation for the planning data service.

[![Documentation Deployment](https://github.com/digital-land/technical-documentation/actions/workflows/deploy-documentation.yml/badge.svg)](https://github.com/digital-land/technical-documentation/actions/workflows/deploy-documentation.yml)

### Running Locally

This repo produces static pages which are then hosted by github but you can serve these locally to shorten the development loop.

To do this you'll need a couple of dependencies:

* node.js and npm installed locally
* make to be installed (make is used to simplify the commands to run)



### [Live Documentation](https://digital-land.github.io/technical-documentation)

This project used to use the [Tech Docs Template][template], which is a [Middleman template][mmt] that you can use to build
technical documentation using a GOV.UK style.

But we found that using  the template required knowledge of Ruby  which isn't a requirement of our project and was difficult for alll members of the team to interact with so we switched to [X-GOVUK Eleventy Plugin](https://x-govuk.github.io/govuk-eleventy-plugin/).

We have customised the layout so that edits don't need any  special knowledge other than creating and editing markdown files. To make a change simply edit the relvent document or create a new one in the docs directory and the sidenav will automatically update!

[mit]: LICENCE
[copyright]: http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/
[mmt]: https://middlemanapp.com/advanced/project_templates/
[template]: https://github.com/alphagov/tech-docs-template
