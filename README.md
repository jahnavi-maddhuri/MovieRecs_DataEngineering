# MovieRecs_DataEngineering


## Workflow
* Extract data using API from movie site and load as a table into Databricks
* Create Docker image and container to host Flask app locally, which takes in user input for genre of movie interest and current mood
* Call on Databricks table and query using SQL filtering by genre, mood, and top ratings to output 3 movie recommendations 
* Push Docker image to AWS ECR (Elastic Container Registry) for cloud hosted image
* Deploy Flask app on AWS App Runner sourcing through image in ECR
* When local Flask app and Docker image is updated, automatic updates to ECR container and image using CI/CD 
* AppRunner is deployed automatically and ECR updates are automatically reflected in AppRunner web app


## Environment
* requirements.txt 
* Dockerfile to set up Flask app and Docker 
* Makefile - to build the Docker image, run it, and push to Docker Hub
* github actions - yml file with Github secrets for Docker Hub in order to automate the build and run when pushed to Github


## AWS App Runner deployment
![alt text](images/apprunner.png)

## Preparation and Running
1. Open codespaces 
2. Load repo to code spaces
3. Run `make build` to build the Docker image
4. Run `make run` to run the app
5. Run `make push` to push the image to Docker Hub