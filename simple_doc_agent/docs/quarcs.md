# quarcs

_Auto-generated documentation (generated on )_

---

## 🛡️ Security Audit

✅ No immediate security risks (hardcoded secrets or insecure ports) detected.


---
---

## Overview

- **Type:** Python Application
- **Python Version:** ^3.11

---

## Dependencies

| Package | Version |
|--------|---------|

| poetry-dynamic-versioning | ^1.1.0 |

| pandas | ^2.2.3 |

| bottleneck | >=1.3.2 |

| requests | ^2.32.3 |

| faststream | ^0.5.33 |

| netcdf4 | ^1.7.2 |

| asyncio | ^3.4.3 |

| aiohttp | ^3.11.11 |

| aio-pika | ^9.5.4 |

| python-dotenv | ^1.0.1 |

| anyio | ^4.8.0 |

| pytest | ^8.3.4 |

| pytest-mock | ^3.14.0 |

| pytest-asyncio | ^0.25.2 |

| pytest-cov | ^6.0.0 |

| base-data-object | 0.0.5 |

| bodctools | ^1.1.0 |

| filelock | ^3.17.0 |

| celery | ^5.4.0 |


---

## Python Code

### File: quarcs/__init__.py


#### Module <module>

quarcs Python package.



### File: quarcs/models/messages.py


#### Module <module>

python models of the rabbitmq messages.


#### ClassDef QC_Mapping

This class maps qc calls to the parameters needed.


#### ClassDef Task

This class models a Celery task.


#### ClassDef Content

This class models the RabbitMQ JSON payload.

We expect the following attributes:
- deployment_id: The deployment ID.
- rxf_location: A valid file location for the RXF.
- qc_mapping: A list of mappings between the QC URLs and their parameters.
- fileref: A list of filerefs.
- tasks: A list of Celery tasks.
- qc_rxf_snapshot_name: The name for the QC RXF snapshot.



### File: quarcs/qc.py


#### Module <module>

Main app to start the processing.


#### FunctionDef process_tasks

Receives the filrefs in kwargs and sends tasks to Celery.


#### FunctionDef run_async_in_thread

Helper function to run async functions inside threads.



### File: quarcs/util/__init__.py


#### Module <module>

module section for util.



### File: quarcs/util/call_qc.py


#### Module <module>

helper class.


#### ClassDef ChunkedResponse

Wrapper class to hold a list of QcResponse objects.


#### ClassDef QcResponse

Class to hold response data from QC tests.


#### ClassDef FetchQc

A class for dealing with fetching QC flags.


#### FunctionDef __init__

ChunkedResponse init.


#### FunctionDef get_parameters

Get the list of parameters related to the qc response chunks.


#### FunctionDef get_test_path

Get the test url related to the qc response chunks.


#### FunctionDef get_full_data

Get an aggregated list of the data from all the qc response chunks.


#### FunctionDef is_ok

Return True if all QcResponses were successful. Else False.


#### FunctionDef is_empty

Return True if there are no responses in this object.

Returns:
    bool: True if there are no responses assigned to this object.


#### FunctionDef __init__

QcResponse init.

Args:
    url (str): Test URL.
    parameters (list|str): List of parameters.
    flags (dict): JSON response from QC test.
    ok (bool): Whether or not the request was successful or not.


#### FunctionDef _parse_flags

Get the flag data in a nice format.

Args:
    flags (str): Flag response from the QC tests.


#### FunctionDef get_test_path

Remove domain and store only the test name.

e.g. http://localhost:5003/global-range-temp -> /global-range-temp

Args:
    url (str): QC test url (including domain name).

Returns:
    str: Test path.


#### FunctionDef __init__

Setup class with url and data.



### File: quarcs/util/config.py


#### Module <module>

Read configs from OS env.


#### FunctionDef buildRabbitMqUrl

Build the url for the rabbitmq instance.

Returns:
    str: The connection string for rabbitmq.



### File: quarcs/util/rxf_qc.py


#### Module <module>

Class to call and update the rxf.


#### ClassDef QcRxf

This class deals with fetch and storing the data needed for QC to be run.


#### FunctionDef __init__

