# AWS serverless backend developer recruitment task

## Setup
- Instructions for setting up your development environment can be found from [INSTRUCTIONS.md](INSTRUCTIONS.md)
- Clone the task repository to your workstation. Do not fork the task repository. The forks are visible to everyone.
- Create a new public repository to GitHub and push your commits for the task there
- Original commit log of the task repository must be preserved.

## Application development 
- Everything you implement should have tests (unit / integration)
  - Use you own judgement what kind of testing is required
### Implementation ideas
- Implement a GraphQL endpoint that integrates to OpenWeather API and provides the data https://openweathermap.org/
- Create a database migration that creates a table or two for storing the data
- Implement GraphQL endpoint that updates the data to the database
- Implement a GraphQL endpoint to retrieve the data from the database
- Implement CI pipeline for the project with GitHub Actions 
  - Executes pylint
  - Executes unit and integration tests
  - Set up at least some kind of repository / code / dependency scanning for vulnerabilities
    - [Trivy](https://trivy.dev/)
    - [CodeQL](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql)
    - [Dependabot](https://docs.github.com/en/code-security/dependabot) ...
  - Set up [semantic-release](https://github.com/semantic-release/semantic-release) 

## Documentation:
- Draw an AWS architecture picture of the environment for example, with [Draw.io](https://app.diagrams.net/)
- List suggestions how to improve the architecture if you would have budget allocated for your AWS usage
- List improvement suggestions that you would do if there was more time / this would be a real application

## Returning the task
- Commit all code, documentation and architecture image to your GitHub repository
- Make sure that your Github repository is accessible (public) and provide the link to it




