## Code Repositories

Taking an [IaC](https://en.wikipedia.org/wiki/Infrastructure_as_code) approach, our hosting infrastructure is defined
in Terraform code.

There are two repositories that handle our infrastructure:

* [Digital Land Infrastructure](https://github.com/digital-land/digital-land-infrastructure) - this contains our primary infrastructure and allows the user to interact all environments and is what the instructions in this guide aim to help with.
  This repository contains Terraform configuration files that create the necessary services to deploy applications and background tasks for the planning data service.  It is structured as a set of smaller Terraform projects - based around systems.  Each system has it's own isolated state meaning that changes can be made more discretely and efficiently.  Please view the repository's [README](https://github.com/digital-land/digital-land-infrastructure/blob/main/README.md) for a fuller explanation.
* [Global Digital Land Infrastructure](https://github.com/digital-land/global-digital-land-infrastructure) - this mainly contains infrastructure that needs to lie outside of the other repo such as nameserver records to subdomains as well as lagacy infrastructure such as S3 buckets who's content is stored in glacier.
  > [!WARNING]
  > Note this repository is being phased out.  Please speak to a member of the team before considering or proposing any changes.


## Deploying

#### Authentication

[aws-vault](https://github.com/99designs/aws-vault) is recommended to assume the correct role for deploying resources to
the AWS environments. This guide does not cover the correct configuration of aws-vault.

Once configured correctly all the following commands can be executed as follows.

```shell
aws-vault exec <profile> -- <command>
```

### An Existing Environment

To deploy updates to an existing environment first, clone the
[infrastructure repository](https://github.com/digital-land/digital-land-infrastructure)
`git clone git@github.com:digital-land/digital-land-infrastructure.git`.

Once cloned, run `make apply STAGE=<environment>` to deploy the updated infrastructure configuration.

### A New Environment

To deploy a new environment the following details are needed:

* Environment name
* Root domain name

First, clone the [infrastructure repository](https://github.com/digital-land/digital-land-infrastructure)
`git clone git@github.com:digital-land/digital-land-infrastructure.git`.

Familiarise youself with the structure of the repository, noting that the Terraform projects therein (systems) should
be applied in specific order, starting with core.

Navigate to the desired system directory, e.g. system/core, and run `make new-environment STAGE=<environment> DOMAIN=<root domain>` to create the needed configuration files. Commit the created files to the repository.

Run `make apply STAGE=<environment>` to deploy the new environment, do not worry about errors, this will fail the first
time you deploy a new environment. There should be roughly 500 new resources created to action the deployment.

On completion of the first deployment of core run you will see errors regarding the verification of SSL certificates created for
the environment.

**First `terraform apply` output**

```shell
│ Error: error creating CloudFront Distribution: InvalidViewerCertificate: The specified SSL certificate doesn't exist, isn't in us-east-1 region, isn't valid, or doesn't include a valid certificate chain.
│       status code: 400, request id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
│
│   with module.application_main.aws_cloudfront_distribution.cdn,
│   on modules/application/application_traffic.tf line 28, in resource "aws_cloudfront_distribution" "cdn":
│   28: resource "aws_cloudfront_distribution" "cdn" {
│
```

To resolve this error we must configure the DNS provider for the root domain to use these nameservers, and then run the
deployment for the environment a second time. To obtain the DNS nameservers, first log into the AWS console
(`aws-vault login <profile>`), then access Route53 > Hosted Zones > [domain] and get the four values for the NS record,
configuring these servers with the domain's DNS provider.

This can be done by using the global digital land infrastructure to create the required record.

Once DNS delegation is complete, you may check that the SSL certificate has been generated by logging into AWS for the
appropriate account and checking the ACM service in the us-east-1 region. The relevant certificate will show as verified
once delegation is complete.

You can now run `make apply STAGE=<environment>` for the second time and should see changes to the CDN and Route53
resources. The new infrastructure is now set up, and all that remains is to deploy applications into the new
environment. At this point all applications will serve a page stating that the service will shortly be resumed.

<strong>Note:</strong> The following slack bot token parameters required to be update manaully in the aws Parameter Store (SSM).
The slack bot token `(dl-github-actions)` values are the same across all envirnments and can be obtains from other environment notification slack token or from Slack direct.

* `/<environment>-datasette-tiles/notifications/slack-token`
* `/<environment>-datasette/notifications/slack-token`
* `/<environment>-main/notifications/slack-token`
* `/<environment>-status/notifications/slack-token`

#### Deploying data

In order for the applications to start and run we must have data in the platform. Firstly we need both background tasks
deployed to the environment prior to uploading data for processing.

Deploy the following applications using the dispatch workflow

* [datasette-tiles (task)](https://github.com/digital-land/tiles-builder/actions/workflows/deploy-task.yml)
  A background task that builds [MBTiles](https://github.com/mapbox/mbtiles-spec) files for use in the datasette-tiles
  application.
* [postgres-importer](https://github.com/digital-land/digital-land-postgres/actions/workflows/deploy.yml)
  A background task that imports the digital-land.sqlite3 in a postgres database.

Once both applications are deployed we can now copy data into the environment. Data generally enters the environment via
upload as part of a [collection job](https://github.com/digital-land?q=-collection) or via the
[entity-builder](https://github.com/digital-land/entity-builder) and
[digital-land-builder](https://github.com/digital-land/digital-land-builder) jobs.

While these data pipelines run on a regular basis you may need to start with a set of data from another environment in
order to successfully deploy the various applications needed to run the system. The AWS command line application has a
command to make this easier. Run with `--dryrun` to preview the files to be synced (though the output is not useful).

```bash
aws s3 sync s3://[source]-collection-data s3://[destination]-collection-data
```
<strong>Note:</strong> It may be worth deployed the main application once before deploying data and once after as the database schema is applied when the application is

#### Deploying applications

Now the new environment is up and running you should deploy the following applications:

* [main](https://github.com/digital-land/digital-land.info/actions/workflows/continuous-deployment.yml)
  The main digital land web application.
* [datasette](https://github.com/digital-land/datasette-builder/actions/workflows/deploy.yml)
  A web service and API allowing SQL queries against sqlite databases.
* [datasette-tiles (application)](https://github.com/digital-land/tiles-builder/actions/workflows/deploy-application.yml)
  A web service that allows the main application's frontend to draw vector tiles on the map feature from our datasets.
* [digital-land-status](https://github.com/digital-land/digital-land-status/actions/workflows/deploy.yml)
  A simple web page which show the digital land dependencies status.

<strong>Note:</strong> data may need to be re-deployed to the postgres db once the application has been deployed due to the build failing if no data is found but the database schema only being deployed when the app is


### Lambda functions

* EFS Sync collection
* Slack Notification

The creation of the actual aws lambda functions are still in the [infrastructure repo](https://github.com/digital-land/digital-land-infrastructure), but the function code are now located in this repo `https://github.com/digital-land/digital-land-lambda`.

**GitHub deployment workflow (Lambda functions)**

{% raw %}
```yaml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        type: environment
        description: The environment to deploy to.

jobs:
  detect-environments:
    runs-on: ubuntu-latest
    outputs:
      environments: ${{ steps.environments.outputs.result }}
    steps:
      - uses: actions/github-script@v6
        id: environments
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          result-encoding: json
          script: |
            if (context.payload?.inputs?.environment) return [context.payload?.inputs?.environment];
            const {data: {environments}} = 
              await github.request(`GET /repos/${process.env.GITHUB_REPOSITORY}/environments`);
            return environments.map(e => e.name)

  deploy:
    runs-on: ubuntu-latest
    needs: [detect-environments]
    strategy:
      matrix:
        environment: ${{ fromJSON(needs.detect-environments.outputs.environments) }}
    environment: ${{ matrix.environment }}
    steps:
      - uses: actions/checkout@v3

      - name: Install aws cli
        run: |
          curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
          unzip -q awscliv2.zip
          sudo ./aws/install --update
          sudo apt-get update
          sudo apt-get install -y rsync

      - name: Build efs sync collection
        run: |
          rm -rf node_modules/
          docker build -t efs-sync-collection-lambda-builder ./efs-sync-collection
          docker run -i -v ${GITHUB_WORKSPACE}/efs-sync-collection:/var/task efs-sync-collection-lambda-builder

      - name: Build Notification functions
        run: |
          rm -rf node_modules/
          docker build -t ${{ matrix.environment }}-notification-builder ./notification-code
          docker run -i -v ${GITHUB_WORKSPACE}/notification-code:/var/task ${{ matrix.environment }}-notification-builder

      - name: Set File Permissions
        run: |
          chmod 0666 ./efs-sync-collection
          chmod 0666 ./notification-code
  
      - name: Create efs sync Archive
        run: |
          sudo -s sh -c 'cd efs-sync-collection && zip -r ../efs-sync-collection.zip ./*'
          sudo -s sh -c  'pwd'

      - name: Upload efs sync artifact for deployment job
        uses: actions/upload-artifact@v3
        with:
          name: efs-sync-collection
          path: efs-sync-collection.zip

      - name: Create Notification Archive
        run: |
          sudo -s sh -c 'cd notification-code && zip -r ../notification-code.zip ./*'
          sudo -s sh -c  'pwd'
  
      - name: Upload Notification artifact for deployment job
        uses: actions/upload-artifact@v3
        with:
          name: notification-code
          path: notification-code.zip
      
      - name: Set up AWS credentials
        uses: aws-actions/configure-aws-credentials@v1-node16
        with:
          aws-access-key-id: ${{ secrets.DEPLOY_AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.DEPLOY_AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-west-2
      
      - name: Deploy aws Lambda functions
        run: |
          aws lambda update-function-code --function-name ${{ matrix.environment }}-efs-sync-collection --zip-file fileb://./efs-sync-collection.zip
          aws lambda update-function-code --function-name ${{ matrix.environment }}-main-slack-notifier --zip-file fileb://./notification-code.zip
          aws lambda update-function-code --function-name ${{ matrix.environment }}-status-slack-notifier --zip-file fileb://./notification-code.zip
          aws lambda update-function-code --function-name ${{ matrix.environment }}-datasette-tiles-slack-notifier --zip-file fileb://./notification-code.zip
          aws lambda update-function-code --function-name ${{ matrix.environment }}-datasette-slack-notifier --zip-file fileb://./notification-code.zip
```
{% endraw %}


## Configuration Changes

### Add a new application

To create a new application in the terraform configuration, you will need to know the following:

* The **GitHub repository** (under the [digital-land](https://github.com/digital-land) organisation) hosting the application code.
* The **subdomain** of `planning.data.gov.uk` that the application will run under.
* An estimate of the **memory usage** of the application.
* A list of the application **environment variables**.
* If the application needs access to the SQLite or MBTiles files generated by background tasks.
* Decide which system project in which the application should reside

Add a new section to `variables.tf` under `locals.application_defaults`, replacing attributes as required.

```hcl
<name> = {
  // The subdomain to serve the application from
  access = {
    domain = "<subdomain>"
  }

  // Any static environment variables
  environment = {
    PORT = 5000 // Defaults to 80
  }

  // The GitHub repository that hosts the application code
  github_repository = "<organisation>/<repository>"

  // Set to true if the GitHub repository contains both an
  // application and a background task.
  github_repository_dual = false

  // The application healthcheck path and timeout
  healthcheck = {
    endpoint = "/"
    timeout = "30"
  }

  // Minimum and maximum number of application instances
  // The auto-scaling configuration scales the initial
  // number on 60% CPU Utilisation
  instances = {
    minimum = 1
    maximum = 2
    initial = 1
  }

  // The resources needed per application instance
  resources = {
    memory      = 1024
    cpu_credits = 20
  }
}
```

* Add a new application block with a Terraform file of the relevant system project, replacing attributes as required.

```hcl
module "application_<name>" {
  source = "./modules/application"

  // Application name
  name                   = "<name>"

  // The environment this application is deployed to (do not change)
  stage                  = var.stage

  // All resources created by this module with have their names
  // prefixed with the string here.
  resource_prefix        = "${var.stage}-<name>"

  // The ECS cluster this application is deployed to
  cluster                = module.cluster.cluster
  // Tags associated with
  tags                   = module.tags.computed
  // The environment variables to expose to the application
  environment            = merge(
    module.storage.environment,
    local.applications["<name>"].environment,
  )
  // The stored secrets to inject into the application environment
  secrets                = module.storage.secrets
  // var.deployment_approval set to a list of users will enforce approvals
  //   to deploy to this environment
  deployment_approval    = var.deployment_approval

  // These are set via the `locals.application_defaults` section in `variables.tf`
  github_repository      = local.applications["<name>"].github_repository
  github_repository_dual = local.applications["<name>"].github_repository_dual
  healthcheck            = local.applications["<name>"].healthcheck
  instances              = local.applications["<name>"].instances
  resources              = local.applications["<name>"].resources
  access                 = merge(
    local.applications["<name>"].access,
    {
      certificate_arn = module.domain.certificate_arn
      zone_id         = module.domain.zone_id
    }
  )

  // EFS volumes to mount for this application
  //   (must set network mode to awsvpc)
  volumes                = {
    datasets = merge(
      module.storage.files.datasets,
      // Add this if you wish the volume to be mounted read-only
      {
          readonly = true
      }
    )
  }

  // Additional IAM permissions, see `outputs.tf` in `modules/storage`
  //   for a list of permissions
  additional_permissions = merge(module.storage.permissions.efs_read)

  network = {
    // Set to awsvpc if you need to mount a volume, bridge otherwise
    mode            = "awsvpc"
    vpc_id          = module.network.vpc_id
    subnets         = module.network.subnet_public_ids
    security_groups = [module.network.security_group_public_id]
  }
}
```

* Run terraform apply
* Check that the service is running on the appropriate domain name, if it is you will see a holding page.
* Update the slackbot token at `/<environment>-<application>/notifications/slack-token` in AWS SSM
* If configured with a GitHub repository add a deployment workflow to the repo,
  otherwise you need only authenticate using the details under `/<environment>-<name>/deployer/access_*`
  and push a built docker image to the

**GitHub deployment workflow (Application Only)**

{% raw %}
```yaml
name: Deploy
on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        type: environment
        description: The environment to deploy to.

jobs:
  # Include any tests or audits in jobs prior to detect-environments.
  detect-environments:
    runs-on: ubuntu-latest
    needs: [] # Add any previous jobs here
    outputs:
      environments: ${{ steps.environments.outputs.result }}
    steps:
      - uses: actions/github-script@v6
        id: environments
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          result-encoding: json
          script: |
            if (context.payload?.inputs?.environment) return [context.payload?.inputs?.environment];
            const {data: {environments}} =
              await github.request(`GET /repos/${process.env.GITHUB_REPOSITORY}/environments`);
            return environments.map(e => e.name)

  deploy:
    runs-on: ubuntu-latest
    env:
      DOCKER_REPO: ${{ secrets.DEPLOY_DOCKER_REPOSITORY }}
    needs: [detect-environments]
    strategy:
      matrix:
        environment: ${{ fromJSON(needs.detect-environments.outputs.environments) }}
    environment: ${{ matrix.environment }}
    steps:
      - uses: actions/checkout@v3
      - id: vars
        run: echo "sha_short=$(git rev-parse --short HEAD)" >> $GITHUB_OUTPUT
      - run: |
          sudo apt-get update
          sudo apt-get install -y rsync
      - uses: aws-actions/configure-aws-credentials@v1-node16
        with:
          aws-access-key-id: ${{ secrets.DEPLOY_AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.DEPLOY_AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-west-2
      - uses: aws-actions/amazon-ecr-login@v1
      - run: docker pull $DOCKER_REPO:latest
      - run: docker build -t $DOCKER_REPO:${{ steps.vars.outputs.sha_short }} .
      - run: docker tag $DOCKER_REPO:${{ steps.vars.outputs.sha_short }} $DOCKER_REPO:latest
      - run: docker push $DOCKER_REPO:${{ steps.vars.outputs.sha_short }}
      - run: docker push $DOCKER_REPO:latest
```
{% endraw %}

### Add a new background task

To create a new background task in the terraform configuration, you will need to know the following:

* The **GitHub repository** (under the [digital-land](https://github.com/digital-land) organisation) hosting the task code.
* A list of events that should trigger a background task run (currently only s3 events are supported).
* An estimate of the **memory usage** of the task.
* A list of the task **environment variables**.
* If the task needs access to the SQLite or MBTiles files.

Add a new variables section in a relevant system project, replacing attributes as required.

```hcl
<name> = {
  // The GitHub repository that hosts the background task code
  github_repository = "<organisation>/<repository>"

  // Set to true if the GitHub repository contains both a
  // background task and an application.
  github_repository_dual = false

  // The resources needed per background task invocation
  resources = {
    memory      = 8192
    cpu_credits = 1024
  }

  // A map of the events that should trigger this task
  triggers = {
    entity-uploaded = {
      // The events that trigger the task
      events = ["PutObject", "CompleteMultipartUpload"]
      // The S3 bucket to watch for events
      bucket = "${var.stage}-collection-data"
      // The keys of S3 objects to watch for
      watch  = ["/entity-builder/dataset/entity.sqlite3"]
    }
  }
}
```

* Add a new task block in the relevant system project, replacing attributes as required.

```hcl
module "task_<name>" {
  source = "./modules/application-task"

  // Application name
  name                   = "<name>"

  // The environment this task is deployed to (do not change)
  stage                  = var.stage

  // All resources created by this module with have their names
  // prefixed with the string here.
  resource_prefix        = "${var.stage}-<name>"

  // The ECS cluster this task is deployed to
  cluster                = module.cluster.cluster
  // Tags associated with
  tags                   = module.tags.computed
  // The environment variables to expose to the task
  environment            = merge(
    module.storage.environment,
    local.tasks["<name>"].environment,
  )
  // The stored secrets to inject into the task environment
  secrets                = module.storage.secrets
  // var.deployment_approval set to a list of users will enforce approvals
  //   to deploy to this environment
  deployment_approval    = var.deployment_approval

  // These are set via the `locals.task_defaults` section in `variables.tf`
  github_repository      = local.tasks["<name>"].github_repository
  github_repository_dual = local.tasks["<name>"].github_repository_dual
  triggers               = local.tasks["<name>"].triggers
  instances              = local.tasks["<name>"].instances
  resources              = local.tasks["<name>"].resources

  // EFS volumes to mount for this task
  volumes                = {
    datasets = merge(
      module.storage.files.datasets,
      // Add this if you wish the volume to be mounted read-only
      {
          readonly = true
      }
    )
  }

  // Additional IAM permissions, see `outputs.tf` in `modules/storage`
  //   for a list of permissions
  additional_permissions = merge(module.storage.permissions.efs_read)

  network = {
    vpc_id          = module.network.vpc_id
    subnets         = module.network.subnet_public_ids
    security_groups = [module.network.security_group_public_id]
  }
}
```

* Run terraform apply
* If configured with a GitHub repository add a deployment workflow to the repo,
  otherwise you need only authenticate using the details under `/<environment>-<name>/deployer/access_*`
  and push a built docker image to the

**GitHub deployment workflow (Task Only)**

{% raw %}
```yaml
name: Deploy
on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        type: environment
        description: The environment to deploy to.

jobs:
  detect-environments:
    runs-on: ubuntu-latest
    outputs:
      environments: ${{ steps.environments.outputs.result }}
    steps:
      - uses: actions/github-script@v6
        id: environments
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          result-encoding: json
          script: |
            if (context.payload?.inputs?.environment) return [context.payload?.inputs?.environment];
            const {data: {environments}} =
              await github.request(`GET /repos/${process.env.GITHUB_REPOSITORY}/environments`);
            return environments.map(e => e.name)

  deploy:
    runs-on: ubuntu-latest
    env:
      DOCKER_REPO: ${{ secrets.DEPLOY_DOCKER_REPOSITORY }}
    needs: [detect-environments]
    strategy:
      matrix:
        environment: ${{ fromJSON(needs.detect-environments.outputs.environments) }}
    environment: ${{ matrix.environment }}
    steps:
      - uses: actions/checkout@v3
      - id: vars
        run: echo "sha_short=$(git rev-parse --short HEAD)" >> $GITHUB_OUTPUT
      - run: |
          sudo apt-get update
          sudo apt-get install -y rsync
      - uses: aws-actions/configure-aws-credentials@v1-node16
        with:
          aws-access-key-id: ${{ secrets.DEPLOY_AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.DEPLOY_AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-west-2
      - uses: aws-actions/amazon-ecr-login@v1
      - run: docker pull $DOCKER_REPO:latest
      - run: docker build -t $DOCKER_REPO:${{ steps.vars.outputs.sha_short }} .
      - run: docker tag $DOCKER_REPO:${{ steps.vars.outputs.sha_short }} $DOCKER_REPO:latest
      - run: docker push $DOCKER_REPO:${{ steps.vars.outputs.sha_short }}
      - run: docker push $DOCKER_REPO:latest
```
{% endraw %}

#### Deploy a Task and Application

To deploy both a task and application from the same repository, use the following two github actions workflows.

**`.github/workflows/deploy-application.yml`**

{% raw %}
```yaml
name: Deploy Application

on:
  push:
    branches: [main]
    # Put a path here for the folder to watch for changes
    paths: [application/]
  workflow_dispatch:
    inputs:
      environment:
        type: environment
        description: The environment to deploy to (select an -application environment).

jobs:
  detect-environments:
    runs-on: ubuntu-latest
    outputs:
      environments: ${{ steps.environments.outputs.result }}
    steps:
      - uses: actions/github-script@v6
        id: environments
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          result-encoding: json
          script: |
            if (context.payload?.inputs?.environment) return [context.payload?.inputs?.environment];
            const {data: {environments}} =
              await github.request(`GET /repos/${process.env.GITHUB_REPOSITORY}/environments`);
            return environments.map(e => e.name).filter(e => e.indexOf('-application') != -1)

  deploy:
    runs-on: ubuntu-latest
    env:
      DOCKER_REPO: ${{ secrets.DEPLOY_DOCKER_REPOSITORY }}
    needs: [ detect-environments ]
    strategy:
      matrix:
        environment: ${{ fromJSON(needs.detect-environments.outputs.environments) }}
    environment: ${{ matrix.environment }}
    steps:
      - uses: actions/checkout@v3

      - id: vars
        run: echo "sha_short=$(git rev-parse --short HEAD)" >> $GITHUB_OUTPUT

      - run: |
          curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
          unzip -q awscliv2.zip
          sudo ./aws/install --update
          sudo apt-get update
          sudo apt-get install -y rsync

      - uses: aws-actions/configure-aws-credentials@v1-node16
        with:
          aws-access-key-id: ${{ secrets.DEPLOY_AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.DEPLOY_AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-west-2

      - uses: aws-actions/amazon-ecr-login@v1

      - run: docker pull $DOCKER_REPO:latest || echo "no current latest image"

      - run: docker build -t $DOCKER_REPO:${{ steps.vars.outputs.sha_short }} .
        working-directory: ./application

      - run: docker tag $DOCKER_REPO:${{ steps.vars.outputs.sha_short }} $DOCKER_REPO:latest

      - run: docker push $DOCKER_REPO:${{ steps.vars.outputs.sha_short }}

      - run: docker push $DOCKER_REPO:latest
```
{% endraw %}

**`.github/workflows/deploy-task.yml`**

{% raw %}
```yaml
name: Deploy Task

on:
  push:
    branches: [main]
    # Put a path here for the folder to watch for changes
    paths: [task/]
  workflow_dispatch:
    inputs:
      environment:
        type: environment
        description: The environment to deploy to (select an -application environment).

jobs:
  detect-environments:
    runs-on: ubuntu-latest
    outputs:
      environments: ${{ steps.environments.outputs.result }}
    steps:
      - uses: actions/github-script@v6
        id: environments
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          result-encoding: json
          script: |
            if (context.payload?.inputs?.environment) return [context.payload?.inputs?.environment];
            const {data: {environments}} =
              await github.request(`GET /repos/${process.env.GITHUB_REPOSITORY}/environments`);
            return environments.map(e => e.name).filter(e => e.indexOf('-application') != -1)

  deploy:
    runs-on: ubuntu-latest
    env:
      DOCKER_REPO: ${{ secrets.DEPLOY_DOCKER_REPOSITORY }}
    needs: [ detect-environments ]
    strategy:
      matrix:
        environment: ${{ fromJSON(needs.detect-environments.outputs.environments) }}
    environment: ${{ matrix.environment }}
    steps:
      - uses: actions/checkout@v3

      - id: vars
        run: echo "sha_short=$(git rev-parse --short HEAD)" >> $GITHUB_OUTPUT

      - run: |
          curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
          unzip -q awscliv2.zip
          sudo ./aws/install --update
          sudo apt-get update
          sudo apt-get install -y rsync

      - uses: aws-actions/configure-aws-credentials@v1-node16
        with:
          aws-access-key-id: ${{ secrets.DEPLOY_AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.DEPLOY_AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-west-2

      - uses: aws-actions/amazon-ecr-login@v1

      - run: docker pull $DOCKER_REPO:latest || echo "no current latest image"

      - run: docker build -t $DOCKER_REPO:${{ steps.vars.outputs.sha_short }} .
        working-directory: ./task

      - run: docker tag $DOCKER_REPO:${{ steps.vars.outputs.sha_short }} $DOCKER_REPO:latest

      - run: docker push $DOCKER_REPO:${{ steps.vars.outputs.sha_short }}

      - run: docker push $DOCKER_REPO:latest
```
{% endraw %}

### RDS autoscaling

RDS database autoscaling is now enabled in all aws environments. The autoscaling_min_capacity & autoscaling_max_capacity are
configure in the `.config.<env>.tfvars` terraform config file.

The below config will create at least one writer and one reader node instance. A maximum of 3 additional reader node will be created
based on the autoscaling policy which default set to 70% CPUUtilization.

```
resources = {
  database = {
    count                        = 2
    class                        = "db.t4g.large"
    autoscaling_enabled          = true
    autoscaling_min              = 0
    autoscaling_max              = 3
    performance_insights_enabled = true
  }
```



### Synthetics Canaries

There are 4 canaries created in each aws environment. `datasette` , `datasette-tiles`, `status`, `www`

These are healthchecks to ensure the defined endpoints are returning status code within the range of `200 - 299`, otherwise it will raised an aws alarm.

The canary template is written in node.js

{% raw %}
```
const { URL } = require('url');
const synthetics = require('Synthetics');
const log = require('SyntheticsLogger');
const syntheticsConfiguration = synthetics.getConfiguration();
const syntheticsLogHelper = require('SyntheticsLogHelper');
const { hostname } = require('os');

const loadBlueprint = async function () {

    // Set screenshot option
    let takeScreenshot = ('${enablescreenshot}' === 'true')
    /* Disabling default step screen shots taken during Synthetics.executeStep() calls
     * Step will be used to publish metrics on time taken to load dom content but
     * Screenshots will be taken outside the executeStep to allow for page to completely load with domcontentloaded
     * You can change it to load, networkidle0, networkidle2 depending on what works best for you.
     */
    syntheticsConfiguration.disableStepScreenshots();
    syntheticsConfiguration.setConfig({
       continueOnStepFailure: true,
       includeRequestHeaders: true, // Enable if headers should be displayed in HAR
       includeResponseHeaders: true, // Enable if headers should be displayed in HAR
       restrictedHeaders: [], // Value of these headers will be redacted from logs and reports
       restrictedUrlParameters: [] // Values of these url parameters will be redacted from logs and reports

    });

    let page = await synthetics.getPage();

    let hostnames = [];
    if ('${appname}' == "www") {
        hostnames = ['https://${hostname}','https://${hostname}/dataset','https://${hostname}/entity','https://${hostname}/map','https://${hostname}/docs','https://${hostname}/entity.json?limit=10','https://${hostname}/dataset.json'];
        takeScreenshot = false;
    } else {
        hostnames = ['https://${hostname}'];
    }

    for (const url of hostnames) {
        await loadUrl(page, url, takeScreenshot);
    }
};

// Reset the page in-between
const resetPage = async function(page) {
    try {
        await page.goto('about:blank',{waitUntil: ['load', 'networkidle0'], timeout: 30000} );
    } catch (e) {
        synthetics.addExecutionError('Unable to open a blank page. ', e);
    }
}

const loadUrl = async function (page, url, takeScreenshot) {
    let stepName = null;
    let domcontentloaded = false;

    try {
        if (url.includes("/entity.json?limit=10")) {
            stepName = "Entity API Check";
        }
        else if (url.includes("/dataset.json")){
            stepName = "Dataset API Check";
        }
        else {
            stepName = url;
        }
    } catch (e) {
        const errorString = 'Error parsing url:' + url + e;
        log.error(errorString);
        /* If we fail to parse the URL, don't emit a metric with a stepName based on it.
           It may not be a legal CloudWatch metric dimension name and we may not have an alarms
           setup on the malformed URL stepName.  Instead, fail this step which will
           show up in the logs and will fail the overall canary and alarm on the overall canary
           success rate.
        */
        throw e;
    }

    await synthetics.executeStep(stepName, async function () {
        const sanitizedUrl = syntheticsLogHelper.getSanitizedUrl(url);

        /* You can customize the wait condition here. For instance, using 'networkidle2' or 'networkidle0' to load page completely.
           networkidle0: Navigation is successful when the page has had no network requests for half a second. This might never happen if page is constantly loading multiple resources.
           networkidle2: Navigation is successful when the page has no more then 2 network requests for half a second.
           domcontentloaded: It's fired as soon as the page DOM has been loaded, without waiting for resources to finish loading. Can be used and then add explicit await page.waitFor(timeInMs)
        */
        const response = await page.goto(url, { waitUntil: ['domcontentloaded'], timeout: 30000});
        if (response) {
            domcontentloaded = true;
            const status = response.status();
            const statusText = response.statusText();

            logResponseString = 'Response from url:' + sanitizedUrl +  'Status:' + status + 'Status Text:' + statusText;

            //If the response status code is not a 2xx success code
            if (response.status() < 200 || response.status() > 299) {
                throw new Error('Failed to load url: ' + sanitizedUrl);
            }
        } else {
            const logNoResponseString = 'No response returned for url: ' + sanitizedUrl;
            log.error(logNoResponseString);
            throw new Error(logNoResponseString);
        }
    });

    // Wait for 15 seconds to let page load fully before taking screenshot.
    if (domcontentloaded && takeScreenshot) {
        await page.waitFor(15000);
        await synthetics.takeScreenshot(stepName, 'loaded');
        await resetPage(page);
    }
};

let hostnames = [];

exports.handler = async () => {
    return await loadBlueprint();
};
```
{% endraw %}

aws alarm status

* OK - The metric or expression is within the defined threshold.
* ALARM - The metric or expression is outside of the defined threshold.

The canary alarm condition is currently set to `SuccessPercent < 100 for 2 datapoints within 10 minutes`