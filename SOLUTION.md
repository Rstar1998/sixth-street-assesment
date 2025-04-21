

## Deliverables

### Software

A solution implemented in Python with instructions on how to run locally and how to call the endpoints via `curl`.

## How to run locally
-  Make sure you have `python 3.13.2` , `make` and `poetry` installed on your local machine
- `cd boilerplate` and  execute  `make run` to build and start running
- run  `make test` for running test cases
- rest api server will start and serve request on port 8000 of your localhost
- hit the below curl apis to get the necessary results (or use swagger UI http://127.0.0.1:8000/docs or postman)


## Curl commands

`lookup` : 
```
curl --location 'http://127.0.0.1:8000/lookup?symbol=NVDA&date=2023-03-07'
```
`min` : 
```
curl --location 'http://127.0.0.1:8000/min?symbol=NVDA&range=10'
```

`max` : 
```
curl --location 'http://127.0.0.1:8000/max?symbol=NVDA&range=10'
```



### Discussion

A short write-up where you discuss the following:

  - What compromises did you make due to time constraints?
  ```
    1) Did not use docker 
    2) Should have created more comprehensive test cases
    3) all implementation is packed in app.py. 
  ```

  - What would you do differently if this software was meant for production use?
  ```
    1) Dockerize this microservice 
    2) More test cases (coverage)
    3) Use Redis (in memory db) for caching purpose
    4) Make app.py more modular , right now its packed with all functions. Maybe create utils.py and migrate some functions
    5) Use proper authentication/authorization for API's. right now anyone can hit our APIs without any rate limit
    6) Add .gitignore so that files like .env dont get push to repo
    7) Create CI/CD pipelines 

  ```

  - Propose how you might implement authentication, such that only authorized users may hit these endpoints.

  ```  
      Here there are various methods available. One such method is using API keys. API keys will be provided to user and when user hits any of our API , they should pass `API key` in request header. Our service should implement a Middleware which does validation if the key is valid and accordingly give access.
  ```

  - How much time did you spend on this exercise?
  ```
    Around 2-3 hours 
  ```
  - Please include any other comments about your implementation.
  ```
    I ran this code using python3.13 , Poetry (version 2.1.1) , GNU Make 3.81 on MacOS
  ```
  - Please include any general feedback you have about the exercise.
  ```
    Overall I enjoyed the experience. I like such activities 
  ```
  - You will need a GitHub account for the next round. What is your GitHub username?
```
    https://github.com/Rstar1998
```