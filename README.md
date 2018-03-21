# sims-backbone

This project is heavily based around the OpenAPI (swagger.io) definition of the API.

swagger.yaml defines the API and includes documentation - you can create an interactive API browser from this as well

Usage
=====

First you need to generate the client which you are going to use from the swagger.yaml - see [generate.sh](generate.sh) for how to generate the python flask server, and python and typescript clients using swagger codegen

To get the endpoint info, if you have aws credentials, go to serverless/sims-backbone-service and run `sls info` - you might need to run `npm install` first.

If you don't have credentials then ask somebody who does.

The trickiest part is configuring the OAuth authentication - see [test/test_base.py](test/test_base.py) for an example on how to for the python client - this uses [upload/config_dev.json](upload/config_dev.json) as the credential store - this is based on [upload/config_template.json](upload/config_template.json)

The generate client README.md has instructions on how to call the endpoints

The test directory contains examples of how to call all the API endpoints.

For uploading new records see the upload directory and all_load.sh for examples

Testing
=======

The web client can be tested in the usual way (`ng test`) for an Angular CLI application

The python client and server are (can be) tested together depending on the configuration.

You will need to configure a local postgres database - see [database/README](database/README) - once this is done then start the server via:

  `cd server`
  
  `./run.sh test`
  
  You can then run the `test/run.sh` script to run the python tests
  
  Deployment
  ==========
  
  To deploy the server see [serverless README](serverless/README)
  
  To deploy the web client see [client README](client/sims-backbone/README)
