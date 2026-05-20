from enum import Enum


class S3ControllerDeleteFileOwnerType(str, Enum):
    ARTICLE_CATALOG = "article_catalog"
    BARCODE = "barcode"
    LIST_ITEM = "list_item"

    def __str__(self) -> str:
        return str(self.value)