Setup class with location of rxf file.

Args:
    deployment_id (Int): Deployment for which qc is requested.
    rxf_location (Path): Location of the RXF file.
    filrefs (list[int]): List of filrefs to filter RXF data.


#### FunctionDef final_qced_rxf

Return the path of the QCed RXF file.


#### FunctionDef load_qc_mappings

Method to load the qc mappings json file.


#### FunctionDef get_rxf_data

Retrieve RXF data for the specified QC mappings.

This method fetches data from the RXF file based on the provided
list of QC_Mapping objects. It populates the data attribute of each
QC_Mapping with the corresponding values from the RXF file.

Args:
    var (list[QC_Mapping]): A list of QC_Mapping objects that specify
                            the parameters for which data should be
                            retrieved.

Returns:
    list[QC_Mapping]: The updated list of QC_Mapping objects with
                    their data attributes populated.


#### FunctionDef get_rxf_object

Get RXF table for a given rxf dataset.


#### FunctionDef filter_dataframe

Filter data based on filrefs that already exist.


#### FunctionDef create_qc_rxf_path

Function to build the qc_rxf file path.

Returns:
    Path: The path of the qc_rxf.


#### FunctionDef create_blank_qc_rxf

Creates a blank QC RXF file.

This function creates a blank QC RXF file with default values from original rxf.


#### FunctionDef qc_rxf_snapshot

Creates a snapshot of the QC RXF file.

Args:
    qc_rxf_path (Path): The path to the original RXF file.
    snapshot_name (str): The name for the snapshot.

Returns:
    Path: The path to the created snapshot.


#### FunctionDef add_qc_to_rxf

Add new rxf data and qc data to qc_rxf.

Args:
    processed_flags: dict[str, list[dict]]: The tests run for each variable.



### File: tests/__init__.py


#### Module <module>

Init file is needed for tests.



### File: tests/test_config.py


#### Module <module>

Testing configs.


#### FunctionDef create_env_file

Fixture for mocking the rabbitmq config.


#### FunctionDef test_rabbitmq_url

Test for checking the Rabbitmq URL.


#### FunctionDef test_custom_rabbitmq_url

Test the construction of a custom RabbitMQ URL using environment variables.


#### FunctionDef test_missing_env_vars

Testing when there are missing env vars.



### File: tests/test_example.py


#### Module <module>

Example test file.


#### FunctionDef test_example

An example test function.



### File: tests/test_qc.py


#### Module <module>

Tests to test qc generation.


#### FunctionDef mock_netCDF4

Fixture to mock netCDF4.Dataset.


#### FunctionDef temp_rxf_file

Fixture for generating temp file.


#### FunctionDef sample_content

Fixture for Content object.


#### FunctionDef mock_logger

Fixture to mock the logger.



### File: tests/test_qc_call.py


#### Module <module>

Test file for call qc functions.


#### FunctionDef sample_data

Generate sample QC mapping data for testing.


#### FunctionDef fetch_qc

Create a FetchQc instance using the provided sample QC mapping data.


#### FunctionDef test_init

Test the initialization of the FetchQc instance with sample data.


#### FunctionDef test_chunked_response_class

Test for the ChunkedResponse class.


#### FunctionDef test_qc_response_class

Test for the QcResponse class.



### File: tests/test_rxf_qc.py


#### Module <module>

Tests to check rxf qc.


#### FunctionDef sample_rxf_file

Create a sample RXF file for testing with predefined data.


#### FunctionDef sample_qc_rxf_file

Create a sample RXF file for testing with predefined data.


#### FunctionDef sample_qc_rxf_file_to_check_appending

Create a sample RXF file for testing with predefined data.


#### FunctionDef sample_rxf_file2

Create a sample RXF file with a group and root variable for testing.


#### FunctionDef empty_qc_rxf

Create an empty QC RXF file for testing.


#### FunctionDef qc_rxf_instance

Create a qc_rxf instance initialized with a sample RXF file.


#### FunctionDef qc_rxf_instance2

Create a qc_rxf instance initialized with a sample RXF file.


#### FunctionDef test_create_blank_qc_rxf_file_exists

