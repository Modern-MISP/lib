import json

import httpx
from deepdiff import DeepDiff
from icecream import ic


def to_legacy_format(data):
    if isinstance(data, bool):
        return data
    elif isinstance(data, (int, float)):
        return str(data)
    elif isinstance(data, dict):
        return {key: to_legacy_format(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [to_legacy_format(x) for x in data]
    return data


def get_legacy_modern_diff(http_method, path, body, auth_key, client, preprocessor=None, ignore_order=True):
    clear_key, auth_key = auth_key
    headers = {"authorization": clear_key, "accept": "application/json"}

    ic("-" * 50)
    ic(f"Calling {path}")
    ic(body)

    kwargs = {"headers": headers}
    if http_method != "get":
        kwargs["json"] = body

    call = getattr(client, http_method)
    response = call(path, **kwargs)
    response_json = response.json()

    call = getattr(httpx, http_method)
    legacy_response = call(f"http://misp-core{path}", **kwargs)
    ic(legacy_response)
    legacy_response_json = legacy_response.json()
    ic("Modern MISP Response")
    ic(response_json)
    ic("Legacy MISP Response")
    ic(legacy_response_json)

    if preprocessor is not None:
        preprocessor(response_json, legacy_response_json)

    diff = DeepDiff(
        to_legacy_format(response_json),
        to_legacy_format(legacy_response_json),
        verbose_level=2,
        ignore_order=ignore_order,
    )
    ic(diff)

    # remove None values added in Modern MISP.
    # They shouldnt hurt and removing all None
    # overshoots, MISP is inconsistent when to include what.
    # Note: We don't want the opposite. If MISP includes None, Modern MISP should do this as well!
    if diff.get("dictionary_item_removed", False):
        diff["dictionary_item_removed"] = {
            k: v for k, v in diff["dictionary_item_removed"].items() if v is not None and v != [] and v != {}
        }
        if diff["dictionary_item_removed"] == {}:
            del diff["dictionary_item_removed"]

    # somehow misp manages to maintain the json encoded restricted_to_domain str in GalaxyCluster only.
    # we will ignore this, this is too broken
    if diff.get("type_changes", False):
        diff["type_changes"] = {
            k: v
            for k, v in diff["type_changes"].items()
            if not ("restricted_to_domain" in k and v["new_value"] == json.dumps(v["old_value"]))
        }
        if diff["type_changes"] == {}:
            del diff["type_changes"]

    return diff
