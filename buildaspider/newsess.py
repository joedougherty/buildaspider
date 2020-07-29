import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def mint_new_session(max_num_retries=5):
    adapter = HTTPAdapter(max_retries=Retry(total=max_num_retries, backoff_factor=1))
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
