# Welcome to Release Manager's documentation!

[About](modules/about.md)

## What is Release Manager

Release manager is a Django app to help you manage releases of embedded items in your Django project. A perfect example is with managing a javascript app or SPA (Single Page Application). You can control when a particular version is available, schedule it's release and even add users to "Release Groups" so they can try out pre-release versions.

It is particularly useful for cases where the front-end and back-end of your project might be on different release cycles.

## How to install

To add the "django-release-manager" package to your Django project, follow these steps:

1. **Activate the Virtual Environment (Optional)**: If you are using a virtual environment for your Django project (which is recommended), you should activate it. You can do this with the following command (the exact command may vary depending on their operating system and virtual environment tool):

   For `venv` on Linux/macOS:

   ```bash
   source /path/to/venv/bin/activate
   ```

   For `venv` on Windows:

   ```bash
   \path\to\venv\Scripts\activate
   ```

2. **Install the Package**: Use `pip` to install the "django-release-manager" package, as mentioned earlier:

   ```bash
   pip install django-release-manager
   ```

3. **Add the App to Django Project's `INSTALLED_APPS`**: You need to add the app provided by the "django-release-manager" package to the `INSTALLED_APPS` setting in their Django project's settings file (`settings.py`). Open the `settings.py` file and add the app's name to the `INSTALLED_APPS` list:

   ```python
   INSTALLED_APPS = [
       # ...
       'releasemanager',
       # ...
   ]
   ```

4. **Add the URLs to Django Project's urls.py** (optional): If you want to use the views and/or API from the release manager you will need to add the urls in the "django-release-manager" package to your project's urls.py. Feel free to name the base URL how you wish.

   **_Views_**

   ```python
   urlpatterns = [
      ...
      path("releasemanager/", include("releasemanager.urls") ),
      ...
   ]
   ```

   **_API_**

   ```python
   urlpatterns = [
      ...
      path("api/releasemanager/", include("releasemanager.api.urls") ),
      ...
   ]
   ```

5. **Run Migrations**: Run the migrations to create the necessary database tables:

   ```bash
   python manage.py migrate
   ```

6. **Start the Django Development Server**: Run your project with the newly added package:

   ```bash
   python manage.py runserver
   ```

## How to use

### Configuration

The first step is to define your package in your settings.py file.

```python
# Django Release Manager Settings
RM_PACKAGES = {
    "basic": {"name": "Basic", "description": "Basic package"},
    "advanced": {
        "name": "Advanced",
        "description": "Advanced package with more features",
    },
}
```

The packages themselves are defined in the settings rather than as a model for a couple reasons.

- Simplicity: Defining packages directly in your settings is straightforward and can be easily accessed throughout your application without needing database queries.
- Performance: Since the data is loaded into memory when the application starts, accessing this information is fast and doesn't involve the overhead of an extra database call.
- Stability: Since the packages are not going to change often or only change with new releases of the application, keeping them in the settings makes it easier to manage through version control.

### Usage in Templates

This app stores information about your releases in the database and renders the URL to the files into your template using tags. You need to include the tag library in your template at the top of the page and then you can use it anywhere you want. Here is an example of how this would work on a page.

Include this at the top of your template:

```python
{% load release_template_tags %}
```

Now you can put this tag wherever is appropriate in your template:

```python
{% release_packages "basic" user=user file_types="js" %}
```

In this example, we are managing a Package called 'basic' and we want to render the 'js' files. Controls for which version of the script to include is set in the Admin panel on the Release Manager record. What the example above will do is find the latest release version of the package, "basic", and render a link for all the "js" files included in the package.

How this all works behind the scenes will be explained in the next steps.

> **Note:** There can only be one package specified in a tag at a time but there can be multiple file_types in a comman seperated list like: "js,css,img" for example.

### Admin Interfaces

#### Packages

There are three Admin panels and a template tag included in the project. The first is defining your Packages. A Package is the main app you are building and all releases will be children of the Package. The Name is for Human readability and the Description is there for future use in rendered templates. However the most important value is the "Package key". This is the value used by the template tag to know what package we are working with in that tag.

#### Releases

A release is a versioned collection of files associated with the Package. Releases contain all the information that is needed to render the urls into a template properly.

- **Active**: Boolean to say whether or not the release is available in production. Turning this on makes it availiable to all users on the site and will use it when rendering the template. The latest active version will be considered the current production version.
- **Version**: This is arbitrary but required. It does not enforce a specific scheme so it's flexible to match whatever works on your project.
- **Release date**: This, combined with the Active state, determines what Release of the package is considered the current production version. The release who's Active _and_ has the most recent release date (but not in the future) wins. Using a future date/time is helpful if you want to schedule the roll out os a package.
- **Package**: Which package this release is for.
- **Files**: A JSON formatted list of the files included in the release. These files will be rendered in the order they are included in in the list. In the example below you can see there is a "file_type", which is used by the tag to determine which files to include in the tag render. Options are a nested JSON object that contains optional "HTML tag" attributes to include when rendering the template tag. In this example the "js" file includes an "integrity" attribute that will be added to the HTML and assigned the associated value.

```json
[
  { "file_type": "css", "path": "/static/css/v3.0.0/main.css" },
  { "file_type": "js", "path": "/static/js/v3.0.0/main.js", "options": { "integrity": "futureisbright!" } }
]
```

#### Release groups

Release groups are used for giving specific users access to particular versions of a release. This is useful for creating Beta Test or Early Access groups on your site so you can give them controlled access to that specific version.

- **Name**: There to help identify the release.
- **Description**: A description of the group.
- **Members**: Which users are in the group.
- **Active**: Whether or not the group is active. An inactive group is ignored by the template tag.
- **Sites**: Which sites this group is avaialble on.
- **Releases**: Which release the group has access to.

> **Note:** Of the seleted releases in the Releases, similar to the default behavior, the package with the newest release date will be used. For that reason it's a good idea to make sure to only select one at a time. Also the "Active" state of the release is ignored as this is used to determine which is the current active production release of the package.

## Advanced Usage

### Overriding the template

The template used be the tag is completely customizeable. It is found here:

```bash
templates/releasemanager/release_template.html
```

Take a look at what is there and if you want to add functionality or change formatting for your particular use, feel free. The version that comes with Django Release Manager assumes that the paths to the package files will be absolute paths so an example of customization might be to add Django's "{% static ... %}" tag to the template if you are keeping versions in the standard static location.

## TODOs

This is still a works in progress but its completely useable currently.

There are many things still to be done.

- More Unit Testing
- REST API
- Support for A/B testing

If there is a feature you want to request feel free to file an issue with the subject starting with "REQUEST: " or better yet, write it your self and make a pull request.
