# Release Manager

A Release Manager for Embedded Apps in your website, such as an SPA.

## User Story

_As a developer I want to control the release version of my Single Page Application (SPA) so I can make it available to who on what site that I want._

This user story drives this project's development and explains it's goals. In the project we've been working on, we have two different development streams for Front-End and Back-End. This app project is there to make sure they are decoupled while giving us the control to make available any version we wish, when we want.

We do this by building every 'package' to a cloud store/CDV (like S3/Cloudfront) with a unique path for each release. The path contains the "name" of the release (typically a verion number) and the locaiton where to find it. As a new version of the package is successfully built by the CI/CD pipeline, a version is registered with the Django Project via an API call. Then the developer can go into the Django Project and change which version is available to the users. It can also make versions available to only certian users on certian sites.

To learn more about how it works, check out the link below and the docs will show you how to set your packages up.

## Docs

Docs can be found here [docs/index.md](https://github.com/renderbox/django-release-manager/blob/main/docs/index.md) file.

## Status

[![Python Test](https://github.com/renderbox/django-release-manager/actions/workflows/python-test.yml/badge.svg)](https://github.com/renderbox/django-release-manager/actions/workflows/python-test.yml)

[![Generate Docs](https://github.com/renderbox/django-release-manager/actions/workflows/docs.yml/badge.svg)](https://github.com/renderbox/django-release-manager/actions/workflows/docs.yml)

[![Upload Python Package](https://github.com/renderbox/django-release-manager/actions/workflows/python-publish.yml/badge.svg)](https://github.com/renderbox/django-release-manager/actions/workflows/python-publish.yml)
