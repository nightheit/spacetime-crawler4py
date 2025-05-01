import requests
import cbor
import time

from utils.response import Response

# def download(url, config, logger=None):
#     host, port = config.cache_server
#     resp = requests.get(
#         f"http://{host}:{port}/",
#         params=[("q", f"{url}"), ("u", f"{config.user_agent}")])
#     try:
#         if resp and resp.content:
#             return Response(cbor.loads(resp.content))
#     except (EOFError, ValueError) as e:
#         pass
#     logger.error(f"Spacetime Response error {resp} with url {url}.")
#     return Response({
#         "error": f"Spacetime Response error {resp} with url {url}.",
#         "status": resp.status_code,
#         "url": url})

#### temporary workaround to search real web, delete before testing
import pickle
def download(url, config, logger=None):
    try:
        resp = requests.get(url)
    except requests.exceptions.RequestException as e:
        return Response({
            "url":   url,
            "status": 603,
            "error": str(e)
        })
    return Response({
        "url":    url,
        "status": resp.status_code,
        "response": pickle.dumps(resp)
    })