import time

from taskcapsule import Task, TaskRunner


def to_sleep(duration: int, message: str):

    time.sleep(duration)
    return f"Hello, {message}!"


my_tasks = []
my_tasks.append(
    Task(
        function=to_sleep,
        kwargs={
            "message": "callable runner!",
            "duration": 10,
        },
        output_filter="callable",
    )
)
my_tasks.append(
    Task(
        function=to_sleep,
        kwargs={
            "message": "callable runner!",
            "duration": 10,
        },
        output_filter="callable",
    )
)
runner = TaskRunner(
    tasks=my_tasks,
    workers=1,
)
runner.run()