Test that create_blank_qc_rxf exits early if the file already exists.


#### FunctionDef test_init

Test the initialization of the qc_rxf instance with a sample RXF file.


#### FunctionDef test_get_rxf_data

Test the retrieval of RXF data from the qc_rxf instance.


#### FunctionDef test_get_rxf_data_with_qc

Test the creation of qc_rxf with existing filrefs data.


#### FunctionDef test_adding_to_existing_qxf

Test the creation of qc_rxf when the qc_vars are not present.


#### FunctionDef test_get_rxf_with_no_data

Test the retrieval of RXF data from the qc_rxf instance and adding to an existing qxf.


#### FunctionDef test_get_rxf_data_with_missing_values

Test to check if flags are generated for missing values.


#### FunctionDef test_get_rxf_data_nonexistent_variable

Test the creation of the QC RXF for a non existent variable.


#### FunctionDef test_add_qc_to_rxf_nonexistent_group

Test the addition of qxf to a non existent group.


#### FunctionDef test_create_qc_rxf_path

Test the creation of the QC RXF file path.


#### FunctionDef test_add_qc_to_rxf_with_no_new_data

Test the addition of qxf to a non existent group.


#### FunctionDef test_add_qc_to_rxf

Test adding QC data to an RXF file.

This test verifies that when QC data is added to an RXF file,
the operation completes successfully and the resulting RXF file
is updated correctly. It checks that the QC variables are created
and that the original data is preserved.

Args:
    qc_rxf_instance: An instance of the `qc_rxf` class initialized
                     with a sample RXF file for testing.
    tmp_path: A temporary directory provided by pytest for creating
              temporary files during the test.

Asserts:
    - The updated RXF file contains the expected QC variables.
    - The original data in the RXF file is preserved.


#### FunctionDef test_add_empty_qc_to_rxf

Test adding an empty QC to an RXF file.

This test verifies that when an empty QC is added to an RXF file,
the operation completes without errors and the resulting qc_rxf file
is correctly updated. It checks that the expected dimensions and
groups are present in the updated RXF file.

Args:
    qc_rxf_instance: An instance of the `qc_rxf` class initialized
                      with a sample RXF file for testing.

Asserts:
    - The updated QC RXF file contains the expected dimensions and groups.
    - No errors are raised during the addition of the empty QC.


#### FunctionDef test_rxf_data_with_no_group

Test the retrieval of RXF data when no group is present in the file.

This test verifies that the `qc_rxf` instance can correctly handle
cases where the RXF file does not contain any groups. It checks
that the data can still be accessed using the root variable path.

Args:
    sample_rxf_file2: A temporary RXF file created for testing,
                       which is expected to have no groups.

Asserts:
    - The retrieved data matches the expected values for the root variable.


#### FunctionDef test_load_qc_mappings_invalid_json

Test handling of invalid JSON format.




---

## CI/CD


### Global Variables

- **DEPLOY_ENVIRONMENT**: null

- **BODCCI_USER**: approc

- **BODCCI_APPS**: /local/approc/apps

- **BODCCI_SYSTEMD**: /local/approc/.config/systemd/user

- **BODCCI_UNIT**: quarcs




### Jobs

- **test**
  - Stage: ['.stages', 'test']
  - Image: python:3.11
  - Runs: on_success

- **Deploy application**
  - Stage: ['.stages', 'deploy']
  - Image: default
  - Runs: on_success



---

## Docker

### Dockerfile: Dockerfile

- **Filename:** Dockerfile

- **Base Image:** python:3.11

- **Exposed Ports:** []

- **Volumes:** []

- **Workdir:** /project

- **Entrypoint:** 

- **Env Vars:** ['POETRY_CACHE_DIR=/tmp/.cache']


### Dockerfile: docker-compose.yml

- **Filename:** docker-compose.yml

- **Base Image:** unknown

- **Exposed Ports:** []

- **Volumes:** []

- **Workdir:** /app

- **Entrypoint:** 

- **Env Vars:** []



---

## Architecture Diagram

