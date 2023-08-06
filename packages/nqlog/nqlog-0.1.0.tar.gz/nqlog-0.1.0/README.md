# nqlog
## Luca de Alfaro, 2020

Not quite the logger Google wrote, not quite the logger Luca wanted, but at least: 

* It logs to the Google cloud. 
* It groups logs for the same "request" into the same log entry. 
* The severity of the grouped lines is equal to the maximum severity of any line in the group. 
* It avoids running string formatting for strings that are logged below the minimum level. 

This seems trivial and normal, but unfortunately, it is no longer the standard behavior.  In GC, log lines are no longer automatically grouped together for each request, and even if you figure out how to have them grouped, the group [no longer inherits the maximum severity of any line in the group](https://cloud.google.com/appengine/docs/standard/python3/writing-application-logs). 

The chief limitation of this logger is that it works only for 
single-threaded services.  Extension to multi-threaded services is
a work in progress. 

## Use

### Keys to GC

In your "main" file, you need: 

```python
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "keys/google_cloud_keys.json"
```

where of course you replace the path with the actual one.  The keys are json keys to a service account that has logging rights on Google cloud. 

### Logger use

All you need is: 

```python
from nqlog import logthis, logging
```
    
Then, you need to decorate the functions whose execution corresponds to a "request".  This can be the execution of a web request (e.g., a bottle entry point), or the execution of a task from a scheduler. 

```python
@logthis()
def function_to_be_logged():
    ...
```
        
Once this is done, whenever inside the function to be logged, or one of the things it calls, you do: 

```python
logging.info("This is a log line")
```
    
the log line is logged together with all other lines of the request. The grouping is thread-safe, so if you call `function_to_be_logged` from multiple threads (e.g., to service requests in parallel), everything works as it should.

The logthis decorator takes optional parameters:

    Decorator to cause a function to be logged.
    :param log_name: Name of the log to be used for logging.
    :param resource: resource to be used for logging.  You can create a
        resource e.g. via:
        from google.cloud.logging.resource import Resource
        resource = Resource( type='gae_app',
                    labels={
                        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT")
                        "module_id": os.getenv("GAE_MODULE")
                        "service_id": os.getenv("GAE_SERVICE")
                        "version_id": os.getenv("GAE_VERSION")
                       })
    :param max_duration: Max duration of a log entry in seconds.
        If the request takes longer than this, the log entry is broken into
        multiple log entries, each of at most max_duration length.
    :param level: Minimum level at which logging occurs.

### Efficiency

Often, building a log line is computationally intensive, due to the process of converting data types and structures to a string.  nqlog contains an optimization.  If instead of doing: 

    logging.debug("The value of my monster data structure is: %r" % monster)
    
you do: 

    logging.debug("The value of my monster data structure is: %r", monster)

with a `,` instead of a `%`, then nqlog avoids converting `monster` to its representation unless the log level is `DEBUG` or lower. 