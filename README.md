# Plaza DevOps Coding Assignment

This repository contains the code for setting up a GKE cluster using Terraform and a sample web application. Your task is to containerize the web application, create a Helm chart for deployment, and update the GitHub Actions workflow file for automated testing, building, and deploying the container image to the Kubernetes cluster.

## Repository Structure

- `infrastructure`: This directory contains the Terraform code for setting up the GKE cluster. This directory will not be modified in the tasks.
- `services`: This directory contains Terraform code for deploying services to the Kubernetes cluster. This directory will not be modified in the tasks.
- `webapp`: This directory contains the source code for the web application and tests.
  - `src`: This directory contains the main Python file for the web application.
  - `tests`: This directory contains test cases for the web application.
- `helm-chart`: This directory will contain the Helm chart for deploying the web application. You'll need to create this as part of the assignment.
- `modules/helm_webapp`: This directory is where you will create the Terraform module for deploying the web application using the Helm chart.
- `.github/workflows`: This directory contains the GitHub Actions workflow file that you'll need to update.

## Getting Started

### Prerequisites

- Python 3.x
- Docker ([with Kubernetes enabled](https://docs.docker.com/desktop/features/kubernetes/))
- Helm
- Terraform

### Web Application

The web application is a simple app that displays data from the Star Wars API. You can explore the API using `curl https://swapi.info`.

To set up and run the web application, follow these steps:

```bash
# Navigate to the 'webapp' directory
cd webapp

# Create a Python virtual environment and activate it
python -m venv env
source env/bin/activate

# Install the necessary dependencies
pip install -r requirements.txt

# Start the application using Uvicorn
uvicorn src.app:app --reload
```

The application will be accessible at http://localhost:8000.

## Testing

To run the tests for the web application, use the following steps:

```bash
# Navigate to the 'webapp' directory
cd webapp

# Install the necessary dependencies
pip install -r requirements.txt

# Run the tests
pytest tests/
```

The tests will run and their results will be displayed in the terminal.

For local development of Terraform, you can use Docker Desktop with Kubernetes enabled to test your module. Setup kube config file path by `export KUBE_CONFIG_PATH=~/.kube/config` and run `terraform apply` in the `services` directory to verify successful installation.

## Instructions for the Candidate

Your tasks are as follows:

1. Clone the repository. You can choose to fork it instead, but this might cause complications during the assignment presentation.
2. **Dockerfile**: Create a Dockerfile in the `webapp` directory to containerize the web application. Ensure that the Dockerfile installs all necessary dependencies and starts the application when a container is run.

```bash
# In the 'webapp' directory
echo "FROM python:3.10" > Dockerfile
# Add the necessary statements to the Dockerfile in order to be able to build a working image.
```

3. **Add Features**:
   1. Currently, the `/` endpoint has a hard-coded message. Make this message configurable using a configuration parameter in the Helm values file.
   2. Currently, the `/data` endpoint is hard-coded to fetch the first entry in the `people` database. Get the ID from a query parameter instead of a hard-coded value.
   3. Add a new endpoint `top-people-by-bmi` that fetches all people from the Star Wars API and returns a list of the 20 people with the highest BMI, sorted by BMI. BMI is calculated as `mass / height^2`.

You might find the [FastAPI](https://fastapi.tiangolo.com/tutorial/) documentation useful here.

4. **Test Cases**: Enhance the existing test case in `webapp/tests/test_get_star_wars_data.py` (`test_get_star_wars_data`) by adding more test cases to cover different scenarios, error conditions, and edge cases. Write additional test cases for the new and updated endpoints.

```bash
# Example: Adding test cases in 'webapp/tests/test_get_star_wars_data.py'

def test_api_http_error():
    # Test case for API HTTP error. For example, fetch a Star Wars character with an ID that doesn't exist.
    pass
```

5. **Helm Chart**: Update the helm chart under the `helm-chart` directory to implement the configurable hello world message. Add a Helm value such as `helloWorldMessage` and make it available in the web application through some mechanism.

```bash
# In the 'helm-chart' directory
# Update the 'values.yaml' file and other necessary files in the chart
```

6. **Terraform Module**: Create a Terraform module called `helm_webapp` under the `modules` directory. This module should:
  - Include a Helm chart resource that installs your application in the Kubernetes cluster
  - Implement a variable to set the Helm value `helloWorldMessage`

```hcl
# Example structure for modules/helm_webapp
├── modules
│   └── helm_webapp
│       ├── main.tf
│       ├── variables.tf
│       └── providers.tf
```

Note that you should only modify files in the `modules/helm_webapp` directory and leave both the `services` and `infrastructure` directories unchanged.

7. **Workflow**: Update the GitHub Actions workflow file in `.github/workflows` to automatically build the Docker image, push it to the container registry, and deploy the web application to the GKE cluster using the Helm chart.

```bash
# In the '.github/workflows' directory
# Update the workflow file with necessary steps and actions. We have added comments specifying suitable locations for such steps.
# The steps syntax to use will be the following:

  - name: Step description
    run: |
      shell command 1
      shell command 2
      shell command 3
      
# You can use environment variables defined earlier in the workflow just as you would use them in the shell.
```

8. During the assignment presentation, you will be asked to push the code to a branch named `candidate-<your-name>` of the original repository. Replace the `<your-name>` with your actual name, using only alphanumeric characters and hyphens (e.g., `candidate-pricer-ab`). Avoid spaces or special characters, and ensure the branch name is all lowercase letters. The provided GitHub CI/CD workflow expects the branch to be named this way. You will be given write access to the repository before or during the presentation. You will be asked to create a Pull Request from the branch. If you forked the repository, you will still need to create the Pull Request from the branch of the original repository, since the CI/CD workflow cannot run from a fork.
9. Make sure to have your development environment and GitHub access setup before the presentation, so that you can push updates during the presentation if anything fails or doesn't work as expected.
