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

   The release manager views are pretty simple. Mostly they include things like the auto-generated page on release notes. Feel free to include it how you want on your site. Here is an example:

   ```python
   urlpatterns = [
      ...
      path("releasemanager/", include("releasemanager.urls") ),
      ...
   ]
   ```

   **_API_**

   The API is a seperate set of URLs since many sites organize them under different URL hierarchies. Here is an example of how it can be done:

   ```python
   urlpatterns = [
      ...
      path("api/v1/releasemanager/", include("releasemanager.api.urls") ),
      ...
   ]
   ```

5. **Run Migrations**: Run the migrations to create the necessary database tables. The DB models are where information on the versions of your included packages are managed.

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
- Secutiry: By not allowing a package to be defined outside of the core code, it reduces places a malicious actor can inject something unexpected.

### Usage in Templates

This app stores information about your releases in the database and renders the URL to the files into your template using tags. You need to include the tag library in your template at the top of the page and then you can use it anywhere you want. Here is an example of how this would work on a page.

Include this at the top of your template to gain access to the app's tags:

```python
{% load release_template_tags %}
```

Now you can put this tag wherever is appropriate in your template:

```python
{% release_packages "basic" user=user file_group="js" %}
```

In this example, we are managing a Package called 'basic' and we want to render the 'js' file group. We pass along the user as well to get information about which version of the package the user has access to.

What the example above will do is find the latest release version of the package, "basic", that the user has access to and render the link for all the "js" files included in the package.

How this all works behind the scenes will be based on how you organize your packages as explained in the next steps.

> **Note:** Files are included in the template tag based on the file_group they are in. All files in a package release are rendered if they are in that file group. There is a template called "release_template.html" that handles what should be rendered based on the file extention. If the file ends in ".js" a "\<script\>" tag is used vs if the file is a ".css" file a "\<style\>" tag is used. There are examples later below when we talk about files.

### Admin Interfaces

#### Packages

There are three Admin panels and a template tag included in the project. The first is defining your Packages. A Package is the main app you are building and all releases will be children of the Package. The Name is for Human readability and the Description is there for future use in rendered templates. However the most important value is the "Package key". This is the value used by the template tag to know what package we are working with in that tag.

#### Releases

A release is a versioned collection of files associated with the Package. Releases contain all the information that is needed to render the urls into a template properly.

- **Active**: Boolean to say whether or not the release is available in production. Turning this on makes it availiable to all users on the site and will use it when rendering the template. The latest active version will be considered the current production version.

  > **Note:** All active release are included in the release notes. Turning the active state off will exclude them from the release note page.

- **Version**: This is arbitrary but required. It does not enforce a specific scheme so it's flexible to match whatever works on your project.
- **Release date**: This, combined with the Active state, determines what Release of the package is considered the current production version. The release who's Active _and_ has the most recent release date (but not in the future) wins. Using a future date/time is helpful if you want to schedule the roll out os a package.
- **Package**: Which package this release is for.
- **Files**: A JSON formatted list of the file "objects" are included in the release. These files will be rendered in the order they are included in in the list. In the example below you can see there is a "file_group", which is used by the tag to determine which files to include in the tag render. Options (which are optional) are a nested JSON object that contains HTML tag attributes to include when rendering the template tag. These attributes follow the "key":"value" == "attribute_name"="value" aproach. In this example the "js" file includes an "integrity" attribute that will be added to the HTML tag and assigned the associated value.

  ```json
  [
    { "file_group": "css", "path": "css/v3.0.0/main.css" },
    {
      "file_group": "js",
      "path": "https://mybucket.cdn.com/v3.0.0/js/main.js",
      "options": { "integrity": "futureisbright!" }
    }
  ]
  ```

  The end result would look like this:

  ```html
  css group...
  <link rel="stylesheet" href="/static/css/v3.0.0/main.css" />

  js group...
  <script src="https://mybucket.cdn.com/v3.0.0/js/main.js" integrity="futureisbright!" />
  ```

  > **Note:** Files are rendered in list order, per group.

  > **Note:** Files without a leading "/" or "http" will have the settings value 'RM_URL' prepended to the string. This by default is the STATIC_URL used by Django. Files with a full URL and ones with a "rooted URL" are rendered as is.

- **Groups**: Release groups are handled with Django's built-in user groups. To create a release group, all you need to do is create a new group in the Django's Group Admin and give it the "**can_test_releases**" permission. Now anyone you add to that group will have access to assigned permissions.

  > **Note:** Groups are exclusive. That means that once you add a group to a release it is only available to that group. A release with no groups is available to the whole site.

- **Sites**: Sites are similar to groups in that they restrict the release to only those sites. A release with no sites is available to _all_ sites on the server.

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

- REST API
- Tools for A/B testing

If there is a feature you want to request feel free to file an issue with the subject starting with "REQUEST: " or better yet, write it your self and make a pull request.
