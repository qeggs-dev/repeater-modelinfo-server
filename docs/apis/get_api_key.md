# Get API Key

获取指定 uid 的模型信息

- `/model_api_key/{model_type}/{model_uid}`
  - **method**: `GET`
  - **params**:
    - `model_type`: 模型类型，详情请查看 [模型类型](../model_type.md)
    - `model_uid`: 模型 UID
  - **response**:
    - `message`: 响应信息
    - `api_keys`: API Key 列表