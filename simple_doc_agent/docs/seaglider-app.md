# seaglider_app

_Auto-generated documentation (generated on )_

---

## 🛡️ Security Audit

> [!WARNING]
> Potential security risks detected in configuration files.


### 📄 `docker-compose.yml`

| Type | Item | Risk Level | Details |
| :--- | :--- | :--- | :--- |

| **Env Leak** | `rmq_pass` | 🟡 WARNING | gue*** |

| **Env Leak** | `qc_route_key` | 🟡 WARNING | qc*** |





---
---

## Overview

- **Type:** Python Application
- **Python Version:** ^3.10

---

## Dependencies

| Package | Version |
|--------|---------|

| dbdreader | 0.4.11 |

| gevent | 23.7.0 |

| gunicorn | 21.2.0 |

| apds-flask-app | 2.2.3 |

| apds-platforms | 1.5.4 |

| apds-formats | 7.4.1 |

| messaging | * |

| celery | ^5.3.1 |

| alive-progress | ^3.1.4 |

| numpy | <2 |

| missing-file-manager | ^0.0.1 |

| tenacity | ^9.1.2 |


---

## Python Code

### File: sandbox.py


#### Module <module>

Sandbox for local testing.



### File: seaglider_app/__init__.py


#### Module <module>

Import the app.



### File: seaglider_app/apis/__init__.py


#### Module <module>

Import blueprints.



### File: seaglider_app/apis/cov_json.py


#### Module <module>

Handles the routes for coverage json output files.


#### ClassDef CovJsonSummary

An endpoint to get information on coverage json file statuses.


#### FunctionDef get

Generates a short summary of coverage json file statuses for deployments.

Args:
    only: An optional filter for specific deployments. Set to "active" to get info for active deployments only.

Returns:
    A JSON representation of file info.



### File: seaglider_app/apis/file_transfers.py


#### Module <module>

Handles the routes for transferring files.


#### ClassDef TransferRawZipFiles

An endpoint to allow the transfer of a zip file to erddap.


#### FunctionDef post

Triggers a remote celery worker to zip raw files within the given deployment folder.

Args:
    deployment (int): The deployment id.

Returns:
    response: 200.



### File: seaglider_app/apis/metadata_json.py


#### Module <module>

Handles the route for creating the Metadata JSON file.


#### ClassDef ProcessMetadataJSON

An endpoint to allow (re-)generation of just the Metadata JSON file.


#### FunctionDef post

Generate the Metadata JSON file for a deployment.

Args:
    deployment (int): The deployment id.

Returns:
    response: The path to the JSON file.



### File: seaglider_app/apis/ocean_gliders.py


#### Module <module>

Handles the route for creating an OceanGliders 1.0 format output.


#### ClassDef ProcessOceanGliders

An endpoint to allow (re-)generation of just the OceanGliders file.


#### ClassDef OceanGlidersSummary

An endpoint to get information on OG1 file statuses.


#### FunctionDef post

Requests an OceanGliders file for a deployment.

Args:
    deployment (int): The deployment id.

Returns:
    response: A JSON response representing the OceanGliders format.


#### FunctionDef get

Generates a short summary of OG1 file statuses for deployments.

Args:
    only: An optional filter for specific deployments. Set to "active" to get info for active deployments only.

Returns:
    A JSON representation of file info.



### File: seaglider_app/apis/rxf.py


#### Module <module>

Endpoint for producing an RXF file.


#### ClassDef ProcessRxf

Class to Process an RXF files from raw files.


#### ClassDef RXFSummary

An endpoint to get information on RXF file statuses while excluding RXF QC files.


#### ClassDef RxfQcSummary

An endpoint to get information on RXF QC file statuses.


#### FunctionDef post

Post endpoint to trigger an RXF processing.


#### FunctionDef get

Generates a short summary of RXF file statuses for deployments.

Args:
    only: An optional filter for specific deployments. Set to "active" to get info for active deployments only.

Returns:
    A JSON representation of file info.


#### FunctionDef get

Generates a short summary of RXF QC file statuses for deployments.

