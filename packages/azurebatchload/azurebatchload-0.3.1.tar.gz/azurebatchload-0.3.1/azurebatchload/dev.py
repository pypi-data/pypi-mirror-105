# flake8: noqa
import time
import os
from azurebatchload.upload import Upload
from azurebatchload.download import Download
from azurebatchload.utils import Utils
import pandas as pd

from dotenv import load_dotenv

load_dotenv(override=True, verbose=True)


# Download(
#     destination="data",
#     source="twinfield",
#     folder="xml_responses/vrk/20201117",
#     method="single"
# ).download()

Upload(
    destination="test",
    source="data",
    method="single",
    extension=".xml",
    overwrite=True
).upload()

# files = Utils(
#     container="test", name_starts_with="data", dataframe=True, extended_info=True
# ).list_blobs()
#
# print(files)
