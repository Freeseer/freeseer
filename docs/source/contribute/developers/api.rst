Developing new APIs
===================

Freeseer uses a REST API framework to remotely control a headless Freeseer host. This article will give a primer on how APIs are designed, and how they are implemented with `Flask <http://flask.pocoo.org>`.

RESTful API Primer
------------------

Freeseer's API strives to be RESTful, so you should learn the basics of REST theory to ensure that your endpoint is in fact RESTful. What follows is by no means a replacement for figuring out how RESTful APIs and endpoints are designed, but it is useful for understanding some of the design choices for our framework.

A REST API is a resource based interface for interacting with software. The most common use case for a REST API, is to allow us to interact with software across a network, without requiring any knowledge of the software'srinternals. Any parts of your software you wish to control externally are abstracted into resources and signified by URIs called endpoints. So in other words to design and develop a RESTful API is to design and develop endpoints that will allow us to interact with parts of your software from the outside. If some set of endpoints is logically related, they are grouped into a set called an API (For example, the Recording API, or the Configuration API).

So, to keep the somewhat vague terminology straight: generally when people talk about a “RESTful API”, they are referring to the entire RESTful API and also perhaps the framework on which the endpoints and APIs are built, but when they refer to “an API”, “the <insert group name here> API”, or some variation, they are referring to some specific API or set of APIs.

Designing Endpoints
-------------------

In the most simplistic and crude sense, a RESTful endpoint will be the plural of the type of resource that you want perform a ``GET``, ``POST``, ``DELETE``, or ``PATCH`` on. For example if you want to have RESTful endpoint for handling a server's users, you could have an endpoint named:

``/users``

You could either get a list of all users with

``GET /users``

Or post a new user with

``POST /users``

Or if you want to get specific instances of that resource, you use some identifier.

``GET /users/1`` (to get user with id “1”)
``DELETE /users/1`` (to delete user with id “1”)

You also want to have some parameters for your endpoint. For example for creating a user, you will want some set of parameters like, username, email, etc.

**From endpoints to an API**

In the Freeseer RESTful API there is a logical organization to our endpoints, which we refer to as APIs. For example, one set of RESTful endpoints is grouped under the Recording API, where each resource is related to creating, deleting, accessing, or performing an action on some recording. Very rarely is an endpoint designed in isolation, we consider what API needs to be developed first and then think of what endpoints would fall under that API. So make sure that your endpoint either falls under and existing API or create a new API for that endpoint to fall under.

Developing an API
-----------------

**Note:** *From this point forward we assume that you are creating a new API (a new logically grouped set of RESTful API endpoints). (If you simply need to add new endpoint to an existing API, you can skip to the section <creating new endpoints>)*

**Creating an API module**

In the ``freeseer/frontend/controller/`` folder, create a new module <api_name>.py replacing <api_name> with your APIs name. You will need to import the ``Blueprint`` and ``request`` modules from flask with:

.. code-block:: python

    from flask import Blueprint
    from flask import request

You will also need to import the following:

.. code-block:: python

    from freeseer.frontend.controller import app

``app`` is the server's ``Flask`` app.

**Blueprints**

 To organize our endpoints into separate APIs, we make use of Flask's ``Blueprint`` module. All of our endpoints and API specific code and data will exist in an instance of the ``Blueprint`` module, which simply extends the existing Flask server app. 

So to instantiate our API, we add the following code to our API module.

.. code-block:: python

    <api_name> = Blueprint('<api_name>', __name__) 

To associate our Blueprint with the Flask app, we need to add code to ``freeseer/frontend/controller/__init__.py``.

.. code-block:: python

    from freeseer.frontend.controller.<api_name> import <api_name>

    app.register(<api_name>)

**API-specific Functions and Data**

Outside of the endpoints, there are a number of functions an API may need to function properly. For example, the ``recording`` api needs to instantiate the multimedia backend for any of its endpoints to work. The ``Blueprint`` can provide us with a number of decorators to wrap any functions that would be necessary for the functioning of our api. Furthermore, any api specific data can be saved to the ``Blueprint`` object.

One of the most useful for developers will be the ``@<name_of_api>.before_first_request`` decorator. Any code that needs to be run so that the endpoints can function should be decorated by this decorator so it can run before the first request is made to the REST framework. For example, in the recording api, we have a function called ``configure_recording()`` that loads references to existing videos from disk so our endpoints will work. By wrapping it with ``@recording.before_app_first_request``, that code will fire when the first call to the REST API is made. 


