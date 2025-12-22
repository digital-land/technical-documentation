---
title: Testing Guidance
---

Testing is an essential part of quality assurance. If we cannot test our code then we cannot be confident that it is achieving what it needs to do.

## Types Of Testing

Throughout our codebase there are a number of different types of testing that we use. These definitions often differ between projects and teams. This set of definitions is what we are committing to as a team to help. understand what tests are needed and where they should be stored.

### Unit

Unit tests should always test the smallest piece of code that can be logically isolated in a system. This means that we can ensure the smallest piece of code meets its requirements. A unit test should mock its dependencies and shouldn't rely on a file system or a database to run. Altering how code is written can help remove these dependencies or make mocking easier. Larger functions/methods which combine a lot of units of code may not be appropriate to test with a unit test. In these cases Integration tests should be used.

### Integration

Integration tests should still focus on a single function or method but they should include dependencies such as a file system a database or multiple pieces of our code so that we can ensure our code works as part of a larger system. Mocking may still be necessary for external systems such as APIs that we don't control to ensure consistent results.

### Acceptance

Acceptance tests should. reflect acceptance criteria we set before picking up pieces of development. It is not a developers sole responsibility to craft this criteria and instead should be produced with the help of product managers, technical leads and designers. These will mostly likely mimic exactly how a user is expected to interact with the system, whether that be through running commands or a user interface. These tests are much more likely to be grouped by feature or user story rather than resembling the code base.

### Performance

Performance tests allow us to focus on optimising a particular part of a process. They will not be ran as part of every PR as they are not based on acceptance criteria but they should be. ran semi-regularly to help us ensure that our code isn't becoming bloated and slow over time.

## Testing Structure

there are number of ways to structure tests inside of a repository and elsewhere which help tests stay manageable, enabling developers to easier pick up and change the codebase. We have decided to used a standard structure for the majority of our repositories to aid in this. This is not the only way you can structure tests but by being consistent it is easier to work on different areas of our system.

In all of our repos tests are stored in the root in a folder called tests and all the project code should be stored in a different folder in the root directory. E.g. For a python based application:

```
app
  - routers
    - example_1.py
  - example_2.py
tests
  - unit
  - integration
  ...
```

### Unit & Integration Tests

Both unit and integration tests focus on testing a piece of code, whether than be a large function running a complex set of tasks or a tiny function applying a simple bit of logic. Hence the structure of these directories should exactly match that of the application/package directory.

```
app
  - functions
    - functions_1.py
  - functions_2.py
tests
  - unit
    - functions
      - test_functions_2.py
    - test_fucntions_2.py
  - integration
    - functions
      - test_functions_2.py
    - test_fucntions_2.py
```
There may be test files missing if there's no relevant functions for unit testing and/or integration testing in the files.

### Acceptance Tests

Acceptance tests will be based on the acceptance criteria of work that is given to us. This should and often will be written from the perspective of a user or a process using the code and hence may contain multiple steps hitting various bits of applications or code bases. Because of this the test directory doesn't have a prescribed structure. Where possible it is best to organise by feature and/or user story.

```
app
  - functions
    - functions_1.py
  - functions_2.py
tests
  - acceptance
    - feature_1
      - test_user_story_1.py
    - test_user_story_2.py
```
### Adding `conftest.py` File

The `conftest.py` file in a Python project is a centralized location for defining shared fixtures and configuration for your tests. It provides:

- **Shared Resources**: Setting up shared resources like database connections, mock clients, or application instances.
- **Code Reusability**: Reducing code duplication by providing reusable fixtures.
- **Clarity**: Maintaining test clarity by isolating setup logic from test cases.

##### Best Practices for `conftest.py`

1. **Keep It Focused**
   - Only include shared configurations and fixtures. Avoid adding test cases or unrelated code.

2. **Name Fixtures Clearly**
   - Use descriptive names to indicate their purpose (e.g., `temp_file`, `mock_service`).

3. **Use Appropriate Scopes**
   - Choose the right fixture scope (`function`, `class`, `module`, `session`) based on how long the fixture should persist.

4. **Minimize Side Effects**
   - Ensure fixtures clean up resources after execution to prevent interference between tests.


---