```mermaid
<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
quarcs___init___py["Module: __init__.py"]
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
quarcs_models_messages_py["Module: messages.py"]
quarcs_models_messages_py_QC_Mapping["Class: QC_Mapping"]
quarcs_models_messages_py --> quarcs_models_messages_py_QC_Mapping
quarcs_models_messages_py_Task["Class: Task"]
quarcs_models_messages_py --> quarcs_models_messages_py_Task
quarcs_models_messages_py_Content["Class: Content"]
quarcs_models_messages_py --> quarcs_models_messages_py_Content
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
quarcs_qc_py["Module: qc.py"]
quarcs_qc_py_process_tasks["Function: process_tasks"]
quarcs_qc_py --> quarcs_qc_py_process_tasks
quarcs_qc_py_run_async_in_thread["Function: run_async_in_thread"]
quarcs_qc_py --> quarcs_qc_py_run_async_in_thread
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
quarcs_util___init___py["Module: __init__.py"]
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
quarcs_util_call_qc_py["Module: call_qc.py"]
quarcs_util_call_qc_py_ChunkedResponse["Class: ChunkedResponse"]
quarcs_util_call_qc_py --> quarcs_util_call_qc_py_ChunkedResponse
quarcs_util_call_qc_py_QcResponse["Class: QcResponse"]
quarcs_util_call_qc_py --> quarcs_util_call_qc_py_QcResponse
quarcs_util_call_qc_py_FetchQc["Class: FetchQc"]
quarcs_util_call_qc_py --> quarcs_util_call_qc_py_FetchQc
quarcs_util_call_qc_py___init__["Function: __init__"]
quarcs_util_call_qc_py --> quarcs_util_call_qc_py___init__
quarcs_util_call_qc_py_get_parameters["Function: get_parameters"]
quarcs_util_call_qc_py --> quarcs_util_call_qc_py_get_parameters
quarcs_util_call_qc_py_get_test_path["Function: get_test_path"]
quarcs_util_call_qc_py --> quarcs_util_call_qc_py_get_test_path
quarcs_util_call_qc_py_get_full_data["Function: get_full_data"]
quarcs_util_call_qc_py --> quarcs_util_call_qc_py_get_full_data
quarcs_util_call_qc_py_is_ok["Function: is_ok"]
quarcs_util_call_qc_py --> quarcs_util_call_qc_py_is_ok
quarcs_util_call_qc_py_is_empty["Function: is_empty"]
quarcs_util_call_qc_py --> quarcs_util_call_qc_py_is_empty
quarcs_util_call_qc_py___init__["Function: __init__"]
quarcs_util_call_qc_py --> quarcs_util_call_qc_py___init__
quarcs_util_call_qc_py__parse_flags["Function: _parse_flags"]
quarcs_util_call_qc_py --> quarcs_util_call_qc_py__parse_flags
quarcs_util_call_qc_py_get_test_path["Function: get_test_path"]
quarcs_util_call_qc_py --> quarcs_util_call_qc_py_get_test_path
quarcs_util_call_qc_py___init__["Function: __init__"]
quarcs_util_call_qc_py --> quarcs_util_call_qc_py___init__
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
quarcs_util_config_py["Module: config.py"]
quarcs_util_config_py_buildRabbitMqUrl["Function: buildRabbitMqUrl"]
quarcs_util_config_py --> quarcs_util_config_py_buildRabbitMqUrl
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
quarcs_util_rxf_qc_py["Module: rxf_qc.py"]
quarcs_util_rxf_qc_py_QcRxf["Class: QcRxf"]
quarcs_util_rxf_qc_py --> quarcs_util_rxf_qc_py_QcRxf
quarcs_util_rxf_qc_py___init__["Function: __init__"]
quarcs_util_rxf_qc_py --> quarcs_util_rxf_qc_py___init__
quarcs_util_rxf_qc_py_final_qced_rxf["Function: final_qced_rxf"]
quarcs_util_rxf_qc_py --> quarcs_util_rxf_qc_py_final_qced_rxf
quarcs_util_rxf_qc_py_load_qc_mappings["Function: load_qc_mappings"]
quarcs_util_rxf_qc_py --> quarcs_util_rxf_qc_py_load_qc_mappings
quarcs_util_rxf_qc_py_get_rxf_data["Function: get_rxf_data"]
quarcs_util_rxf_qc_py --> quarcs_util_rxf_qc_py_get_rxf_data
quarcs_util_rxf_qc_py_get_rxf_object["Function: get_rxf_object"]
quarcs_util_rxf_qc_py --> quarcs_util_rxf_qc_py_get_rxf_object
quarcs_util_rxf_qc_py_filter_dataframe["Function: filter_dataframe"]
quarcs_util_rxf_qc_py --> quarcs_util_rxf_qc_py_filter_dataframe
quarcs_util_rxf_qc_py_create_qc_rxf_path["Function: create_qc_rxf_path"]
quarcs_util_rxf_qc_py --> quarcs_util_rxf_qc_py_create_qc_rxf_path
quarcs_util_rxf_qc_py_create_blank_qc_rxf["Function: create_blank_qc_rxf"]
quarcs_util_rxf_qc_py --> quarcs_util_rxf_qc_py_create_blank_qc_rxf
quarcs_util_rxf_qc_py_qc_rxf_snapshot["Function: qc_rxf_snapshot"]
quarcs_util_rxf_qc_py --> quarcs_util_rxf_qc_py_qc_rxf_snapshot
quarcs_util_rxf_qc_py_add_qc_to_rxf["Function: add_qc_to_rxf"]
quarcs_util_rxf_qc_py --> quarcs_util_rxf_qc_py_add_qc_to_rxf
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
tests___init___py["Module: __init__.py"]
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
tests_test_config_py["Module: test_config.py"]
tests_test_config_py_create_env_file["Function: create_env_file"]
tests_test_config_py --> tests_test_config_py_create_env_file
tests_test_config_py_test_rabbitmq_url["Function: test_rabbitmq_url"]
tests_test_config_py --> tests_test_config_py_test_rabbitmq_url
tests_test_config_py_test_custom_rabbitmq_url["Function: test_custom_rabbitmq_url"]
tests_test_config_py --> tests_test_config_py_test_custom_rabbitmq_url
tests_test_config_py_test_missing_env_vars["Function: test_missing_env_vars"]
tests_test_config_py --> tests_test_config_py_test_missing_env_vars
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
tests_test_example_py["Module: test_example.py"]
tests_test_example_py_test_example["Function: test_example"]
tests_test_example_py --> tests_test_example_py_test_example
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
tests_test_qc_py["Module: test_qc.py"]
tests_test_qc_py_mock_netCDF4["Function: mock_netCDF4"]
tests_test_qc_py --> tests_test_qc_py_mock_netCDF4
tests_test_qc_py_temp_rxf_file["Function: temp_rxf_file"]
tests_test_qc_py --> tests_test_qc_py_temp_rxf_file
tests_test_qc_py_sample_content["Function: sample_content"]
tests_test_qc_py --> tests_test_qc_py_sample_content
tests_test_qc_py_mock_logger["Function: mock_logger"]
tests_test_qc_py --> tests_test_qc_py_mock_logger
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
tests_test_qc_call_py["Module: test_qc_call.py"]
tests_test_qc_call_py_sample_data["Function: sample_data"]
tests_test_qc_call_py --> tests_test_qc_call_py_sample_data
tests_test_qc_call_py_fetch_qc["Function: fetch_qc"]
tests_test_qc_call_py --> tests_test_qc_call_py_fetch_qc
tests_test_qc_call_py_test_init["Function: test_init"]
tests_test_qc_call_py --> tests_test_qc_call_py_test_init
tests_test_qc_call_py_test_chunked_response_class["Function: test_chunked_response_class"]
tests_test_qc_call_py --> tests_test_qc_call_py_test_chunked_response_class
tests_test_qc_call_py_test_qc_response_class["Function: test_qc_response_class"]
tests_test_qc_call_py --> tests_test_qc_call_py_test_qc_response_class
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
tests_test_rxf_qc_py["Module: test_rxf_qc.py"]
tests_test_rxf_qc_py_sample_rxf_file["Function: sample_rxf_file"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_sample_rxf_file
tests_test_rxf_qc_py_sample_qc_rxf_file["Function: sample_qc_rxf_file"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_sample_qc_rxf_file
tests_test_rxf_qc_py_sample_qc_rxf_file_to_check_appending["Function: sample_qc_rxf_file_to_check_appending"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_sample_qc_rxf_file_to_check_appending
tests_test_rxf_qc_py_sample_rxf_file2["Function: sample_rxf_file2"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_sample_rxf_file2
tests_test_rxf_qc_py_empty_qc_rxf["Function: empty_qc_rxf"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_empty_qc_rxf
tests_test_rxf_qc_py_qc_rxf_instance["Function: qc_rxf_instance"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_qc_rxf_instance
tests_test_rxf_qc_py_qc_rxf_instance2["Function: qc_rxf_instance2"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_qc_rxf_instance2
tests_test_rxf_qc_py_test_create_blank_qc_rxf_file_exists["Function: test_create_blank_qc_rxf_file_exists"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_create_blank_qc_rxf_file_exists
tests_test_rxf_qc_py_test_init["Function: test_init"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_init
tests_test_rxf_qc_py_test_get_rxf_data["Function: test_get_rxf_data"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_get_rxf_data
tests_test_rxf_qc_py_test_get_rxf_data_with_qc["Function: test_get_rxf_data_with_qc"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_get_rxf_data_with_qc
tests_test_rxf_qc_py_test_adding_to_existing_qxf["Function: test_adding_to_existing_qxf"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_adding_to_existing_qxf
tests_test_rxf_qc_py_test_get_rxf_with_no_data["Function: test_get_rxf_with_no_data"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_get_rxf_with_no_data
tests_test_rxf_qc_py_test_get_rxf_data_with_missing_values["Function: test_get_rxf_data_with_missing_values"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_get_rxf_data_with_missing_values
tests_test_rxf_qc_py_test_get_rxf_data_nonexistent_variable["Function: test_get_rxf_data_nonexistent_variable"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_get_rxf_data_nonexistent_variable
tests_test_rxf_qc_py_test_add_qc_to_rxf_nonexistent_group["Function: test_add_qc_to_rxf_nonexistent_group"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_add_qc_to_rxf_nonexistent_group
tests_test_rxf_qc_py_test_create_qc_rxf_path["Function: test_create_qc_rxf_path"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_create_qc_rxf_path
tests_test_rxf_qc_py_test_add_qc_to_rxf_with_no_new_data["Function: test_add_qc_to_rxf_with_no_new_data"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_add_qc_to_rxf_with_no_new_data
tests_test_rxf_qc_py_test_add_qc_to_rxf["Function: test_add_qc_to_rxf"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_add_qc_to_rxf
tests_test_rxf_qc_py_test_add_empty_qc_to_rxf["Function: test_add_empty_qc_to_rxf"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_add_empty_qc_to_rxf
tests_test_rxf_qc_py_test_rxf_data_with_no_group["Function: test_rxf_data_with_no_group"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_rxf_data_with_no_group
tests_test_rxf_qc_py_test_load_qc_mappings_invalid_json["Function: test_load_qc_mappings_invalid_json"]
tests_test_rxf_qc_py --> tests_test_rxf_qc_py_test_load_qc_mappings_invalid_json
</pre></div>

## Test Coverage

```testcoverage
{'test_coverage': [{'name': 'quarcs/__init__.py', 'line_rate': 100.0, 'branch_rate': 0.0}, {'name': 'quarcs/models/messages.py', 'line_rate': 100.0, 'branch_rate': 0.0}, {'name': 'quarcs/qc.py', 'line_rate': 71.0, 'branch_rate': 0.0}, {'name': 'quarcs/util/__init__.py', 'line_rate': 100.0, 'branch_rate': 0.0}, {'name': 'quarcs/util/call_qc.py', 'line_rate': 98.0, 'branch_rate': 0.0}, {'name': 'quarcs/util/config.py', 'line_rate': 100.0, 'branch_rate': 0.0}, {'name': 'quarcs/util/rxf_qc.py', 'line_rate': 92.0, 'branch_rate': 0.0}], 'summary_coverage': '89%'}