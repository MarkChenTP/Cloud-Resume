# Mark-Cloud-Website-with-Resume

## Author
Mark Chen

<a name="table"></a>
## Table of Contents
* [Introduction](#introduction)
* [Features](#features)


## Introduction
Mark-Cloud-Website-with-Resume is a serverless website for hosting my personal information and resume. It is created for completing the <a href="https://cloudresumechallenge.dev/instructions/">Cloud Resume Challenge</a> from <a href="https://aws.amazon.com/developer/community/heroes/forrest-brazeal">Forrest Brazeal</a>.

<a href="#table">Back to Table of Contents</a>


## Features
Mark-Cloud-Website-with-Resume is hosted on Amazon Web Services (AWS) using an Amazon S3 bucket and delivered over HTTPS connection using an Amazon CloudFront distribution. Visitors of the website are counted by a visitor counter that is operated through an AWS Lambda function, a REST API on Amazon API Gateway, and an Amazon DynamoDB table. The website's frontend and backend infrastructures are automated with AWS Cloudformation and AWS Serverless Application Model (SAM). Templates of these infrastructures are then built, tested, and deployed via GitHub-Actions-based CI/CD pipelines that utilized AWS CLI.

<a href="#table">Back to Table of Contents</a>