Args:
    only: An optional filter for specific deployments. Set to "active" to get info for active deployments only.

Returns:
    A JSON representation of file info.



### File: seaglider_app/apis/seaglider.py


#### Module <module>

Endpoint for performing a full reprocess of a Seaglider deployment.


#### ClassDef ProcessSeaglider

Class to handle a full re-process of a Seaglider.


#### ClassDef RegisterSeaglider

Class to register new Seagliders.


#### FunctionDef post

Post method to trigger a full reprocess.


#### FunctionDef post

Post method to trigger register a new Deployment queue.



### File: seaglider_app/apis/source.py


#### Module <module>

Endpoint for tracking source data files.


#### ClassDef FileFormat

This class deals with formats for files.


#### ClassDef SourceSummary

An endpoint to get information on source file statuses.


#### FunctionDef get

Generates a short summary of source data file statuses for deployments.

Args:
    only: An optional filter for specific deployments. Set to "active" to get info for active deployments only.

Returns:
    A JSON representation of file info.



### File: seaglider_app/apis/symlink_generation.py


#### Module <module>

Endpoint for symlink generation.


#### ClassDef symlinkGeneration

An endpoint to allow create symlinks to files that are archived.


#### FunctionDef post

Create a symlink for a file of a Deployment.

Args:
    deployment (int): The deployment id.
    symlink_name (str): The name of the symlink to create.
    orig_location (str): The actual location of the file to which the symlink is created.
    mode (str): The mode of the deployment

Returns:
    response: A response of the process of creating symlink.



### File: seaglider_app/core/__init__.py


#### Module <module>

Import Processing class.



### File: seaglider_app/core/processing.py


#### Module <module>

Process Seagliders.


#### FunctionDef rxf_snapshot

Create a temporary "snapshot" copy of an RXF file that other applications can use without it being updated.

Args:
    rxf_path: The path to the RXF file to copy.
    snapshot_name: A unique name for the new snapshot.
    overwrite: If an existing snapshot with this name exists, should we overwrite it?

Returns:
    The path to the generated snapshot file.


#### FunctionDef segment_snapshot

Create an RXF snapshot (see rxf_snapshot above) that represents data from a specific segment.

For Seagliders, we assume that one source NetCDF = one segment, so we can use the source file stem in our name.

Args:
    rxf_path: The path to the RXF file to copy. This must contain the target segment, but can also include more.
    segment: The name of the segment to use in the filename, this is usually the Source NetCDF file stem.

Returns:
    The path to the generated snapshot file.


#### FunctionDef skip_corrupted_file

Move a NetCDF file that has been identified as corrupted into a separate directory and log a warning.

Args:
    file: The path to the source file to move to the SKIPPED/CORRUPTED directory.


#### ClassDef ProcessingError

Raised when an error occurs during processing of a deployment.


#### ClassDef Processing

Class to process Seaglider deployments.


#### FunctionDef __init__

Prepare the error message and error code.


#### FunctionDef __init__

Initialise the class.


#### FunctionDef metadata_url

Return ORDS URL to fetch metadata information for deployment.


#### FunctionDef get_raw_deployment

Fetch the raw files & metadata.


#### FunctionDef load_netcdf_data

Load data from NetCDF file. Retries up to 5 times if an error is encountered during load.


#### FunctionDef generate_rxf

Given a deployment, generate an RXF from its NC files.

Args:
    deployment(str): The Deployment ID to be processed.
    rxf_path (Path): Where to save/load the RXF to/from.
    mode(str) = NRT: The mode of data, which is usually NRT.
    files (Sequence[Path], optional): The source files to read from, rebuilding from scratch if not provided.
    covjson(bool): Whether to generate CovJSON jobs after ingesting segment data.


#### FunctionDef generate_ocean_gliders

Generate an NRT ocean gliders file asynchronously.

Args:
        deployment (int): A Seaglider deployment ID.

Returns: this method will request for a file to be  saved to disk, using the app config to pick a location.
The returned value of this method is only the saved files name.


#### FunctionDef request_og1

Request the generation of an OG1 file by OARS.

