# prettyunit.

prettyunit is a full-featured automated testing wrapper and results aggregation system. prettyunit includes three primary components:
  - Language-specific unit test wrappers
  - Unit test results API
  - Test result website for aggregation of results over time

#### Test Wrappers

prettyunit has been designed to work with a number of unit testing frameworks from a variety of different programming languages.

The purpose of the test wrappers is to send automated test results to the prettyunit API, or additionally output test results in a universal and consumable json format.

##### Supported unit test frameworks
* [unittest] - python's built-in unittest framework for python 2.x
* More coming soon


#### API

The prettyunit REST API is built using the python [flask] microframework.

The primary purpose of the API is as a means of importing test results into a persistant datastore to be displayed and queried later.


#### Website

Prettysite is built using [flask], [siimple], and [chart.js].


### Requirements

You can see a full list of requirements in the requirements.txt file. prettyunit runs on python 2.7.10 (but any [python 2.7.x] should work), there are plans to update to [python 3.5.2] in the future.

### Installation

```sh
$ mkdir prettyunit
$ cd prettyunit/
$ git clone https://github.com/beatsbears/prettyunit.git
$ chmod 666 install_prettyunit.sh
$ python manage.py runserver &
```

### Usage
Coming soon!

License
-------
[MIT]

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [unittest]: <https://docs.python.org/2/library/unittest.html>
   [flask]: <http://flask.pocoo.org/>
   [python 2.7.x]: <https://www.python.org/downloads/release/python-2712/>
   [python 3.5.2]: <https://www.python.org/downloads/release/python-352/>
   [siimple]: <http://siimple.juanes.xyz/>
   [chart.js]: <http://www.chartjs.org/>
   [MIT]: <https://github.com/beatsbears/prettyunit/blob/master/LICENSE>







