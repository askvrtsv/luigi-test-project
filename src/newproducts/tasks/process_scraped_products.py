import pathlib
from dataclasses import asdict

from luigi import LocalTarget, Task

from newproducts.models import ProcessedProduct, Product, ProductStatus, StoreConfig
from newproducts.readers import ScrapedProductReader, UniqueProductReader
from newproducts.settings import PROCESS_DIR, SCRAPED_DIR
from newproducts.tasks.unique_products import UniqueProducts
from newproducts.utils import read_stores
from newproducts.writers import ProcessedProductWriter


def is_out_of_category(
    category: str | None, patterns: list[str], skip_empty_category: bool = False
) -> bool:
    if not category:
        return skip_empty_category
    for pattern in patterns:
        if pattern.startswith("*") and pattern.endswith("*"):
            if pattern.strip("*") in category:
                return False
        elif pattern.startswith("*"):
            if category.endswith(pattern.lstrip("*")):
                return False
        elif pattern.endswith("*"):
            if category.startswith(pattern.rstrip("*")):
                return False
        else:
            if category == pattern:
                return False
    return True


def has_stop_words(title: str, stop_words: list[str]) -> bool:
    for stop_word in stop_words:
        if stop_word in title:
            return True
    return False


class ProcessScrapedProducts(Task):
    filename = PROCESS_DIR / "processed_products.csv"
    _completed = False
    seen_products: set[Product]

    def output(self):
        return LocalTarget(self.filename)

    def run(self) -> None:
        self.seen_products = set(
            x for x in UniqueProductReader(pathlib.Path(self.input()[0].path))
        )
        processed_products = [product for product in self._get_processed_products()]
        ProcessedProductWriter(self.filename, processed_products).write_products()

    def _get_processed_products(self):
        for store in read_stores():
            yield from self._process_products(store)

    def _process_products(self, store: StoreConfig):
        for products_path in SCRAPED_DIR.rglob(f"{store.scraped_prefix}*.csv"):
            for product in ScrapedProductReader(products_path, store):
                product_id = Product(store_name=product.store_name, sku=product.sku)
                if is_out_of_category(product.category, store.categories):
                    status = ProductStatus.OUT_OF_CATEGORY
                elif has_stop_words(product.title, store.stop_words):
                    status = ProductStatus.STOP_WORD_IN_TITLE
                elif product_id in self.seen_products:
                    status = ProductStatus.DUPLICATE
                else:
                    status = ProductStatus.NEW
                    self.seen_products.add(product_id)
                yield ProcessedProduct(**asdict(product), status=status)

    def requires(self):
        yield UniqueProducts()
