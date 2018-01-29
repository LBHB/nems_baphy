# NEMS BAPHY API

The NEMS<->BAPHY API wraps separates the operation of BAPHY from that of NEMS so that neither system has to know about the internal workings of the other. 

As a modeler, we don't care how the data was captured, we just want the data in a format that is friendly to NEMS. As maintainers of BAPHY, we don't want them accidentally writing garbage to our database!


## Setup

SSH into the server that will be running this API.

Install the following required packages:
```
pip3 install flask --user
pip3 install flask_restful --user
```

Define the following environment variables (edit as needed):

```
export NEMS_BAPHY_API_HOST='localhost'
export NEMS_BAPHY_API_PORT='3003'
export MYSQL_HOST=
export MYSQL_USER=
export MYSQL_PASS=
export MYSQL_DB=
export MYSQL_PORT='3306'
```

Then run the server with `python3 -m nems_baphy_api`.

Note that `NEMS_BAPHY_API_HOST` is localhost for testing, but be sure to make it an externally-facing address if you want anybody else to be able to use it.


## Testing the API

In a new terminal on that same machine, you should be able to test that the API is working using:

```
curl http://localhost:3003/by-batch/273/gus018c-a3
```
  
where '273' is the batch and 'por39' is the cellid. 


## Future work

If desired and time allows, it would not be tht hard to add some "search" functionality to this that would help us find recordings based on:

1) stimulus type & cellid

2) cellid

3) area of brain

