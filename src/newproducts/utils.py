from newproducts.models import StoreConfig


def read_stores():
    return [
        StoreConfig(
            "Впрок",
            "Vprok",
            "Vprok_",
            11,
            4,
            2,
            ["Зоотовары>*"],
            None,
            None,
            ["для кошек"],
        ),
    ]
