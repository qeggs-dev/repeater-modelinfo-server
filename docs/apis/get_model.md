# Get Model

获取指定 uid 的模型信息

- `/model_info/{model_type}/{model_uid}`
  - **method**: `GET`
  - **params**:
    - `model_type`: 模型类型，详情请查看 [模型类型](../model_type.md)
    - `model_uid`: 模型 UID
  - **response**:
    - `message`: 响应信息
    - `models`: 与 UID 匹配的模型列表，单元结构请查看 [Model Info Object](../model_info_obj.md)