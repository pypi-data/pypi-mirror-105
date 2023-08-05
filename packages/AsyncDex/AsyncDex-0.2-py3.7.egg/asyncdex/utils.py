from typing import Any, Callable, Dict, Generic, Iterable, Mapping, Optional, TYPE_CHECKING, Tuple, TypeVar, Union

from .enum import Relationship

if TYPE_CHECKING:
    from .models.abc import Model
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


def remove_prefix(prefix: str, string: str) -> str:
    """Remove a prefix from a string. This is a polyfill for Python versions <3.9.

    :param prefix: The prefix to remove
    :type prefix: str
    :param string: The string to remove the prefix from
    :type string: str
    :return: The string without the prefix
    :rtype: str
    """
    if string[:len(prefix)] == prefix:
        return string[len(prefix):]
    else:
        return string


class AttrDict(dict, Dict[str, _VT], Generic[_VT]):
    """A :class:`dict` where keys can be accessed by attributes.

    .. versionadded:: 0.2
    """

    __slots__ = ()

    def __getattr__(self, item: str) -> _VT:
        """Get a key of the dictionary by calling the attribute representing it.

        :param item: The key to get.
        :type item: str
        :return: The value that is held inside the dictionary.
        :rtype: Any
        :raises: :class:`KeyError` if the attribute does not exist in the key.
        """
        return self[item]

    def __setattr__(self, key: str, value: _VT):
        """Sets a key of the dictionary.

        :param key: The key to set.
        :type key: str
        :param value: The value for the key.
        :type value: Any
        """
        self[key] = value

    def __repr__(self) -> str:
        """Provide a string representation of the object.

        :return: The string representation
        :rtype: str
        """
        return f"{type(self).__name__}{super().__repr__()}"


class DefaultAttrDict(AttrDict[_VT], Generic[_VT]):
    """A :class:`.AttrDict` with a default.

    .. versionadded:: 0.2
    """

    __slots__ = ("default",)

    default: Callable[[], _VT]
    """A callable that accepts no arguments and returns an instance of the value's class."""

    def __init__(self, mapping_or_iterable: Optional[Union[Mapping[str, _VT], Iterable[Tuple[str, _VT]]]] = None, *,
                 default: Callable[[], _VT]):
        if mapping_or_iterable:
            super().__init__(mapping_or_iterable)
        else:
            super().__init__()
        object.__setattr__(self, "default", default)

    def __missing__(self, key: str) -> _VT:
        """Apply the default if a key does not exist.

        :param key: The key that is missing
        :type key: str
        :return: The new default
        :rtype: Any
        """
        self[key] = value = self.default()
        return value


class _Sentinel:
    __slots__ = ()

    def __bool__(self):
        return False

    def __repr__(self):
        return "Sentinel"


_sentinel = _Sentinel()


def copy_key_to_attribute(source_dict: dict, key: str, obj: Any, attribute_name: Optional[str] = None, *,
                          default: Any = _sentinel, transformation: Optional[Callable[[str], Any]] = None):
    """Copies the value of a dictionary's key to an object.

    .. versionadded:: 0.2

    :param source_dict: The dictionary with the key and value.
    :type source_dict: dict
    :param key: The key that has the value.
    :type key: str
    :param obj: The object to set the attribute of.
    :type obj: Any
    :param attribute_name: The name of the attribute to set if the name of the key and the name of the attribute are
        different.
    :type attribute_name: str
    :param default: A default value to add if the value is not found.
    :type default: Any
    :param transformation: A callable that will be executed on the value of the key. It should accept a :class:`str` and
        can return anything.
    :type transformation: Callable[[str], Any]
    """
    attribute_name = attribute_name or key
    if key in source_dict:
        setattr(obj, attribute_name, source_dict[key])
        if transformation:
            setattr(obj, attribute_name, transformation(getattr(obj, attribute_name)))
    else:
        if default is not _sentinel:
            setattr(obj, attribute_name, default)
            if transformation:
                setattr(obj, attribute_name, transformation(getattr(obj, attribute_name)))


def parse_relationships(data: dict, obj: "Model"):
    """Parse the relationships available in a model.

    .. versionadded:: 0.2

    :param data: The raw data received from the API.
    :type data: dict
    :param obj: The object to add the models to.
    :type obj: Model
    """
    # Notes for future contributors: As of May 7, the MangaDex API has a quirk where it sends the same relationship
    # (same UUID and same type) multiple times. Until this bug is fixed, I had to check that each UUID was unique.
    from .models.manga import Manga
    from .models.author import Author
    relationship_data = {}
    seen_uuids = {}
    if "relationships" in data:
        for relationship in data["relationships"]:
            assert "id" in relationship, "Missing ID."
            relationship_id = relationship["id"]
            relationship_type = Relationship(relationship["type"])
            if relationship_type == Relationship.MANGA:
                dupe_list = seen_uuids.setdefault("mangas", [])
                if relationship_id not in dupe_list:
                    relationship_data.setdefault("mangas", []).append(Manga(obj.client, id=relationship_id))
                    dupe_list.append(relationship_id)
            elif relationship_type == Relationship.AUTHOR:
                dupe_list = seen_uuids.setdefault("authors", [])
                if relationship_id not in dupe_list:
                    relationship_data.setdefault("authors", []).append(Author(obj.client, id=relationship_id))
                    dupe_list.append(relationship_id)
            elif relationship_type == Relationship.ARTIST:
                dupe_list = seen_uuids.setdefault("artists", [])
                if relationship_id not in dupe_list:
                    relationship_data.setdefault("artists", []).append(Author(obj.client, id=relationship_id))
                    dupe_list.append(relationship_id)
    for key, value in relationship_data.items():
        setattr(obj, key, value)
