# Sports Betting Odds Prediction Pipeline

## What is this?
This is a template data pipeline project for generating predictions on upcoming sporting event using a machine learning model and live sportsbook odds. Here is a look at the infrastructure:

![image](https://github.com/tbryan2/sports-betting-odds-prediction-pipeline/assets/29851231/a8af1c9c-f84a-4557-a84a-21ef1551a8bb)

If you're unfamiliar with any of these technologies, this is a great starter project that you can expand on. Here are the main components:

- **Apache Airflow** - This is a workflow scheduler and what we will use to orchestrate pulling the latest odds from an API, running these odds through the model, and emailing out our predictions.
- **Amazon EC2** - This is an AWS service for creating and utilizing web servers; in other words a computer that we will rent that will automatically turn on and run our code.
- **Docker** - 

## Motivation
Data scientists spend a majority of their time developing models. At the end of this process, when they have a model they're happy with, they need a way to generate predictions on live, real world data. All of the effort up until this point has been spent on creating the model without any thought put into model deployment. The goal of this project is to create a __functional model__; in other words, to create a model where:

1) Generating predictions is both easy and automated, and
2) There can be continuous improvement of the model

By starting with the finished product in mind it validates all the effort spent on model development.
