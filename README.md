In this project, we built an image classification model that can automatically detect which kind of vehicle delivery drivers have, in order to route them to the correct loading bay and orders. Assigning delivery professionals who have a bicycle to nearby orders and giving motorcyclists orders that are farther can help Scones Unlimited optimize their operations.

Project Steps Overview
Step 1: Data staging
Step 2: Model training and deployment
Step 3: Lambdas and step function workflow
Step 4: Testing and evaluation
Step 5: Optional challenge
Step 6: Cleanup cloud resources

We created an event-drivent ML workflow that can be incorporated into the Scones Unlimited production architecture. We used the SageMaker Estimator API to deploy your SageMaker Model and Endpoint, and we used AWS Lambda and Step Functions to orchestrate your ML workflow. Using SageMaker Model Monitor, we instrumented and observed your Endpoint, and at the end of the project we built a visualization to help stakeholders understand the performance of the Endpoint over time.
