# Django project creator

On one of my interview I got a test task in which I had to create a simple REST API application. But I had to fulfill the following requirements: 
- use Django and DRF 
- implement authentication 
- create Docker images and write instructions how to deploy it 
- create API documentation

The following points were not in the requirements, but without them I cannot create a good application:

- filtration
- pagination
- API testing 
- using JWT or OAuth for authentication 

All of the above requirements usually implemented by using libraries (drf-filter, pytest, swagger etc.) For each library we have to setup it. But when we use a lot of libraries we can spend a lot of time for it. 

In this app I try to automate creation of typycal Django/DRF application. 

This app work only in linux environment and used Python 3.6 or higher.

You can just load dist directory, and inside it run:
```sh
./start_project.sh
```
and answer to questions. In the same directory will be created new directory with ready to run  Django project.

If you want to add some functional. You can clone repo. Make necessary changes test it by run:
```sh
pytest tests
```
Then you can build the app just run: 
```sh
./build_dist.sh
```
It creates `dist` directory with `start_project.sh` script and `wheel` package.