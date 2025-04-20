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
