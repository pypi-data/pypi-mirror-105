from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pagination import Pagination
from ..models.query import Query
from ..models.sort import Sort
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssetRequest")


@attr.s(auto_attribs=True)
class AssetRequest:
    """ """

    pagination: Union[Pagination, Unset] = UNSET
    sort: Union[Unset, List[Sort]] = UNSET
    query: Union[Query, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pagination: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pagination, Unset):
            pagination = self.pagination.to_dict()

        sort: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.sort, Unset):
            sort = []
            for sort_item_data in self.sort:
                sort_item = sort_item_data.to_dict()

                sort.append(sort_item)

        query: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.query, Unset):
            query = self.query.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pagination is not UNSET:
            field_dict["pagination"] = pagination
        if sort is not UNSET:
            field_dict["sort"] = sort
        if query is not UNSET:
            field_dict["query"] = query

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pagination: Union[Pagination, Unset] = UNSET
        _pagination = d.pop("pagination", UNSET)
        if not isinstance(_pagination, Unset):
            pagination = Pagination.from_dict(_pagination)

        sort = []
        _sort = d.pop("sort", UNSET)
        for sort_item_data in _sort or []:
            sort_item = Sort.from_dict(sort_item_data)

            sort.append(sort_item)

        query: Union[Query, Unset] = UNSET
        _query = d.pop("query", UNSET)
        if not isinstance(_query, Unset):
            query = Query.from_dict(_query)

        asset_request = cls(
            pagination=pagination,
            sort=sort,
            query=query,
        )

        asset_request.additional_properties = d
        return asset_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
