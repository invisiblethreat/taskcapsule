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
        kwargs={"message": "Hello, callable runner!"},
        output_filter="Hello",
    )
)

runner = TaskRunner(
    tasks=my_tasks,
    workers=4,
    show_failures=True,
)
runner.run()