Developing Endpoints
--------------------

**Route decorator**

Every endpoint is wrapped with a ``@<name_of_api>.route()`` decorator. 

*Route Parameters* 

*rule* 

the first parameter of the ``route()`` function. The path of the endpoint with any path parameters declared. Ex. route('/users') will establish a route at to http://<host_info>/users

*methods*

a list of all methods (GET, POST, etc.) that this route should accept. Example: ``route('users/<int:id>', methods=['GET'])`` means this function will only fire if a GET request is sent to the corresponding path.

More information about route registration can be found in the `Flask documentation <http://flask.pocoo.org/docs/0.10/api/#url-route-registration>`

**Path parameters**

Any path parameters are specified with angular brackets. Ex. ``route('/users/<username>')`` means any text entered after ``/users/`` will be saved as a string under the variable ``username``.

If you want your parameter to be coerced to a certain type, you use the format <type:name>

Available types include int, and float.

**Parameters sent via request body**

In Flask, for an endpoint to accept a parameters from a request body, we don't need to explicitly declare body parameters in our function definition or route decorator. A function can examine the body of data sent by some client by reading the data found in 'request.form' where our body would be contained.


**Request validation**

Obviously we want some way to ensure our endpoint gets the right kind of data (in our case, ``JSON`` formatted), and gets the data the endpoint expects. So we have added a module called ``validate`` that ensures the body data is the correct format, and contains the data the endpoint needs to function. 

The validate module validates request data through ``validate_form(to_validate, schema)``

*Parameters:*

*to_validate* - the body data of our request. In most cases this will be 'request.form'.

*schema* - a `jsonschema <http://json-schema.org>` formatted schema to describe what our request data should look like.   

If the validation fails, ``validate_form()`` throws an ``HTTPError`` which will be sent to the client as a response.

**validation_schemas**

Depending on the nature of your API, your validation schema may be automatically generated. <Francisco can you please fill in any information about how this works?>. If your schema is not auto-generated, you may have to include any relevant schemas in the Blueprint object. (In the case of Recording API, we store the schemas in a dictionary called form_schema.)

We use the library jsonschema to validate our json objects. The json-schema `documentation <http://json-schema.org>` will have any information you need for creating json schemas to validate data against.

**Returning a response**

For your function to return information back to the client, the endpoint function needs to return a ``dict`` which represents the JSON object that will be the body of the response returned by the server.  

By wrapping our endpoint function with ``@http_response(status_code)`` (status_code being the HTTP status code that indicates success), the ``dict`` and ``status_code`` become the basis for our response to the client. The decorator should go between the route decorator and the endpoint function.

**Error handling**

Our endpoints needs some way of handling requests that would cause our endpoint functions to fail, and alert the client that their request was faulty. We do this by catching the error as it happens, or pre-empting it via some validation, and sending a response back to the client that includes error information for why the request failed.

For example: an endpoint receiving a request for a non-existent resources like a non-existent recording. When we do run into one of these errors, we need to send a response with an appropriate status code, and error information in our responses body. In the case of a non-existent recording, we alert the user with a 404 status code, and our response body will be a JSON object that includes a useful message such as 'No recording with id <id> was found.'

When we run into this kind of situation, we raise an ``HTTPError`` in our endpoint function.

``HTTPError(status_code, description=None)``

*status_code:* 
the HTTP Error code that corresponds to our error, the error codes supported at present are (more can always be added):

400: 'Bad Request: Request could not be understood due to malformed syntax.',
401: 'Unauthorized: Authentication was not provided or has failed.',
404: 'Not Found: Requested resource is not available.',
409: 'Conflict: Request could not be processed because of server conflict.',
422: 'Unprocessable Entity: Request could not be processed due to semantic errors.'

*description:*
a string containing human readable information that a client user would find informative, and rectify the issue. If we don't supply a description method, the user will only read a generic message corresponding to the status code.

*Errors handled by the framework*

In some situations the framework or another module already handles these errors for us, so we do not need to worry about them. (The following list may not be exhaustive, feel free to add more)

Faulty path parameters: If path parameters cannot be coerced to the type specified by the route's rule parameter, it will send the client a response with error information.

Validation errors: As long as we are calling the validate_form method from the validate module, the validate module will raise an HTTPError and supply appropriate information.
