import oci
import time
import datetime
import os
import sys
import subprocess
import uuid
import base64
import json
from oci.loggingingestion import LoggingClient
from oci.loggingingestion.models import PutLogsDetails, LogEntryBatch, LogEntry


JOB_RUN_OCID_KEY = "JOB_RUN_OCID"
OCI_RESOURCE_PRINCIPAL_VERSION = "OCI_RESOURCE_PRINCIPAL_VERSION"
# Replace secret_id value below with the ocid of your secret
SECRET_OCID = "ocid1.vaultsecret.oc1.iad.amaaaaaanif7xwia56zwdrjuhoesurnimnqshon6v2a55fs3x3lqnyr4xkka"


class Jobs:
    def __init__(self):
        rp_version = os.environ.get(OCI_RESOURCE_PRINCIPAL_VERSION, "UNDEFINED")
        if rp_version == "UNDEFINED":
            # RUN LOCAL TEST
            self.signer = oci.config.from_file("~/.oci/config", "BIGDATA")
            self.secret_client = oci.secrets.SecretsClient(config=self.signer)
        else:
            # RUN AS JOB
            self.signer = oci.auth.signers.get_resource_principals_signer()
            self.secret_client = oci.secrets.SecretsClient(
                config={}, signer=self.signer
            )

    def install(self, package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    def read_secret_value(self, secret_id):
        secret_bundle = self.secret_client.get_secret_bundle(secret_id)
        base64_secret_content = secret_bundle.data.secret_bundle_content.content
        base64_secret_bytes = base64_secret_content.encode("ascii")
        base64_message_bytes = base64.b64decode(base64_secret_bytes)
        secret_content = base64_message_bytes.decode("ascii")
        return secret_content


try:
    job = Jobs()

    print("Start Vault Job Logging...")

    print("Logging for job run: {}".format(job.get_by_key(JOB_RUN_OCID_KEY, "LOCAL")))
    print("Current timestamp in UTC: {}".format(str(datetime.datetime.utcnow())))

    print("Init Vault")

    print("Get Vault Secret UUID: {}".format(SECRET_OCID))

    # Print secret
    secret_content = job.read_secret_value(SECRET_OCID)
    print("Secret:{}".format(secret_content))

    print("Job Done.")

except Exception as e:
    print(e)
    raise e
