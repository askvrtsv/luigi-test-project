import abc
import csv
import pathlib
import typing as t

from newproducts.models import ProcessedProduct, Product

Row = list[str]


class DataOutput(abc.ABC):
    @abc.abstractmethod
    def write_rows(self, rows: list[Row]) -> None:
        raise NotImplementedError


class CsvOutput(DataOutput):
    filename: pathlib.Path

    def write_rows(self, rows: list[Row]) -> None:
        with self.filename.open("w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)


class ProductWriter(abc.ABC):
    @abc.abstractmethod
    def write_products(self) -> None:
        raise NotImplementedError


class UniqueProductWriter(ProductWriter, CsvOutput):
    def __init__(self, filename: pathlib.Path, products: t.Collection[Product]) -> None:
        self.filename = filename
        self.products = products

    def write_products(self) -> None:
        rows = []
        rows.append(["store", "sku"])
        for product in self.products:
            rows.append([product.store_name, product.sku])
        self.write_rows(rows)


class ProcessedProductWriter(ProductWriter, CsvOutput):
    def __init__(
        self, filename: pathlib.Path, products: t.Collection[ProcessedProduct]
    ) -> None:
        self.filename = filename
        self.products = products

    def write_products(self) -> None:
        rows = []
        rows.append([
            "store",
            "sku",
            "title",
            "image",
            "category",
            "brand",
            "label",
            "status",
        ])
        for product in self.products:
            rows.append([
                product.store_name,
                product.sku,
                product.title,
                product.image or "",
                product.category or "",
                product.brand or "",
                product.label,
                product.status.value,
            ])
        self.write_rows(rows)