Args:
    rxf_file: The path to the RXF file to build from.
    og1_file: The path to save the generated OG1 file.
    metadata_url: Where OARS should fetch deployment metadata from.
    data_mode: The mode (i.e. "NRT") of the source data for this deployment.
    after: Any additional tasks that should fire after successful OG1 generation.
    unlink: Whether the file at rxf_file should be unlinked/deleted after the OG1 job runs.


#### FunctionDef check_open_dep

Check deployment is open. Copied from Slocum app.

Args:
        deployment_id: deployment number.

Returns: if the deployment is open (true) or restricted (false).


#### FunctionDef generate_filename_from_metadata

Generate the full filename for the Metadata JSON.

Args:
    root_dir(str): The root of the file system.
    raw_json(dict): The JSON which is parsed to retrieve folder/file name.
    deployment(str): The Deployment used to create the folder.

Returns:
    (Path): The full file path to the JSON file.



### File: seaglider_app/delivery/__init__.py


#### Module <module>

Imports for the delivery classes.



### File: seaglider_app/delivery/base_celery.py


#### Module <module>

Base class for celery.


#### ClassDef CelerySetUp

Super class for shared methods.


#### FunctionDef __init__

Shared init that sets up celery.

Args:
    config: an object holding RabbitMQ details.
    backend: The results backend protocol (if any) to use for sent tasks.



### File: seaglider_app/delivery/erddap_sender.py


#### Module <module>

Class for sending message to erddap celery task.


#### ClassDef TransferError

Raised when an error occurs during tranfer to ERDDAP.


#### ClassDef ErddapSender

This class deals with triggering tasks to zip and transfer source files to ERDDAP.


#### FunctionDef __init__

Prepare the error message and error code.


#### FunctionDef zip_transfer_file

Moving zip files into ERDDAP.

Args:
    deployment: the id of the deployment
    destination: where the transfer ends
    remove_source: should this method move (true), i.e. delete the source file,  or copy (false) the source file



### File: seaglider_app/delivery/met_office.py


#### Module <module>

Met office JSON.


#### ClassDef CovJSON

Class for building CoverageJSON files.


#### FunctionDef to_jars

Request a new CovJSON generation job from JARS.

Args:
    task: The Celery task content to send to JARS.



### File: seaglider_app/delivery/ocean_gliders.py


#### FunctionDef to_oars

Request a new OG1 generation job from OARS.

Args:
    task: The Celery task content to send to OARS.



### File: seaglider_app/logger.py


#### Module <module>

API logger.


#### FunctionDef create_rotating_log

Set up the Logger.


#### FunctionDef set_log_filename

Create the logfile name.

It will attempt to create the filename by looking in
- The location specified in the env file (log_file_location)



### File: seaglider_app/seaglider_app.py


#### Module <module>

Create the Seaglider application and queues.


#### FunctionDef create_app

Create and return Flask app.



### File: seaglider_app/utilities/qc.py


#### FunctionDef request_qc

Request a processing application to spawn a job for new QC generation.

Args:
    deployment: The ID of the deployment to create an qc job for.
    rxf: the path Object containing the location of the rxf file.
    qc_map: a list of dict containing the QC urls and the parameters that need to be send to them.
    filref: a list of filrefs.
    jars_payload: a dict of the data being sent to the JARS app.

Returns:
    The response from the POST request.


#### FunctionDef from_metadata

build mappings from deployment metadata and QC mappings file.

Args:
    metadata: A dict of an EGODeployment object. (i.e. egodep[EGODeployment][0]).

Returns:
    The instantiated tracker.



### File: seaglider_app/utils.py


#### Module <module>

General purpose utli function and constants.


#### FunctionDef create_rabbitmq_connection

Create a RabbitMQ connection.

Args:
    app (Flask): The Flask application to get the config strings from

Return:
    connection: New connection for RabbitMQ


#### FunctionDef get_seaglider_deployment_list

Get a list of deployments.

Return:
    list: List of deployment IDs


#### FunctionDef ords_get

Simple wrapper for GET calls to ORDS.

