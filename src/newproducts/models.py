import dataclasses
import enum


class ProductStatus(enum.Enum):
    NEW = "NEW"
    DUPLICATE = "DUPLICATE"
    STOP_WORD_IN_TITLE = "STOP_WORD_IN_TITLE"
    OUT_OF_CATEGORY = "OUT_OF_CATEGORY"


@dataclasses.dataclass(frozen=True)
class StoreConfig:
    name: str
    repo_name: str
    scraped_prefix: str
    sku_col: int
    category_col: int | None
    title_col: int
    categories: list[str]
    image_col: int | None
    brand_col: int | None
    stop_words: list[str]


@dataclasses.dataclass(frozen=True)
class Product:
    store_name: str
    sku: str


@dataclasses.dataclass(frozen=True)
class RepoProduct(Product):
    title: str
    image: str | None
    category: str | None
    brand: str | None
    label: str


@dataclasses.dataclass(frozen=True)
class ScrapedProduct(RepoProduct):
    pass


@dataclasses.dataclass(frozen=True)
class ProcessedProduct(ScrapedProduct):
    status: ProductStatus
