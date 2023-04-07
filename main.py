import logging

from destination.example.example import ExampleDestination
from source.example.example import ExampleSource
from workflow.workflow import Workflow, Workflows

if __name__ == "__main__":
    # setup logging to console stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    workflows = Workflows(
        ws=[
            Workflow(source=ExampleSource(), destination=ExampleDestination()),
        ]
    )
    workflows.run()