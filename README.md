# Tiamat Backend
Tiamat is a research project by the RESHAPE Lab focused on creating an AI-powered assistant to support novice programmers through interactive, personalized feedback. This repository contains the backend services for the Tiamat system.

The services provided by this repository powers the frontend for the tool, which can be found [here](https://github.com/RESHAPELab/tiamat-vscode).

If you want to learn more about the RESHAPE Lab, visit our [website](https://www.reshapelab.site/).

## REST API

The backend's main service is a REST API, which is accessed by the frontend. This section outlines the features and services provided by the REST API.

### Features

The REST API supports the following features:
- Prompting Tiamat
- Collecting feedback on responses
- Managing available personas for Tiamat to use
- Managing personalized prompts for users

### Reference

If you would like to use the REST API, the reference can be found in [`/docs/api`](/docs/api/README.md).

## Technologies Used

## Directory Structure
This section provides a brief description of each of the main directories in this project.

- [`/api`](/api/) - this is a Flask app which runs the REST API
- [`/docs`](/docs/) - this directory contains documentation for the REST API as well as the evaluation component
- [`/llm`](/llm/) - this directory contains the main prompt engineering and LLM calling needed for this project
- [`/test`](/test/) - this directory contains everything related to evaluation and testing of the LLM component
- [`/ui`](/ui/) - this is a simple React app which can communicate with the REST API, providing a UI for managing personas

## Setup

### Docker
This project has been set up to be containerized and run in Docker. We highly recommend that you use Docker to run everything. If you do not have Docker set up, you can find instructions [here](https://www.docker.com/get-started/).

### Environment Variables
Once you have Docker installed, you will need to set some environment variables. There are two .env files to be set up, one in [`/api`](/api/) and one in [`/ui`](/ui/). There should be a `.env.template` file in these directories. Copy it, rename it to `.env`, and fill in the required values Note that you will need to create an OpenAI API Key.

### How to Run
Once the environment variables are set, the project should be ready to run. In the top-level directory, run the following command:

```bash
docker-compose --profile dev up --build
```

This will run the project in a development environment, providing you access to features like hot reloading. If you are deploying this to a production server, change the `--profile dev` to `--profile prod`.

## Testing

There are some testing features available, including an LLM-as-a-judge tool and a command line tool to directly interact with Tiamat. More information can be found in [`/docs/testing`](/docs/testing/README.md). 

## Questions?

If you have any questions, feel free to reach out to [@pehilbert](https://github.com/pehilbert).