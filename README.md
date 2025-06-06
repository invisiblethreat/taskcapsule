# taskcapsule

A simple framework for running commands or Python functions concrrently using templated
commands/functions and dictionaries of arguments.

## Warning

This has sharp edges which can only be smoothed as errors are discovered. Expect better
guardrails to occur over time as issues are discovered.

### CLI/Subprocess Warning

Shells and environments behave in all sorts of ways. When in doubt, use absolute paths for the
items that you're calling

## Features

- Support for CLI subshells and Python callables
- Output filtering, which is the functional equivilent of `grep`
- Minimum worker spawning. If you have fewer tasks than defined workers, the worker pool will be reduced to the number of tasks
- `Task` validation to ensure that either `function` or `command` is set

## Future Work

- Validate function calls and arguments via `inspect`
- Tests
- Result gathering
- Pipelines

## Examples

### Subshell and Callable Example

```python
# from examples/cli_or_callable.py
from taskcapsule import Task, TaskRunner


def hello(message: str):
    return f"Hello, {message}!"


my_tasks = []
my_tasks.append(
    Task(
        command="echo {message}",
        kwargs={"message": "Hello, CLI runner!"},
        output_filter="Hello",
    )
)
my_tasks.append(
    Task(
        function=hello,
        kwargs={"message": "callable runner!"},
        output_filter="Hello",
    )
)

runner = TaskRunner(
    tasks=my_tasks,
    workers=4,
)
runner.run()
```

```shell
$ python cli_or_callable.py |jq
INFO:task-runner:spawning 2 workers
{
  "function": "hello",
  "kwargs": {
    "message": "Hello, callable runner!"
  },
  "return_code": 0,
  "output": "Hello, callable runner!!",
  "error": "",
  "duration": 9.5367431640625E-7,
  "success_filter": "Hello"
}
{
  "command": "echo Hello, CLI runner!",
  "kwargs": {
    "message": "Hello, CLI runner!"
  },
  "return_code": 0,
  "output": "Hello, CLI runner!\n",
  "error": "",
  "duration": 0.016596078872680664,
  "success_filter": "Hello"
}
INFO:task-runner:all tasks completed

```

### Nmap Example

```python
from taskcapsule import TaskRunner, Task
# Look to see if the host is running WebLogic T3
template = "nmap -oG - -p {port} --script weblogic-t3-info {addr}"
items = [{"addr":"1.2.3.4","port": "7002"}]
my_tasks = []
for i in items:
    kwargs = items
    my_tasks.append(
        Task(
            command=template,
            kwargs=kwargs,
            target_metadata={"uuid": "fedcba09-1234-1111-bcde-1234567890fe"},
            # This is in the output if, and only if, T3 is running
            output_filter="T3",
        )
    )

tr = TaskRunner(tasks=my_tasks)
tr.run()
```

### Output

`python example.py|jq`

```log
INFO:taskcapsule:spawning 1 workers
{
  "command": "nmap -oG - -p 7002 --script weblogic-t3-info 1.2.3.4",
  "kwargs": {
    "addr": "1.2.3.4",
    "port": "7002"
  },
  "return_code": 0,
  "stdout": "# Nmap 7.95 scan initiated Thu Apr 17 09:23:50 2025 as: nmap -oG - -p 7002 --script weblogic-t3-info 1.2.3.4\nHost: 1.2.3.4 ()\tStatus: Up\nHost: 45.60.186.97 ()\tPorts: 7002/open/tcp//afs3-prserver//WebLogic application server 12.2.1.4 (T3 enabled)/\n# Nmap done at Thu Apr 17 09:23:51 2025 -- 1 IP address (1 host up) scanned in 0.70 seconds\n",
  "stderr": "",
  "duration": 0.7490861415863037,
  "success_filter": "T3",
  "target_metadata": {
    "uuid": "fedcba09-1234-1111-bcde-1234567890fe"
  }
}
INFO:task-runner:all tasks completed

```

### Error Handling

Code

```python
from taskcapsule import Task, TaskRunner


def hello(message: str):
    return f"Hello, {message}!"


my_tasks = []
my_tasks.append(
    Task(
        command="nosuchcommand {message}",
        kwargs={"message": "Hello, CLI runner!"},
    )
)
my_tasks.append(
    Task(
        function=hello,
        kwargs={"wrong_arg": "callable runner!"},
    )
)
runner = TaskRunner(
    tasks=my_tasks,
    workers=4,
    show_failures=True,
)
runner.run()
```

Output

```shell
$ python show_errors.py|jq
INFO:task-runner:spawning 2 workers
ERROR:task-runner:processing command=None function=<function hello at 0x104ec4220> kwargs={'wrong_arg': 'callable runner!'} output_filter=None target_metadata=None: hello() got an unexpected keyword argument 'wrong_arg'
INFO:task-runner:success filter is None, skipping check
{
  "function": "hello",
  "kwargs": {
    "wrong_arg": "callable runner!"
  },
  "return_code": -1,
  "output": "",
  "error": "hello() got an unexpected keyword argument 'wrong_arg'",
  "duration": 0.00011897087097167969
}
INFO:task-runner:success filter is None, skipping check
{
  "command": "nosuchcommand Hello, CLI runner!",
  "kwargs": {
    "message": "Hello, CLI runner!"
  },
  "return_code": 127,
  "output": "",
  "error": "/bin/sh: nosuchcommand: command not found\n",
  "duration": 0.021525859832763672
}
```
