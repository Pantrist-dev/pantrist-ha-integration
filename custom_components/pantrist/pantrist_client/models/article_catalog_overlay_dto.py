from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.article_catalog_overlay_row_dto import ArticleCatalogOverlayRowDto


T = TypeVar("T", bound="ArticleCatalogOverlayDto")


@_attrs_define
class ArticleCatalogOverlayDto:
    """
    Attributes:
        seed_lang (None | str): Language of the default catalog the rows overlay (e.g. `de-DE`); `none` for a list
            without a default catalog and null for a legacy list, whose rows are the whole catalog in both cases. A client
            treats a value it does not know like null.
        rows (list[ArticleCatalogOverlayRowDto]):
    """

    seed_lang: None | str
    rows: list[ArticleCatalogOverlayRowDto]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        seed_lang: None | str
        seed_lang = self.seed_lang

        rows = []
        for rows_item_data in self.rows:
            rows_item = rows_item_data.to_dict()
            rows.append(rows_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "seedLang": seed_lang,
                "rows": rows,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_catalog_overlay_row_dto import ArticleCatalogOverlayRowDto  # noqa: PLC0415

        d = dict(src_dict)

        def _parse_seed_lang(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        seed_lang = _parse_seed_lang(d.pop("seedLang"))

        rows = []
        _rows = d.pop("rows")
        for rows_item_data in _rows:
            rows_item = ArticleCatalogOverlayRowDto.from_dict(rows_item_data)

            rows.append(rows_item)

        article_catalog_overlay_dto = cls(
            seed_lang=seed_lang,
            rows=rows,
        )

        article_catalog_overlay_dto.additional_properties = d
        return article_catalog_overlay_dto

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
