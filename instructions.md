Assignment 2: Serve model as a web service
You have already deployed the headline sentiment analysis model as a batch job. Your task now is to deploy it as a web service so clients can make real-time requests.

What is your task?
You need to create a python file, called score_headlines_api.py (this will help me review your code, otherwise the filename has no connection to the functions exposed to clients). You will need to expose two API functions:

/status, which will simply return a JSON object {'status':'OK'} (this will help us confirm that the service is up). This will be of HTTP type GET

/score_headlines , of HTTP type POST, which will accept a list of headlines and return their labels: {'labels': ['Optimistic', 'Optimistic', 'Neutral', 'Pessimistic', ...]}

Notice that we are not returning the text of the headline, only the label. This will allow us to save on bandwith, if a client is scoring a huge number of headlines. It is on the client to stitch the headliens back together with their labels.
Is it a good idea for us to try to save bandwith?
Warning: Will you load the transformer model for each request? What if you load the model once and encode utterances within the score_headlines function?

Deployment considerations
Please use Python's logging library to write logs. If you are doing any error checking or catching exceptions, those MUST be logged using .warning(), .error(), .critical() (whichever is most appropriate). If you are logging general information, such as the fact that a client made a request, log that as .info(), but don't feel the need to log the full body of the text. This is a log, not a store of transactions. If you do want to track much more detailed information, which should not be used in production, feel free to use .debug()
Please use additional tools, such as curl and Postman to test your code. Consult the presentation deck at lectures/075_web_under_the_hood if you need examples.
Please create a new branch and commit your api code to it. Only when the work is complete should you "merge" the code back into your main branch.
You should already have GitHub actions running to check your code with tools such as pylint
You should continue to use Git for your work AND to "deploy" (Use the git pull command on the server to pull the latest code that you have been pushing to git)
Other notes
Please do not keep your server running when you are not testing it. For whatever reason, our server is the target of hackers and this server might give them more "vectors of attack".

Note that there is a worked example of FastAPI serving and consuming POST requests at lectures/075_web_under_the_hood/[consume_services.ipynb and serve_post_json.py]

Please use the following ports for your service:

Student	Port
stephenc	8081
sebgarcia	8082
sharonlee	8083
kenlew	8084
gmartinezh	8085
bimalsen	8086
linsabones	8087
alextsourmas	8088
charlottez	8089
haoyu25	8090
You do not need to submit anything to canvas. I will check your code by running it on the linux server.

Linux command lines notes
top, htop to see what processes (programs) are running
ps -ef or ps auxwww and "|grep yourname" for a useful way to find what programs are running
Find programs which hold a port: lsof -i:8080 or netstat -tulnp | grep :8000 or ss -tulnp | grep :8000
Kill a process: kill -9 process_id (you can get the process id by using the ps -ef command)
Ctrl + c to exit a program