Args:
    endpoint: The location of the desired endpoint after "/ords/" - i.e. nrtdb/approc/active/deployments

Returns:
    The parsed JSON response body.


#### FunctionDef get_active_deployments

Get a set of all active deployment IDs.

Returns:
    A set of unique active deployment IDs.


#### FunctionDef get_seagliders

Get a set of all Seaglider deployment IDs. Optionally restrict results to active deployments only.

Args:
    only: An optional filter for specific deployments. Set to "active" to get info for active deployments only.

Returns:
    All matching deployment IDs.


#### FunctionDef files_info

Get basic info for specific files in a directory.

Information includes the last written file, the timestamp of the last write, and the total count of matching files.

Args:
    directory: The directory to search for files in.
    glob: A glob pattern to match files against.

Returns:
    A dict containing file information with keys "latest_file", "latest_time", "count"


#### FunctionDef deployment_dir

Get the data directory for a given deployment.

Args:
    deployment: The deployment number to fetch for.
    mode: The data mode (i.e. "NRT") to fetch for.

Returns:
    The expected data directory for the provided deployment and mode.



### File: tests/conftest.py


#### Module <module>

Pytest fixtures to create an app object for automated tests.


#### FunctionDef set_test_env

Fixture to mock environment variables for app configuration.


#### FunctionDef create_test_app

Fixture to create app for testing.



### File: tests/test_routes.py


#### Module <module>

Test the behaviour of application routes.


#### FunctionDef test_client

Fixture to create app client for testing.


#### FunctionDef mock_requests_get_fixture

Fixture for mocking GET request responses.


#### FunctionDef mock_requests_post_fixture

Fixture for mocking POST requests.


#### FunctionDef test_specified_file_recorded_as_missing

If the /files/<deployment> endpoint is called with a missing file, ensure the MissingFileManager is called
and a 201 response is returned.


#### FunctionDef test_empty_files_are_registered

Ensure the file is registered with the Missing Files Manager module if any file in the deployment directory has a
size of 0.


#### FunctionDef test_corrupt_files_are_skipped

Ensure a corrupt .nc file is skipped, moved to a separate directory and processing completes successfully.


#### FunctionDef test_processing_continues_if_corrupt_files_no_longer_found

Ensure a warning is logged if a corrupt .nc file disappears before being moved to SKIPPED/CORRUPTED directory.


#### FunctionDef test_processing_continues_if_corrupt_files_cant_be_moved

Ensure an exception is raised if a PermissionError is encountered when moving a corrupted file.


#### FunctionDef _mock_requests_get

Function returned by the fixture.


#### FunctionDef _mock_requests_post

Function returned by the fixture.




---

## CI/CD


### Global Variables

- **BODCCI_USER**: approc




### Jobs

- **setup**
  - Stage: .pre
  - Image: continuumio/miniconda3
  - Runs: on_success

- **test**
  - Stage: ['.stages', 'test']
  - Image: python:3.10
  - Runs: on_success

- **file-processing**
  - Stage: ['.stages', 'build']
  - Image: default
  - Runs: on_success

- **upload**
  - Stage: ['.stages', 'publish']
  - Image: default
  - Runs: on_success

- **.install-base**
  - Stage: ['.stages', 'install']
  - Image: default
  - Runs: on_success



---

## Docker

### Dockerfile: base.Dockerfile

- **Filename:** base.Dockerfile

- **Base Image:** python:3.10

- **Exposed Ports:** []

- **Volumes:** []

- **Workdir:** /seaglider_app

- **Entrypoint:** python

- **Env Vars:** ['PYTHONUNBUFFERED=1', 'PATH="/seaglider_app/.bodc-env/bin:${PATH}"']


### Dockerfile: docker-compose.yml

- **Filename:** docker-compose.yml

- **Base Image:** unknown

- **Exposed Ports:** []

- **Volumes:** []

- **Workdir:** /app

- **Entrypoint:** 

