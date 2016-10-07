
##This is the new pow. And it's really good. (ok I might be biased ;)
But it's by far the best PoW (concept and implementation) ever !

###Principle
As simple to use as possible. Everything you always need on board. And you can always escape and go RAW.

###Foundation:
* tornado
* sqlalchemy
* cerberus schemas on board
* react.js views
* tornado templates

###Super easy, quick to start and all the basics on board:
* super easy relations with decorators @relations.has_many("comments")
* super easy routing with decorators @app.add\_restful\_routes(), @app.add_route(route)
* db migrations autogenerated usin alembic in the back 
* validation on board with cerberus directly
* automatic scaffolding views
* generate_models
* generate_migrations
* generate_handlers
* generate_app

## Current Status:
The current <master> version in this repo is fully working except for:
* automatic scaffolding views
* generate_app (no problem, you can just copy the root folder)


