# AWS serverless backend developer recruitment task setup instructions

## Setting up the environment
- You need to have [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) installed.
  - For Macos [Docker desktop](https://www.docker.com/products/docker-desktop/) is recommended
- You need to have account for Localstack Pro. If you don't you can get a free trial from https://localstack.cloud/
- Install [AWS Command Line Interface](https://aws.amazon.com/cli/)
- Install [NodeJS](https://nodejs.org/en) v18+
- Install [Yarn](https://yarnpkg.com/) globally
- Install [Python](https://www.python.org/) 3.11

## Setting up AWS profile for running the environment and tests
- Run all the commands on the repository root directory
- You need to create a AWS profile for deploy the service to Localstack  `aws configure --profile serverless`
  - The credential values can be anything.
  - Default region must be `us-east-1`
```
export LOCALSTACK_API_KEY=yourLocalstackPROApiKeyHere
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements_dev.txt
yarn
```

## Running the service
### Running on ARM architecture
`LOG_LEVEL="DEBUG" LS_LOG="trace" DEBUG="1" yarn deploy_arm`

### Running on x86_64 architecture
`LOG_LEVEL="DEBUG" LS_LOG="trace" DEBUG="1" yarn deploy`

## Lint your code
`PYTHONPATH=lambdas pylint ./lambdas`

## Executing the tests
You can execute the unit and integration tests with a command `invoke alltests`

## Tips
- You can run the environment also on dev container
- Read through tasks.py. It defines your invoke tasks.

### Generating database migrations
- Run separate instance of the PostgreSQL database by starting it up with the following command ´docker-compose up -d´
- Create the database with command `invoke createdb`
- Run existing migrations with command `invoke migratedb`
- Do your modifications to database model in file models.py
- Generate migrations with `invoke generatemigrations -m "your migration message"`
- Check the generated migration at `./lambdas/migrations/versions/...`
- Test your migration with command `invoke migratedb`
- If needed you can downgrade back to previous version with `invoke downgradedb -1`
