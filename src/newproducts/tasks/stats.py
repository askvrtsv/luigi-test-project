import collections
import csv
import pathlib
import typing as t

from luigi import LocalTarget, Task

from newproducts.models import ProductStatus
from newproducts.readers import ProcessedProductReader
from newproducts.settings import RESULT_DIR
from newproducts.tasks import ProcessScrapedProducts
from newproducts.utils import read_stores


def metric_key(
    store_name: str,
    metric_name: t.Literal["added", "skipped_by_category", "skipped_by_title"],
) -> str:
    if metric_name not in ("added", "skipped_by_category", "skipped_by_title"):
        raise ValueError("Unknown metric name: %s", metric_name)
    return f"{store_name}:{metric_name}"


class Stats(Task):
    filename = RESULT_DIR / "stats.csv"

    def output(self):
        return LocalTarget(self.filename)

    def run(self) -> None:
        counter = self._calculate_stats()

        with self.filename.open("w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                None,
                "Добавлено",
                "Пропущено (кат.)",
                "Пропущено (назв.)",
            ])
            for store in read_stores():
                writer.writerow([
                    store.name,
                    counter.get(metric_key(store.name, "added"), 0),
                    counter.get(metric_key(store.name, "skipped_by_category"), 0),
                    counter.get(metric_key(store.name, "skipped_by_title"), 0),
                ])

    def requires(self):
        yield ProcessScrapedProducts()

    def _calculate_stats(self) -> dict[str, int]:
        counter: dict[str, int] = collections.defaultdict(int)
        products = ProcessedProductReader(
            pathlib.Path(self.input()[0].path),
            lambda x: x.status != ProductStatus.DUPLICATE,
        )
        for product in products:
            if product.status is ProductStatus.NEW:
                counter[metric_key(product.store_name, "added")] += 1
            if product.status is ProductStatus.OUT_OF_CATEGORY:
                counter[metric_key(product.store_name, "skipped_by_category")] += 1
            if product.status is ProductStatus.STOP_WORD_IN_TITLE:
                counter[metric_key(product.store_name, "skipped_by_title")] += 1
        return counter
