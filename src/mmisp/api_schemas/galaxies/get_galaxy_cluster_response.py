from pydantic import BaseModel

class GetGalaxyClusterResponse(BaseModel):
    id: str
    uuid: str
    collection_uuid: str
    type: str
    value: str
    tag_name: str
    description: str
    galaxy_id: str
    source: str
    Authors: Authors
    version: str
    distribution: str
    sharing_group_id: str
    org_id: str
    orgc_id: str
    default: bool
    locked: bool
    extends_uuid: str
    extends_version: str
    published: bool
    deleted: bool
    "GalaxyElement": [
      {
        "id": "string",
        "galaxy_cluster_id": "string",
        "key": "string",
        "value": "string"
      }
    ],
    "Galaxy": {
      "id": "string",
      "uuid": "string",
      "name": "string",
      "type": "string",
      "description": "string",
      "version": "string",
      "icon": "string",
      "namespace": "string",
      "enabled": true,
      "local_only": true,
      "kill_chain_order": "string"
    },
    "GalaxyClusterRelation": [],
    "Org": {
      "id": "string",
      "name": "string",
      "date_created": "2024-06-06T07:55:16.022Z",
      "date_modified": "2024-06-06T07:55:16.022Z",
      "description": "string",
      "type": "string",
      "nationality": "string",
      "sector": "string",
      "created_by": "string",
      "uuid": "string",
      "contacts": "string",
      "local": true,
      "restricted_to_domain": "string",
      "landingpage": "string"
    },
    "Orgc": {
      "id": "string",
      "name": "string",
      "date_created": "2024-06-06T07:55:16.022Z",
      "date_modified": "2024-06-06T07:55:16.022Z",
      "description": "string",
      "type": "string",
      "nationality": "string",
      "sector": "string",
      "created_by": "string",
      "uuid": "string",
      "contacts": "string",
      "local": true,
      "restricted_to_domain": "string",
      "landingpage": "string"
    }
  class Authors (BaseModel):
    "authors": [
      "string"
    ]