import logging
import pathlib
import time
from functools import partial

import typer

import flowmaster.cli.config
import flowmaster.cli.db
import flowmaster.cli.item
from flowmaster.setttings import (
    APP_HOME,
    FLOW_CONFIGS_DIR,
    POOL_CONFIG_FILEPATH,
    FILE_STORAGE_DIR,
    LOGS_DIR,
    PLUGINS_DIR,
)

app = typer.Typer()
app.add_typer(flowmaster.cli.config.app, name="config")
app.add_typer(flowmaster.cli.db.app, name="db")
app.add_typer(flowmaster.cli.item.app, name="item")


@app.command()
def init():
    from flowmaster.models import database, FlowItem

    typer.echo(f"APP_HOME={APP_HOME}")

    pathlib.Path.mkdir(APP_HOME, exist_ok=True)
    pathlib.Path.mkdir(FILE_STORAGE_DIR, exist_ok=True)
    pathlib.Path.mkdir(LOGS_DIR, exist_ok=True)
    pathlib.Path.mkdir(FLOW_CONFIGS_DIR, exist_ok=True)
    pathlib.Path.mkdir(PLUGINS_DIR, exist_ok=True)

    if not pathlib.Path.exists(POOL_CONFIG_FILEPATH):
        with open(POOL_CONFIG_FILEPATH, "w") as f:
            f.write("flows: 100\n")

    database.create_tables([FlowItem])


def prepare_for_run(dry_run: bool = False):
    init()

    typer.echo("\n===================" "\nFlowMaster" "\n===================\n")

    from flowmaster.models import FlowItem

    # Clearing statuses for unfulfilled flows.
    FlowItem.clear_statuses_of_lost_items()

    if dry_run:
        FlowItem.delete().where(FlowItem.name == "fakedata.etl.flow.yml").execute()


@app.command()
def run(interval: int = 20, dry_run: bool = False):
    prepare_for_run(dry_run=dry_run)

    from flowmaster.utils.logging_helper import CreateLogger
    from flowmaster.operators.base.work import order_flow

    logger = CreateLogger("local_executor", "local_executor.log", level=logging.INFO)
    begin = time.time()
    duration = interval

    while True:
        logger.info("Ordering flow")
        list(order_flow(logger=logger, async_mode=False, dry_run=dry_run))

        if duration >= interval:
            duration = 0
            begin = time.time()
        else:
            time.sleep(interval - duration)
            duration += time.time() - begin


@app.command()
def run_thread(workers: int = 2, interval: int = 20, dry_run: bool = False):
    prepare_for_run(dry_run=dry_run)

    from flowmaster.operators.base.work import order_flow
    from flowmaster.utils.thread_executor import ThreadExecutor

    order_task_func = partial(order_flow, dry_run=dry_run, async_mode=True)
    executor = ThreadExecutor(order_task_func=order_task_func)
    executor.start(order_interval=interval, workers=workers)


if __name__ == "__main__":
    app()
