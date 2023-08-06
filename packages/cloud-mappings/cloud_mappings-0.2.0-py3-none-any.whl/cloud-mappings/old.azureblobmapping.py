from __future__ import annotations

from typing import MutableMapping
from urllib.parse import quote, unquote

from azure.core import MatchConditions
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import ContainerClient


def _safe_key(key: str) -> str:
    if not isinstance(key, str):
        raise TypeError("Key must be of type 'str'. Got key:", key)
    return quote(key)

def _unsafe_key(key: str) -> str:
    return unquote(key)

class AzureBlobMapping(MutableMapping):
    etags: dict[str, str]
    _container_client: ContainerClient
    def __init__(
        self,
        account_url: str,
        container_name: str,
        credential=None,
        serialisation: str="raw",
        create_container_metadata: dict[str, str]=None,
    ) -> None:
        self._container_client = ContainerClient(
            account_url=account_url,
            container_name=container_name,
            credential=credential,
        )
        self.etags = {}
        try:
            if create_container_metadata is None:
                metadata = {}
            else:
                metadata = create_container_metadata
            metadata["serialisation"] = serialisation
            self._container_client.create_container(metadata=metadata)
        except ResourceExistsError:
            self.sync_with_container()

    @classmethod
    def create_with_pickle(
        cls,
        account_url: str,
        container_name: str,
        credential=None,
        create_container_metadata: dict[str, str]=None,
    ) -> MutableMapping:
        from zict import Func
        import pickle
        return Func(
            pickle.dumps,
            pickle.loads,
            AzureBlobMapping(
                account_url=account_url,
                container_name=container_name,
                credential=credential,
                serialisation="pickle",
                create_container_metadata=create_container_metadata,
            )
        )

    def sync_with_container(self, key: str=None) -> None:
        container_prefix = _safe_key(key) if key is not None else None
        self.etags.update({ _unsafe_key(b.name): b.etag 
            for b in self._container_client.list_blobs(
                name_starts_with=container_prefix
            )
        })

    def __getitem__(self, key: str) -> bytes:
        if key not in self.etags:
            raise KeyError(key)
        return self._container_client.download_blob(
            blob=_safe_key(key),
            etag=self.etags[key],
            match_condition=MatchConditions.IfNotModified,
        ).readall()

    def __setitem__(self, key: str, value: bytes) -> None:
        expecting_blob = key in self.etags
        args = { 'overwrite': expecting_blob }
        if expecting_blob:
            args['etag'] = self.etags[key]
            args['match_condition'] = MatchConditions.IfNotModified
        bc = self._container_client.get_blob_client(blob=_safe_key(key))
        response = bc.upload_blob(
            data=value,
            **args,
        )
        self.etags[key] = response['etag']

    def __delitem__(self, key: str) -> None:
        if key not in self.etags:
            raise KeyError(key)
        self._container_client.delete_blob(
            blob=_safe_key(key),
            etag=self.etags[key],
            match_condition=MatchConditions.IfNotModified,
        )
        del self.etags[key]

    def __contains__(self, key: str) -> bool:
        return key in self.etags

    def keys(self):
        return iter(self.etags.keys())

    __iter__ = keys
    
    def __len__(self) -> int:
        return len(self.etags)