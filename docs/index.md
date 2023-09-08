# Welcome to Release Manager's documentation!

[About](modules/about.md)

## What is Release Manager

Release manager is a Django app to help you manage releases of embedded items in your Django project. A perfect example is with managing a javascript app or SPA (Single Page Application). You can control when a particular version is available, schedule it's release and even add users to "Release Groups" so they can try out pre-release versions.

It is particularly useful for cases where the front-end and back-end of your project might be on different release cycles.

## How to install

To add the "django-release-manager" package to your Django project, they should follow these steps:

1. **Activate the Virtual Environment (Optional)**: If they are using a virtual environment for their Django project (which is recommended), they should activate it. They can do this with the following command (the exact command may vary depending on their operating system and virtual environment tool):

   For `venv` on Linux/macOS:

   ```bash
   source /path/to/venv/bin/activate
   ```

   For `venv` on Windows:

   ```bash
   \path\to\venv\Scripts\activate
   ```

   For `conda`:

   ```bash
   conda activate myenv
   ```

2. **Install the Package**: They should use `pip` to install the "django-release-manager" package, as mentioned earlier:

   ```bash
   pip install django-release-manager
   ```

3. **Add the App to Django Project's `INSTALLED_APPS`**: You need to add the app provided by the "django-release-manager" package to the `INSTALLED_APPS` setting in their Django project's settings file (`settings.py`). Open the `settings.py` file and add the app's name to the `INSTALLED_APPS` list:

   ```python
   INSTALLED_APPS = [
       # ...
       'releasemanager',  # Replace 'release_manager' with the actual app name
       # ...
   ]
   ```

   Make sure to replace `'releasemanager'` with the actual name of the app provided by "django-release-manager."

4. **Run Migrations**: If the package includes database models or migrations, they should run the migrations to create the necessary database tables:

   ```bash
   python manage.py migrate
   ```

5. **Start the Django Development Server**: They can start the Django development server to run their project with the newly added package:

   ```bash
   python manage.py runserver
   ```

   This command will start the development server, and they can access their Django project with the package's features through a web browser.

By following these steps, you should be able to add the "django-release-manager" package to their Django project and use its functionality as needed.

## How to use

This app stores information about your releases in the database and renderd them into your template with tags. You need to load the tags into your template at the top of the page and then you can use it anywhere you want. Here is an example of how this would work on a page.

```
{% load release_template_tags %}

...

{% release_packages "sample_app" user=user file_types="js" %}
```

In this example, there is an Package called 'sample_app' and we want to render the 'js' files. These are all set in the Admin panel on the Release Manager records and will start to make sense as we go through them.

> **Note:** There can only be one app specified per tag but there can be multiple file_types in a comman seperated list like: "js,css,img" for example.

### Admin Interfaces

#### Packages

There are three Admin panels and a template tag included in the project. The first is defining your Packages. A Package is the main app you are building and all releases will be children of the Package. The Name is for Human readability and the Description is there for future use in rendered templates. However the most important value is the "Package key". This is the value used by the template tag to know what package to include where.

#### Releases

A release is a versioned set of files associated with the Package. Releases contain all the information that is needed to render them properly into a template.

- **Active**: Determines whether or not the release is available in production. Turning this on makes it availiable to all users on the site and will render it in everyone's session. The latest version that is active will be the default rendered version.
- **Version**: This is arbitrary but required. It there for your own tracking so it can use whatever versioning scheme you see fit.
- **Release date**: This, combined with the active state, determines what Release of the package to default to. The release who's active _and_ has the most recent release date (but not in the future) wins by default. A future data allows you to set a release time in the future to roll out a package so you can schedule it however you want.
- **Package**: Which package this release is for.
- **Files**: Here is a JSON list of the files included in the release. In the example below you can see there is a "file_type", which defines which is used by the template tag above to determine which files to render in the tag at that time and the path to the file. Options are just that, a JSON object that contains optional fields to put in the tag. In this example there is an "integrity" attribute that will be added to the HTML with the associated value.

```json
[
  { "file_type": "css", "path": "/static/css/v3.0.0/main.css" },
  { "file_type": "js", "path": "/static/js/v3.0.0/main.js", "options": { "integrity": "futureisbright!" } }
]
```

#### Release groups

Release groups are used for controlling who has access to a particular version on a particular site. This is useful for creating Beta Test groups on your site so you can give them controlled access to that specific version.

- **Name**: There to help identify the release.
- **Description**: A description of the group.
- **Members**: Who on the site is in the group.
- **Active**: whether or not the group is active. An inactive group is ignored by the template tag.
- **Sites**: which sites the user will have access to the release on.
- **Releases**: which releases the group has access to.

> **Note:** Of the seleted releases in the Releases, the one with the newest release date will be the one used. For that reason it's a good idea to make sure to only select one at a time.

## Advanced Usage

### Overriding the template

It is possible to override the main tag template with your own. It is found in

```bash
templates/releasemanager/release_template.html
```

Take a look at what is there and if you want to add functionality or change formatting for your particular use, feel free.

## TODOs

This is still a works in progress but its completely useable currently.

- More Unit Testing
- REST API
- Support for A/B testing
