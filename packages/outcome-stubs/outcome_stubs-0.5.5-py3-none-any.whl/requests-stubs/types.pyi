from typing import (
    IO,
    AbstractSet,
    Any,
    Callable,
    Iterable,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Protocol,
    Text,
    Tuple,
    TypeVar,
    Union,
)

from requests import auth, cookies, models

_KT_co = TypeVar("_KT_co", covariant=True)
_VT_co = TypeVar("_VT_co", covariant=True)

RequestsCookieJar = cookies.RequestsCookieJar
Request = models.Request
Response = models.Response
PreparedRequest = models.PreparedRequest

Hook = Callable[[Response], Any]
_Hooks = MutableMapping[Text, List[Hook]]
_HooksInput = MutableMapping[Text, Union[Iterable[Hook], Hook]]

class SupportsItems(Protocol[_KT_co, _VT_co]):
    def items(self) -> AbstractSet[Tuple[_KT_co, _VT_co]]: ...

_ParamsMappingKeyType = Union[Text, bytes, int, float]
_ParamsMappingValueType = Union[Text, bytes, int, float, Iterable[Union[Text, bytes, int, float]], None]
_Params = Union[
    SupportsItems[_ParamsMappingKeyType, _ParamsMappingValueType],
    Tuple[_ParamsMappingKeyType, _ParamsMappingValueType],
    Iterable[Tuple[_ParamsMappingKeyType, _ParamsMappingValueType]],
    Union[Text, bytes],
]

Body = Union[bytes, Text]

URL = Union[str, bytes, Text]
Params = _Params
Data = Union[Text, bytes, Mapping[str, Any], Mapping[Text, Any], Iterable[Tuple[Text, Optional[Text]]], IO[Text]]
Headers = MutableMapping[Text, Text]
Cookies = Union[RequestsCookieJar, MutableMapping[Text, Text]]
Files = MutableMapping[Text, IO[Any]]
Auth = Union[Tuple[Text, Text], auth.AuthBase, Callable[[PreparedRequest], PreparedRequest]]
Timeout = Union[float, Tuple[float, float], Tuple[float, None]]
AllowRedirects = bool
Proxies = MutableMapping[Text, Text]
Hooks = _HooksInput
Stream = bool
Verify = Union[bool, Text]
Cert = Union[Text, Tuple[Text, Text]]
Json = Any
