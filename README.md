[![Build Status](https://travis-ci.org/malariagen/sims-backbone.svg?branch=master)](https://travis-ci.org/malariagen/sims-backbone)
[![Coverage Status](https://coveralls.io/repos/github/malariagen/sims-backbone/badge.svg?branch=master)](https://coveralls.io/github/malariagen/sims-backbone?branch=master)

# sims-backbone

This project is heavily based around the OpenAPI (swagger.io) definition of the API.

swagger.yaml defines the API and includes documentation - you can create an interactive API browser from this as well (see below)

Usage
=====

First you need to generate the client which you are going to use from the swagger.yaml - see [generate.sh](generate.sh) for how to generate the python flask server, and python and typescript clients using swagger codegen

To get the endpoint info, if you have aws credentials, go to serverless/sims-backbone-service and run `sls info` - you might need to run `npm install` first.

If you don't have credentials then ask somebody who does.

The generated client README.md has instructions on how to call the endpoints

The example directory contains a simple example of how to call the API

The trickiest part is configuring the OAuth authentication - see [example/example.py](example/example.py) for an example on how to for the python client - this uses [example/config.json](example/config.json) as the credential store - this is based on [example/config_template.json](example/config_template.json)

You also need to set the environment variables in run_example.sh to point to the correct endpoints.

The test directory contains examples of how to call all the API endpoints.

For uploading new records see the upload directory and all_load.sh for examples - the programs here
do a lot of work connected to setting up locations and identifiers

Interactive API browser
=======================

If you use the generated server, in python-flask-server, directly then you can visit the
[http://localhost:8080/v1/ui/](interactive browser)

While this can be configured for authentication and access to the remote service it's probably best
used to get a view of the methods available as part of the API.

Testing
=======

The web client can be tested in the usual way (`ng test`) for an Angular CLI application

The python client and server are (can be) tested together depending on the configuration.

If you want a local instance without authentication then you can use the noauth arg to the
generate.sh script when generating the client/server code.

You will need to configure a local postgres database - see [database/README](database/README) - once this is done then start the server via:

  `cd server`
  
  `./run.sh test`
  
  You can then run the `test/run.sh` script to run the python tests
  
  Deployment
  ==========
  
  To deploy the server see [serverless README](serverless/README)
  
  To deploy the web client see [client README](client/sims-backbone/README)
