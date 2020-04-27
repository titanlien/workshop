# Overview

In this question we are trying to secure a web application with Client SSL certificates, but something isn't working
quite right and it's your job to figure out what's going on.

* We have setup a simple Hello World web app, implemented in Ruby using [Rack](http://rack.github.io/) (1.6.5).
* We run this application in a web server called [Unicorn](https://bogomips.org/unicorn/) (5.1.0).
* Unicorn sits behind [Nginx](http://nginx.org/) (1.10.2) which terminates SSL.

To demonstrate that the application works, we can use curl to make a GET request and see that we get a hello world
message back.

```
$ curl -k -i https://localhost:8080
HTTP/1.1 200 OK
Server: nginx/1.10.2
Date: Fri, 10 Mar 2017 10:23:45 GMT
Content-Type: text/html;charset=utf-8
Content-Length: 49
Connection: keep-alive
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN

hello world! it's 2017-03-10 02:24:14 -0800 here!
```

> `-k` tells curl to ignore self signed certificates.
> `-i` is to print headers for our debugging.

So far so good.

However, we want to authenticate our HTTP clients using client certificates so we have configured nginx to accept client
certificates and pass some information about the certificate to our application via HTTP headers.

We can make another request with curl, this time with a client certificate (`-E client.pem`) but we will notice that we
receive a '400 Bad Request' in response.

```
$ curl -k -i -E client.pem https://localhost:8080
HTTP/1.1 400 Bad Request
Server: nginx/1.10.2
Date: Fri, 10 Mar 2017 10:30:52 GMT
Transfer-Encoding: chunked
Connection: keep-alive

```

# The Question

1. Which of rack, unicorn and nginx is generating the 400? How can you prove it?
1. Can you narrow down the problem to a specific part of the request?
1. What is the bug that causes the '400 Bad Request' response? How did you find it? How can we fix it?

> Hint: To answer this question you will need to understand, from the source code, how nginx and unicorn process HTTP requests.

During the on-site interviews we'll discuss your answers to the above, so remember to take notes as you go and be prepared to justify your answer.
Some people find it helpful to log their terminal and review it later to remember what they did along the way.

# FAQ

## How do I get started?

* The first thing you'll need to do is install gems with `bundle install`

* Then you can start nginx & unicorn with a tool called foreman.

  Foreman looks at `Procfile` to determine what processes should be started, ours loads nginx and unicorn.

  ```
  $ bundle exec foreman start

  04:41:41 nginx.1   | started with pid 12744
  04:41:41 unicorn.1 | started with pid 12747
  04:41:41 nginx.1   | nginx: [alert] could not open error log file: open() "/var/log/nginx/error.log" failed (13: Permission denied)
  04:41:41 unicorn.1 | I, [2017-03-10T04:41:41.771141 #12747]  INFO -- : listening on addr=0.0.0.0:8081 fd=7
  04:41:41 unicorn.1 | I, [2017-03-10T04:41:41.771274 #12747]  INFO -- : worker=0 spawning...
  04:41:41 unicorn.1 | I, [2017-03-10T04:41:41.771948 #12747]  INFO -- : master process ready
  04:41:41 unicorn.1 | I, [2017-03-10T04:41:41.772231 #12763]  INFO -- : worker=0 spawned pid=12763
  04:41:41 unicorn.1 | I, [2017-03-10T04:41:41.772380 #12763]  INFO -- : Refreshing Gem list
  04:41:41 unicorn.1 | I, [2017-03-10T04:41:41.835822 #12763]  INFO -- : worker=0 ready
  ```

* At this point, nginx should be listening on port 8080 and you can use curl to make a request.

  ```
  $ curl -k https://localhost:8080
  hello world! it's 2017-03-10 04:42:48 -0800 here!
  ```

* You should also see these requests being logged to stdout in the terminal where you started foreman.

  ```
  04:42:48 unicorn.1 | 127.0.0.1 - - [10/Mar/2017:04:42:48 -0800] "GET / HTTP/1.0" 200 49 0.0011
  ```

## What are all the files?

* `app.rb`: this contains the source code for the web app.
* `config.ru`, `unicorn.conf`: these files configure Rack & Unicorn.
* `nginx/*`: this contains the configuration and ssl certificates for nginx.
* `Procfile`: this is the config for Foreman
* `client.pem`: a self-signed SSL certificate for Curl.
* `Gemfile`, `Gemfile.lock`, `.bundler`: Bundler config for managing gems.
