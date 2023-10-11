# Sports Betting Odds Prediction Pipeline

## What is this?
This is a template project for deploying an automated, improvable, containerized sports betting odds data pipeline in the cloud. Let's break down each of these aspects:

- **Automated** - Using EC2 Instance Scheduler, we start the EC2 instance at a given time. The Docker image inside of the EC2 instance runs automatically using the startup script, which starts our Apache Airflow server and triggers the pipeline.
- **Containerized** - The application runs inside of a Docker container meaning it will perform the same locally as it does in the cloud.


![image](https://github.com/tbryan2/sports-betting-odds-prediction-pipeline/assets/29851231/a8af1c9c-f84a-4557-a84a-21ef1551a8bb)


## Motivation
Data scientists spend a majority of their time developing models. At the end of this process, when they have a model they're happy with, they need a way to generate predictions on live, real world data. All of the effort up until this point has been spent on creating the model without any thought put into model deployment. The goal of this project is to create a __functional model__; in other words, to create a model where:

1) Generating predictions is both easy and automated, and
2) There can be continuous improvement of the model

By starting with the finished product in mind it validates all the effort spent on model development.
