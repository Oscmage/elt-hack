import logging

from workflow.workflow import Workflows, Workflow

if __name__ == "__main__":
    # setup logging to console stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    workflows = Workflows(
        ws=[
            Workflow(),
        ]
    )
    workflows.run()