- **Env Vars:** ['NODE_ENV=development', 'RMQ_PASS=guest', 'RMQ_HOST=rabbitmq', 'RMQ_USER=guest', 'RMQ_VHOST=apds', 'RMQ_TRANSPORT=amqp', 'ROOT_DIR=/filestore/APDS', 'ORDS_ROOT=https://ordsdev.bodc.uk/', 'LOG_FILE_LOCATION=logs', 'BODCAPP_MODE=dev', 'QC_URL_ROOT=http://localhost', 'QC_RMQ_EXCHANGE=data.local', 'QC_ROUTE_KEY=qc']


### Dockerfile: local.Dockerfile

- **Filename:** local.Dockerfile

- **Base Image:** python:3.10

- **Exposed Ports:** []

- **Volumes:** []

- **Workdir:** /seaglider_app

- **Entrypoint:** 

- **Env Vars:** ['PYTHONUNBUFFERED=1']



---

## Architecture Diagram

```mermaid
<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
sandbox_py["Module: sandbox.py"]
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app___init___py["Module: __init__.py"]
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_apis___init___py["Module: __init__.py"]
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_apis_cov_json_py["Module: cov_json.py"]
seaglider_app_apis_cov_json_py_CovJsonSummary["Class: CovJsonSummary"]
seaglider_app_apis_cov_json_py --> seaglider_app_apis_cov_json_py_CovJsonSummary
seaglider_app_apis_cov_json_py_get["Function: get"]
seaglider_app_apis_cov_json_py --> seaglider_app_apis_cov_json_py_get
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_apis_file_transfers_py["Module: file_transfers.py"]
seaglider_app_apis_file_transfers_py_TransferRawZipFiles["Class: TransferRawZipFiles"]
seaglider_app_apis_file_transfers_py --> seaglider_app_apis_file_transfers_py_TransferRawZipFiles
seaglider_app_apis_file_transfers_py_post["Function: post"]
seaglider_app_apis_file_transfers_py --> seaglider_app_apis_file_transfers_py_post
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_apis_metadata_json_py["Module: metadata_json.py"]
seaglider_app_apis_metadata_json_py_ProcessMetadataJSON["Class: ProcessMetadataJSON"]
seaglider_app_apis_metadata_json_py --> seaglider_app_apis_metadata_json_py_ProcessMetadataJSON
seaglider_app_apis_metadata_json_py_post["Function: post"]
seaglider_app_apis_metadata_json_py --> seaglider_app_apis_metadata_json_py_post
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_apis_ocean_gliders_py["Module: ocean_gliders.py"]
seaglider_app_apis_ocean_gliders_py_ProcessOceanGliders["Class: ProcessOceanGliders"]
seaglider_app_apis_ocean_gliders_py --> seaglider_app_apis_ocean_gliders_py_ProcessOceanGliders
seaglider_app_apis_ocean_gliders_py_OceanGlidersSummary["Class: OceanGlidersSummary"]
seaglider_app_apis_ocean_gliders_py --> seaglider_app_apis_ocean_gliders_py_OceanGlidersSummary
seaglider_app_apis_ocean_gliders_py_post["Function: post"]
seaglider_app_apis_ocean_gliders_py --> seaglider_app_apis_ocean_gliders_py_post
seaglider_app_apis_ocean_gliders_py_get["Function: get"]
seaglider_app_apis_ocean_gliders_py --> seaglider_app_apis_ocean_gliders_py_get
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_apis_rxf_py["Module: rxf.py"]
seaglider_app_apis_rxf_py_ProcessRxf["Class: ProcessRxf"]
seaglider_app_apis_rxf_py --> seaglider_app_apis_rxf_py_ProcessRxf
seaglider_app_apis_rxf_py_RXFSummary["Class: RXFSummary"]
seaglider_app_apis_rxf_py --> seaglider_app_apis_rxf_py_RXFSummary
seaglider_app_apis_rxf_py_RxfQcSummary["Class: RxfQcSummary"]
seaglider_app_apis_rxf_py --> seaglider_app_apis_rxf_py_RxfQcSummary
seaglider_app_apis_rxf_py_post["Function: post"]
seaglider_app_apis_rxf_py --> seaglider_app_apis_rxf_py_post
seaglider_app_apis_rxf_py_get["Function: get"]
seaglider_app_apis_rxf_py --> seaglider_app_apis_rxf_py_get
seaglider_app_apis_rxf_py_get["Function: get"]
seaglider_app_apis_rxf_py --> seaglider_app_apis_rxf_py_get
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_apis_seaglider_py["Module: seaglider.py"]
seaglider_app_apis_seaglider_py_ProcessSeaglider["Class: ProcessSeaglider"]
seaglider_app_apis_seaglider_py --> seaglider_app_apis_seaglider_py_ProcessSeaglider
seaglider_app_apis_seaglider_py_RegisterSeaglider["Class: RegisterSeaglider"]
seaglider_app_apis_seaglider_py --> seaglider_app_apis_seaglider_py_RegisterSeaglider
seaglider_app_apis_seaglider_py_post["Function: post"]
seaglider_app_apis_seaglider_py --> seaglider_app_apis_seaglider_py_post
seaglider_app_apis_seaglider_py_post["Function: post"]
seaglider_app_apis_seaglider_py --> seaglider_app_apis_seaglider_py_post
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_apis_source_py["Module: source.py"]
seaglider_app_apis_source_py_FileFormat["Class: FileFormat"]
seaglider_app_apis_source_py --> seaglider_app_apis_source_py_FileFormat
seaglider_app_apis_source_py_SourceSummary["Class: SourceSummary"]
seaglider_app_apis_source_py --> seaglider_app_apis_source_py_SourceSummary
seaglider_app_apis_source_py_get["Function: get"]
seaglider_app_apis_source_py --> seaglider_app_apis_source_py_get
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_apis_symlink_generation_py["Module: symlink_generation.py"]
seaglider_app_apis_symlink_generation_py_symlinkGeneration["Class: symlinkGeneration"]
seaglider_app_apis_symlink_generation_py --> seaglider_app_apis_symlink_generation_py_symlinkGeneration
seaglider_app_apis_symlink_generation_py_post["Function: post"]
seaglider_app_apis_symlink_generation_py --> seaglider_app_apis_symlink_generation_py_post
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_core___init___py["Module: __init__.py"]
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_core_processing_py["Module: processing.py"]
seaglider_app_core_processing_py_rxf_snapshot["Function: rxf_snapshot"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py_rxf_snapshot
seaglider_app_core_processing_py_segment_snapshot["Function: segment_snapshot"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py_segment_snapshot
seaglider_app_core_processing_py_skip_corrupted_file["Function: skip_corrupted_file"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py_skip_corrupted_file
seaglider_app_core_processing_py_ProcessingError["Class: ProcessingError"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py_ProcessingError
seaglider_app_core_processing_py_Processing["Class: Processing"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py_Processing
seaglider_app_core_processing_py___init__["Function: __init__"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py___init__
seaglider_app_core_processing_py___init__["Function: __init__"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py___init__
seaglider_app_core_processing_py_metadata_url["Function: metadata_url"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py_metadata_url
seaglider_app_core_processing_py_get_raw_deployment["Function: get_raw_deployment"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py_get_raw_deployment
seaglider_app_core_processing_py_load_netcdf_data["Function: load_netcdf_data"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py_load_netcdf_data
seaglider_app_core_processing_py_generate_rxf["Function: generate_rxf"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py_generate_rxf
seaglider_app_core_processing_py_generate_ocean_gliders["Function: generate_ocean_gliders"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py_generate_ocean_gliders
seaglider_app_core_processing_py_request_og1["Function: request_og1"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py_request_og1
seaglider_app_core_processing_py_check_open_dep["Function: check_open_dep"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py_check_open_dep
seaglider_app_core_processing_py_generate_filename_from_metadata["Function: generate_filename_from_metadata"]
seaglider_app_core_processing_py --> seaglider_app_core_processing_py_generate_filename_from_metadata
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_delivery___init___py["Module: __init__.py"]
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_delivery_base_celery_py["Module: base_celery.py"]
seaglider_app_delivery_base_celery_py_CelerySetUp["Class: CelerySetUp"]
seaglider_app_delivery_base_celery_py --> seaglider_app_delivery_base_celery_py_CelerySetUp
seaglider_app_delivery_base_celery_py___init__["Function: __init__"]
seaglider_app_delivery_base_celery_py --> seaglider_app_delivery_base_celery_py___init__
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_delivery_erddap_sender_py["Module: erddap_sender.py"]
seaglider_app_delivery_erddap_sender_py_TransferError["Class: TransferError"]
seaglider_app_delivery_erddap_sender_py --> seaglider_app_delivery_erddap_sender_py_TransferError
seaglider_app_delivery_erddap_sender_py_ErddapSender["Class: ErddapSender"]
seaglider_app_delivery_erddap_sender_py --> seaglider_app_delivery_erddap_sender_py_ErddapSender
seaglider_app_delivery_erddap_sender_py___init__["Function: __init__"]
seaglider_app_delivery_erddap_sender_py --> seaglider_app_delivery_erddap_sender_py___init__
seaglider_app_delivery_erddap_sender_py_zip_transfer_file["Function: zip_transfer_file"]
seaglider_app_delivery_erddap_sender_py --> seaglider_app_delivery_erddap_sender_py_zip_transfer_file
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_delivery_met_office_py["Module: met_office.py"]
seaglider_app_delivery_met_office_py_CovJSON["Class: CovJSON"]
seaglider_app_delivery_met_office_py --> seaglider_app_delivery_met_office_py_CovJSON
seaglider_app_delivery_met_office_py_to_jars["Function: to_jars"]
seaglider_app_delivery_met_office_py --> seaglider_app_delivery_met_office_py_to_jars
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_delivery_ocean_gliders_py["Module: ocean_gliders.py"]
seaglider_app_delivery_ocean_gliders_py_to_oars["Function: to_oars"]
seaglider_app_delivery_ocean_gliders_py --> seaglider_app_delivery_ocean_gliders_py_to_oars
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_logger_py["Module: logger.py"]
seaglider_app_logger_py_create_rotating_log["Function: create_rotating_log"]
seaglider_app_logger_py --> seaglider_app_logger_py_create_rotating_log
seaglider_app_logger_py_set_log_filename["Function: set_log_filename"]
seaglider_app_logger_py --> seaglider_app_logger_py_set_log_filename
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_seaglider_app_py["Module: seaglider_app.py"]
seaglider_app_seaglider_app_py_create_app["Function: create_app"]
seaglider_app_seaglider_app_py --> seaglider_app_seaglider_app_py_create_app
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_utilities_qc_py["Module: qc.py"]
seaglider_app_utilities_qc_py_request_qc["Function: request_qc"]
seaglider_app_utilities_qc_py --> seaglider_app_utilities_qc_py_request_qc
seaglider_app_utilities_qc_py_from_metadata["Function: from_metadata"]
seaglider_app_utilities_qc_py --> seaglider_app_utilities_qc_py_from_metadata
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
seaglider_app_utils_py["Module: utils.py"]
seaglider_app_utils_py_create_rabbitmq_connection["Function: create_rabbitmq_connection"]
seaglider_app_utils_py --> seaglider_app_utils_py_create_rabbitmq_connection
seaglider_app_utils_py_get_seaglider_deployment_list["Function: get_seaglider_deployment_list"]
seaglider_app_utils_py --> seaglider_app_utils_py_get_seaglider_deployment_list
seaglider_app_utils_py_ords_get["Function: ords_get"]
seaglider_app_utils_py --> seaglider_app_utils_py_ords_get
seaglider_app_utils_py_get_active_deployments["Function: get_active_deployments"]
seaglider_app_utils_py --> seaglider_app_utils_py_get_active_deployments
seaglider_app_utils_py_get_seagliders["Function: get_seagliders"]
seaglider_app_utils_py --> seaglider_app_utils_py_get_seagliders
seaglider_app_utils_py_files_info["Function: files_info"]
seaglider_app_utils_py --> seaglider_app_utils_py_files_info
seaglider_app_utils_py_deployment_dir["Function: deployment_dir"]
seaglider_app_utils_py --> seaglider_app_utils_py_deployment_dir
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
tests_conftest_py["Module: conftest.py"]
tests_conftest_py_set_test_env["Function: set_test_env"]
tests_conftest_py --> tests_conftest_py_set_test_env
tests_conftest_py_create_test_app["Function: create_test_app"]
tests_conftest_py --> tests_conftest_py_create_test_app
</pre></div>

<div class ="mermaid-container"> <pre class="mermaid">
flowchart TB
tests_test_routes_py["Module: test_routes.py"]
tests_test_routes_py_test_client["Function: test_client"]
tests_test_routes_py --> tests_test_routes_py_test_client
tests_test_routes_py_mock_requests_get_fixture["Function: mock_requests_get_fixture"]
tests_test_routes_py --> tests_test_routes_py_mock_requests_get_fixture
tests_test_routes_py_mock_requests_post_fixture["Function: mock_requests_post_fixture"]
tests_test_routes_py --> tests_test_routes_py_mock_requests_post_fixture
tests_test_routes_py_test_specified_file_recorded_as_missing["Function: test_specified_file_recorded_as_missing"]
tests_test_routes_py --> tests_test_routes_py_test_specified_file_recorded_as_missing
tests_test_routes_py_test_empty_files_are_registered["Function: test_empty_files_are_registered"]
tests_test_routes_py --> tests_test_routes_py_test_empty_files_are_registered
tests_test_routes_py_test_corrupt_files_are_skipped["Function: test_corrupt_files_are_skipped"]
tests_test_routes_py --> tests_test_routes_py_test_corrupt_files_are_skipped
tests_test_routes_py_test_processing_continues_if_corrupt_files_no_longer_found["Function: test_processing_continues_if_corrupt_files_no_longer_found"]
tests_test_routes_py --> tests_test_routes_py_test_processing_continues_if_corrupt_files_no_longer_found
tests_test_routes_py_test_processing_continues_if_corrupt_files_cant_be_moved["Function: test_processing_continues_if_corrupt_files_cant_be_moved"]
tests_test_routes_py --> tests_test_routes_py_test_processing_continues_if_corrupt_files_cant_be_moved
tests_test_routes_py__mock_requests_get["Function: _mock_requests_get"]
tests_test_routes_py --> tests_test_routes_py__mock_requests_get
tests_test_routes_py__mock_requests_post["Function: _mock_requests_post"]
tests_test_routes_py --> tests_test_routes_py__mock_requests_post
</pre></div>

## Test Coverage

```testcoverage
{'test_coverage': [{'name': 'seaglider_app/__init__.py', 'line_rate': 100.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/apis/__init__.py', 'line_rate': 100.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/apis/cov_json.py', 'line_rate': 89.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/apis/file_transfers.py', 'line_rate': 76.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/apis/metadata_json.py', 'line_rate': 53.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/apis/ocean_gliders.py', 'line_rate': 59.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/apis/rxf.py', 'line_rate': 95.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/apis/rxf_v2.py', 'line_rate': 45.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/apis/seaglider.py', 'line_rate': 72.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/apis/source.py', 'line_rate': 75.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/apis/symlink_generation.py', 'line_rate': 38.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/core/__init__.py', 'line_rate': 100.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/core/generate_rxf_file.py', 'line_rate': 57.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/core/processing.py', 'line_rate': 74.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/delivery/__init__.py', 'line_rate': 100.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/delivery/base_celery.py', 'line_rate': 29.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/delivery/erddap_sender.py', 'line_rate': 60.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/delivery/met_office.py', 'line_rate': 0.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/delivery/ocean_gliders.py', 'line_rate': 50.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/logger.py', 'line_rate': 0.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/seaglider_app.py', 'line_rate': 96.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/utilities/netcdf.py', 'line_rate': 67.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/utilities/qc.py', 'line_rate': 97.0, 'branch_rate': 0.0}, {'name': 'seaglider_app/utils.py', 'line_rate': 48.0, 'branch_rate': 0.0}], 'summary_coverage': '67%'}