### Code Coverage, Linting, and Formatting

To ensure code quality, maintain consistency, and measure testing effectiveness, we can try including steps for **coverage**, **linting**, and **formatting** as part of the testing workflow.

For example, we can add this in a `Makefile` or CI pipeline:

```makefile
test: lint test-coverage

test-coverage:: coverage-unit coverage-integration

coverage-unit:
	pytest --cov=src tests/unit/

coverage-integration:
	pytest --cov=src --cov-append --cov-fail-under=90 tests/integration/

lint:: black-check flake8

black-check:
	black --check .

black:
	black .

flake8:
	flake8 .

```

## Testing Information By Language

As with anything there are additional complexities for each language. Below attempts to outline some general practices we have for each language

### Python

The majority of our codebase is python orientated and hence testing in python is essential. The key frameworks/pakages we use are:

* `pytest` - this is used consistently as the main framework to run tests. `pytest` allows us to use assertions which make the tests more readable than the standard python `unittest` framework. It's extremely common for this to. be. used to test. python code. It's fixtures make it much easier to deal with test dependencies and it has loads of extensions for different python frameworks.
* `playwright` -  this is available for multiple languages. It helps us write acceptance tests which interact with our applications as a user would. This helps us ensure that changes do not break user journeys.

#### Structuring a python test file

We covered structuring a test directory above, for keeping files tidy and consistent we explain how to structure a python test file. This is primarily aimed at unit & integration tests where each. tests focusses on a specific function or method but there may be some useful parts for acceptance tests.

For a python file `application/functions/function_1.py`:

```
def add_function(a,b):
    return a + b
```
the associaed test fille `tests/unit/functions/test_function_1.py`

```
def test_add_function_add_two_numbers():
```

Each function will represent a single test and must begin with test for `pytest` to pick it up. the function name should always represent what the test is attempting to do. For unit & integration tests of functions this should always be the format `test_<function name>_<behaviour>` where the behaviour is what you're testing the function does.

When testing class methods this should be `test_<method name>_<behaviour>` if there are multiple classes in the file being with. the same method name then we suggest structuring them into classes, this is purely an organisational thing there aren't any. other advatages to using test classes with pytest because of the fixtures system.

E.g. if you had a module `application/classes.py`:

```
class ClassOne:
    def process(self):
        print('do something')
        return

class ClassTwo:
    def process(self):
        print('do something else')
        return

```

Then to structure the test file `tests/unit/test_classes.py`:

```
class TestClassOne:
    def test_process_test_something(self):
        .....

class TestClassTwo:
    def test_process_test_something_else(self):
        .....
```


## Testing FastAPI Applications

FastAPI provides built-in tools and conventions that simplify testing APIs.
### `TestClient`

FastAPI includes a `TestClient` utility (via Starlette) to simulate HTTP requests.

```python
from fastapi.testclient import TestClient

# Create a test client for the FastAPI app
client = TestClient(app)

def test_endpoint():
    response = client.get("/endpoint_api")
    assert response.status_code == 200
    assert response.json() == {"key": "value"}  # Replace with your expected response
```


### `Testcontainers`


**Testcontainers** is a library that helps you create lightweight, disposable containers for testing. It is particularly useful for testing services like databases without mocking, ensuring your tests run in a real-world environment.

### Prerequisites

*   **Docker Desktop** (or any Docker runtime)
*   **Python >= 3.8**

### Why Testcontainers?

1.  **Real Services**: Test against actual instances of databases, queues, etc.
2.  **Isolation**: Each test runs in its own container, avoiding conflicts.
3.  **Consistency**: Ensures the test environment matches production as closely as possible.

### Example Usage with LocalStack Container. You can use Testcontainers to spin up a LocalStack container, which emulates AWS services

```python
from testcontainers.localstack import LocalStackContainer
import boto3

def localstack_container():
    # Start LocalStack container
    with LocalStackContainer() as localstack:
        yield localstack

def s3_client(localstack_container):
    # Create an S3 client using the LocalStack endpoint
    s3 = boto3.client(
        "s3",
        endpoint_url=localstack_container.get_url(),
        region_name=os.environ["AWS_DEFAULT_REGION"],
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )
    return s3


