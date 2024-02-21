# AWS serverless backend developer recruitment task setup instructions

## Setting up the environment
- You need to have [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) installed.
  - For Macos [Docker desktop](https://www.docker.com/products/docker-desktop/) is recommended
- You need to have account for Localstack Pro. If you don't you can get a free trial from https://localstack.cloud/
- You need to have an API key for OpenWeatherMap. You can get it from https://openweathermap.org/api
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
export OPENWEATHER_API_KEY=yourapikeyhere
export LOCALSTACK_AUTH_TOKEN="yourLocalstackPROApiKeyHere"
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
- For running the invoke tasks properly you need to have a file called .env with the folowing contents on the root folder of the repository
```
DB_MASTER_SECRET={"dbClusterIdentifier":"local-db-cluster","password":"postgres","dbname":"possu","engine":"postgres","port":5432,"host":"localhost","username":"postgres"}
DB_APP_SECRET={"dbClusterIdentifier":"local-db-cluster","password":"exampledb","dbname":"exampledb","engine":"postgres","port":5432,"host":"localhost","username":"exampledb"}
DB_ENC_SECRET=thisisgeneratedontheprodbysecretsmanager

LOG_LEVEL="DEBUG"
LS_LOG="trace"
DEBUG="1"
```
- If you need for some reason run invoke tasks against the database started by localstack the db port must be 4510
```
DB_MASTER_SECRET={"dbClusterIdentifier":"local-db-cluster","password":"postgres","dbname":"possu","engine":"postgres","port":4510,"host":"localhost","username":"postgres"}
DB_APP_SECRET={"dbClusterIdentifier":"local-db-cluster","password":"exampledb","dbname":"exampledb","engine":"postgres","port":4510,"host":"localhost","username":"exampledb"}
DB_ENC_SECRET=thisisgeneratedontheprodbysecretsmanager

LOG_LEVEL="DEBUG"
LS_LOG="trace"
DEBUG="1"
```

### Generating database migrations
- Run separate instance of the PostgreSQL database by starting it up with the following command ´docker-compose up -d db´
- Create the database with command `invoke createdb`
- Run existing migrations with command `invoke migratedb`
- Do your modifications to database model in file models.py
- Generate migrations with `invoke generatemigrations -m "your migration message"`
- Check the generated migration at `./lambdas/migrations/versions/...`
- Test your migration with command `invoke migratedb`
- If needed you can downgrade back to previous version with `invoke downgradedb -1`
