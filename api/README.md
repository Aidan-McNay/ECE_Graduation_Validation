# `api`

This is a folder for all of our functions that interact with the classes.cornell.edu API

## Files

This folder includes:
 - `bulk_api.py`: A mechanism for caching data from many requests at once, using `grequests` to circumvent Python's Global Interpreter Lock
 - `class_api.py`: The main wrapper around our API data, used for obtaining infor about the rosters present, as well as data on specific class offerings

## API

The functions in this directory heavily interact with the [classes.cornell.edu API](https://classes.cornell.edu/content/SP24/api-details). Specifically,
they use the `requests`/`grequests` module to obtain data from the API, translating it into JSON entries before handing it back to the rest of the code.
It is recommended that other functions interact with this data through the `obj.class_obj.Class` object, which in turn is a further wrapper around class
data that better organizes it, making it more easily accessible for other functions.

## Caching

It is often the case that data requested once will be desired again (as well as other similar data). However, we'd like to avoid having to ping the main
API multiple times in this case, as doing so is time-consuming (about 1 second per request, which adds up on the scale of checklists).

Our API wrappers help minimize the number of API calls in two ways. First, any data that is received is stored ("cached") for later. If a later request
is made, we first check our stored data, and if we have the desired data, simply return it. Second, we never send a request for a single class; instead,
we send requests for data on the entire department for the desired term, and cache all of it, such that later requests for other classes in the same
department and semester will be found cached instead of needing to ping the API (this is often likely for many students, who take multiple classes in a
given department in a given semester, such as their major department.)

Finally, in light of our checklist code, this can be further optimized. All of the classes that are needed are known at the beginning of runtime when the
rosters are created, before any individual check needs a class. Therefore, we can send all of our API requests in parallel at the start of execution. This
allows us to overlap the latency of the requests (amortizing the delay). When a function later needs data on a class, it will have already been stored. This
parallelism is usually hard to implement due to Python's [GIL](https://realpython.com/python-gil/) and its effective imposition of single-threading; however,
our code uses the `grequests` module (which in turn uses the `gevent` module) to bypass the GIL and allow for parallel HTTP requests to get our data.