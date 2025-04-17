"""
Example of using TaskRunner to run nmap commands with Task objects.
"""

from taskcapsule import Task, TaskRunner

if __name__ == "__main__":
    items = ["1.2.3.4,7002"]
    my_tasks = []
    for i in items:
        parts = i.split(",")
        # this would be easier if loading with CSV or JSON
        kwargs = {"addr": parts[0], "port": parts[1]}
        my_tasks.append(
            Task(
                command="nmap -oG - -p {port} --script weblogic-t3-info {addr}",
                kwargs=kwargs,
                target_metadata={"entity_id": ""},
                output_filter="T3",
            )
        )

    tr = TaskRunner(tasks=my_tasks)
    tr.run()
