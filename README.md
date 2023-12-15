# MySQL DB testing

With these simple scripts, I want to demonstrate how to create a database
containing a table with columns of specific data types, manipulate with the 
data and execute some basic positive and negative test cases.
---
## 1. Setup

* Install the required packages
  > pip install -r requirements.txt
* MySQL Server must be installed
* You can change the creds in order to get access to your DB instance

```
config.ini

host_name = localhost
user_name = root
password = qwerty123
...
```
---
## 2. Executing tests

* To run a specific test in a module:
  > pytest -k "test_name"

  > pytest tests/test_module.py::test_name

* To run all tests
  > pytest