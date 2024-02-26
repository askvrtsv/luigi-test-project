from luigi import LocalTarget, Task

from newproducts.readers import RepoProductReader
from newproducts.settings import PROCESS_DIR, REPOS_DIR
from newproducts.utils import read_stores
from newproducts.writers import UniqueProductWriter


class UniqueProducts(Task):
    filename = PROCESS_DIR / "unique_products.csv"

    def output(self):
        return LocalTarget(self.filename)

    def run(self):
        products = []
        for store in read_stores():
            repo_path = REPOS_DIR / f"{store.repo_name}.xlsx"
            if repo_path.exists():
                for product in RepoProductReader(repo_path):
                    products.append(product)

        UniqueProductWriter(self.filename, products).write_products()
