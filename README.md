# web-x
The EDI Website Project X

## Installation notes:

Use of the [Anaconda](https://www.anaconda.com/) environment supports
deployments for both Linux and Microsoft Windows using the `environment` yaml
file for each of the respective operating systems (environment-min.yml and 
environment-win.yml, respectively). To install a new deployment, use the
following sequence:

1. `git clone git@github.com:PASTAplus/web-x.git` or
   `git clone https://github.com/PASTAplus/web-x.git` depending upon your GitHub
   authentication configuration.
1. Change directories into the working `web-x` directory.
1. `conda env install --file environment-min.yml` (Linux flavor)
1. `conda activate web-x`
1. `python main.py`
1. Set your web browser to `http:\\localhost:8000`

 - Note that, as of 28 June 2021, `fastapi-chameleon` must still be installed
   from Michael Kennedy's GitHub [repository](https://github.com/mikeckennedy/fastapi-chameleon):
   `pip install git+https://github.com/mikeckennedy/fastapi-chameleon`. If
   installing from the Conda environment files (i.e., environment-min.yml or
   environment-win.yml), Conda will install `fastapi-chameleon` from GitHub for
   you.
 - Update (October 2021): `fastapi-chameleon` is now available through [PyPi](https://pypi.org/project/fastapi-chameleon/)
   and is now declared as such in the "environment" yaml files.

### Performing an Upgrade

Performing an upgrade to an existing deployment is nearly identical to the
initial installation:

1. Change directories into the working `web-x` directory.
1. `conda activate web-x`
1. `git pull`
1. `conda env update --file environment-min.yml` (Linux flavor)
1. `python main.py`

## Development notes:

*Web-x* uses the Python FastAPI web framework, including the Chameleon
templating engine. Because FastAPI is a Python asynchronous web framework,
*web-x* use the `uvicorn` web server, a very fast implementation of the
Asynchronous Server Gateway Interface (ASGI). *Web-x* uses an MVC
(Mode-View-Controller) deployment pattern with the following directory logic:

- `main.py` - the primary Fast API/Uvicorn entry point.
- `data` - Classes/software that construct object content containing data.
- `db` - Database ORM (object relational mapper) objects.
- `deployment` - System deployment specifications for production operations.
- `services` - Classes/software for handling low-level/system functionality. 
- `static` - Static web content, including images, CSS, Javascript, and HTML. 
- `templates` - Chameleon templates for displaying dynamic-based content.
- `viewmodels` - View models that convey state to Chameleon templates.
- `views` - FastAPI URL router.

The dynamic nature of modern web applications require creating/editing
multiple files within the MVC logic of *web-x*. The simplest example of this
process is the creation of a pseudo-static web page - "pseudo" in the sense
that static content is inserted dynamically into a "layout" template (the
"layout" template is applied to all web pages constructed in *web-x*).

To create a pseudo-static web page you must add a URL "route" to one of the 
route files in the `views` directory and a Chameleon HTML template file to one
of the `templates` directories. For example:

`\views\about.py`
```Python
@router.get('/about/vision-mission')
@template("about/vision-mission.html")
def vision_mission(request: Request):
    vm = ViewModelBase(request)
    return vm.to_dict()
```
The above route tells FastAPI that the URL "/about/vision-mission" is to be
handled by the Python `vision_mission` function, which returns the 
`vision-mission.html` template file.

`\templates\about\vision-mission.html`
```HTML
<div metal:use-macro="load: ../shared/layout.html">
    <div metal:fill-slot="content" tal:omit-tag="True">

<!--?        EDITABLE CONTENT GOES BELOW HERE \/\/\/-->
        <div class="vision">
            <h1>Vision Statement</h1>
            <p>Environmental knowledge through quality data</p>

            <h1>Mission Statement</h1>
            <p>Facilitate knowledge creation by making well-curated data and metadata discoverable, accessible, and reusable</p>
        </div>
<!--?        EDITABLE CONTENT GOES ABOVE HERE /\/\/\-->

    </div>
</div>
```

The above Chameleon HTML template is inserted into the `content` slot defined in
the `layout.html` template.

