# Learning-projects
A collection of notebooks and python scripts that I have written in the process of learning new python skills. 

# Objective
My personal goal is to acquire new machine-learning related python skills and to apply them in practical projects. Hence, this repository is split into subprojects with specific questions and learning objectives. In this readme file, an outline is given.

# Projects
## Project 1 - Data gathering 
Project goal: 
A first step in any analysis is data gathering and display. The goal of the first project is to import data from an API into a pandas dataframe. Pandas is an often used python package for data analysis and it allows you to build dataframes resembling excel (or python list-of-lists). The API in question is cryptocompare and specifically we are interested in hourly cryptocurrency data. Since we might want to deploy this API-wrapper later, we want it to be as fast as possible. The primary way to achieve this is to make it check whether data for specific cryptocurrency has been downloaded before. Also, we are going to make it return a True/False statement when asked whether it has the most recent data or not. Finally, we want to visualize the data.



Learning objectives: 
  1) Understanding Pandas
  2) Building a wrapper around a web-API
  3) Create a wrapper class that doesn't ask for data it has already seen before and allows the user to check if the data is up to date. 
