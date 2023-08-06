from .basecloudmapping import CloudStorageMapping
from .cloudstorage.azureblobstorage import AzureBlobStorage


class AzureBlobMapping(CloudStorageMapping):
    def __init__(
        self,
        account_url: str,
        container_name: str,
        credential=None,
        metadata: dict[str, str]=None,
    ) -> None:
        azureblobstorage = AzureBlobStorage(
            account_url=account_url,
            container_name=container_name,
            credential=credential
        )
        super().__init__(azureblobstorage, metadata)
