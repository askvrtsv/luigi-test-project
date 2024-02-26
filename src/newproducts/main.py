from luigi import WrapperTask, run

from newproducts.tasks import Stats


class Workflow(WrapperTask):
    def requires(self):
        yield Stats()


if __name__ == "__main__":
    run(local_scheduler=True, main_task_cls=Workflow)
