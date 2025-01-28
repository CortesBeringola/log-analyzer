## Log Analyzer
Command-line tool __*(Log Analyzer)*__ to analyze the content of log files.  
__*Log Analyzer*__ accepts 2 mandatory arguments and 4 optional arguments.


## Inputs

#### Mandatory Arguments 

- i_path (Input file path): The log file path to analyze. For ease of use the input paths have been limited 
and narrowed to a project working directory. There are 2 possible input options. 
  - __File__ `(/files/format/file.format)`: Analyze one file. Inside the app working directory, there is a __files__ directory. Inside there are 4 directories where each directory corresponds to the allowed input formats *(csv, json, log, txt)*. Check the addendum below for some sample data examples.
  - __Directory__ `(/files/format)`: Analyze all files within a __directory__ with the matching directory format.
 
- o_path (Output file path): The results file path. The format needs to be as follows: `file_name.format`. This file will be stored in the following path */files_results/file_name.format*.

__*Note__: Inputting directories not matching these requirements will raise an app error.

#### Optional Arguments 

- i_mfip: Most frequent IP
- i_lfip: Least frequent IP
- i_eps: Events per second
- i_bytes: Total amount of bytes exchanged

__*Note 1__: All the optional arguments default values are __None__. As an example, adding __i_mfip__ optional argument in __*Log Analyzer*__ will be done as follows:  
`python cli.py input_path out_path --i-mfip`  
__*Note 2__: For ease of use, not passing any optional argument in __*Log Analyzer*__ will be equivalent to call all optional fields.

## Outputs

Log files stats will be stored in a file in the */files_results/* directory with the specified format. Possible output formats are *(csv, json, txt)*.


## Formats

#### Input formats

The following table will show the data fields and the format in which the data will be gathered:

| timestamp      | header_size | client_ip     | response_code | response_size | request_method | url                 | username      | destination_ip         | response_type |
|----------------|-------------|---------------|---------------|---------------|----------------|---------------------|---------------|------------------------|---------------|
| 1157689312.049 | 5006        | 10.105.21.199 | TCP_MISS/200  | 19763         | CONNECT        | login.yahoo.com:443 | badeyek       | DIRECT/209.73.177.115  | -             |


- #### *log*
 ```bash
 1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -
 ```
- #### *csv*
```bash
1157689312.049,5006,10.105.21.199,TCP_MISS/200,19763,CONNECT,login.yahoo.com:443,badeyek,DIRECT/209.73.177.115,-
````
- #### *json*
```bash
{"1": {
    "timestamp": "1157689312.049",
    "header_size": "5006",
    "client_ip": "10.105.21.199",
    "response_code": "TCP_MISS/200",
    "response_size": "19763",
    "request_method": "CONNECT",
    "url": "login.yahoo.com:443",
    "username": "badeyek",
    "destination_ip": "DIRECT/209.73.177.115",
    "response_type": "-"}
}
```
- #### *txt*
 ```bash
 1157689312.049   5006 10.105.21.199 TCP_MISS/200 19763 CONNECT login.yahoo.com:443 badeyek DIRECT/209.73.177.115 -
 ```

#### Output formats
Output formats will look as follows. Fields to bear in mind:

| File Name   | Most Frequent IP | Least Frequent IP | Events per Second | Total Bytes |
|-------------|------------------|-------------------|-------------------|-------------|
| text.format | 10.105.21.199    | 10.105.21.199     | 1.25              | 47655.0     |

- #### *csv*
```bash
,Most Frequent IP,Least Frequent IP,Events per Second,Total Bytes
long_file.csv,"{'client_ip': '10.105.21.199', 'count': 5}","{'client_ip': '10.105.37.58', 'count': 5}",0.05,47655.0
````
- #### *json*
```bash
{"short_file.csv": {
      "Most Frequent IP": {"client_ip": "10.105.21.199", "count": 5},
      "Least Frequent IP": {"client_ip": "10.105.37.58", "count": 1}, 
      "Events per Second": 0.05, 
      "Total Bytes": 47655.0
      }
}
```
- #### *txt*
```bash
short_file.csv >>> {'Most Frequent IP': {'client_ip': '10.105.21.199', 'count': 5}, 'Least Frequent IP': {'client_ip': '10.105.37.58', 'count': 1}, 'Events per Second': 0.05, 'Total Bytes': 47655.0}
```
   

## Error Handling - Testing

Error handling has been tested using the typer CliRunner library. Examples of tests carried out are:  
- Incorrect number of arguments
- Input/Output path does not exist
- Incorrect input/output format
- No input/output format
- File exported successfully

In order to run the tests from terminal make sure to be in the program working directory and run the following commands:
- Run all tests:
  ```bash
  python -m pytest -rPs tests/
  ```
- Run a particular test:
  ```bash
  python -m pytest -rPs tests/test_cli.py -k test_name
  ```


## Docker Instructions

See below steps on how to build and run a *Log Analyzer* Docker image as a docker container/service.

- #### Docker Container
This would be the simple solution with low scalability. There are two possible ways to run the image container:
  - Run an executable container: More comfortable since it can be executed directly when running the container. 
    1. Go to app root working directory.
    2. Build docker image:
       ```bash
        docker build -f ./docker/executable/Dockerfile . -t cli_executable
       ```
    3. Run container:
       ```bash
        docker run --name cli_container -t cli_executable /files/csv/ results.csv 
       ```
  - Run container and access container terminal: Less comfortable for executing but better for accessing files. 
    1. Go to app root working directory.
    2. Build docker image:
       ```bash
        docker build -f ./docker/terminal/Dockerfile . -t cli_terminal
       ```
    3. Access container terminal:
        ```bash
        docker run -it cli_terminal  /bin/bash
       ```
    4. Run script
       ```bash
        python cli.py /files/csv/ result.csv 
       ```
    5. Check files by accessing proper directories
    6. Exit terminal by typing `exit`  
    
- #### Docker Service
This would be the scalable solution, desired in case this application got popular and started getting a lot of usage.
  1. Go to app root working directory.
  2. Build docker image:
      ```bash
      docker build -t cli_service -f docker/executable/Dockerfile .
      ```  
  3. Run Service:
      ```bash
      docker-compose up --build cli_service  
     ```
     
__Useful commands__:
- Check existing images: `docker images`
- Remove Docker image: `docker rmi cli`
- Check existing containers: `docker ps`
- Remove Docker image container: `docker rm container_id`
