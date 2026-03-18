# Get All Model

获取所有 uid 的模型信息

- `/model_info/{model_type}`
  - **method**: `GET`
  - **params**:
    - `model_type`: 模型类型，详情请查看 [模型类型](../model_type.md)
  - **query**:
    - `with_api_key`: 是否返回 API Key，设置为 `true` 时接口会返回 [Static Model Info Object](../model_info_obj.md#static-model-info-object)
  - **response**:
    - `message`: 响应信息
    - `models`: 模型列表，单元结构请查看 [Model Info Object](../model_info_obj.md)