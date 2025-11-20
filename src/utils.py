import json

def getSettings():  
    with open('config/settings.json') as f:
        settings = json.load(f)
    return settings



def erdFormatByLabel(tableName, fields, allDmoLabels): # dbdiagram.io 포맷으로 변환
  tableLabel = allDmoLabels.get(tableName)
  header = f'Table "{tableLabel}" {{'
  body = ''
  footer = '\n}'
  for field in fields:
    fieldLabel = field.get('label') # 필드 레이블
    fieldType = field.get('type') # 필드 타입
    bodyFormat = f'\n  "{fieldLabel}" {fieldType}' # 필드 포맷
    # PK 체크
    keys = list(field.keys()) # 필드정보 키값 배열
    if 'isPrimaryKey' in keys: # PK인지 체크
      bodyFormat += ' [primary key]' # PK일 경우 추가
    body+=bodyFormat
  if len(body)==0: # 모두 System 타입 필드만 있는 경우
     return ''
  return header+body+footer

def erdFormatByApiName(tableName,fields): # dbdiagram.io 포맷으로 변환
  header = f'Table {tableName} {{'
  body = ''
  footer = '\n}'
  for field in fields:
    fieldName = field.get('name') # 필드 API name
    fieldType = field.get('type') # 필드 타입
    bodyFormat = f'\n  {fieldName} {fieldType}' # 필드 포맷
    # PK 체크
    keys = list(field.keys()) # 필드정보 키값 배열
    if 'isPrimaryKey' in keys: # PK인지 체크
      bodyFormat += ' [primary key]' # PK일 경우 추가
    body+=bodyFormat
  if len(body)==0: # 모두 System 타입 필드만 있는 경우
     return ''
  return header+body+footer




'''
getFieldSourceTargetRelationshipCollection 샘플 데이터
'''
{'currentPageUrl': '/services/data/v65.0/ssot/data-model-objects/cgv_branchesS3__dlm/relationships?dataspace=default&limit=20&offset=0&orderBy=filtersortorderasc&sortBy=DeveloperName', 
 'relationships': 
 [{'cardinality': 'ManyToOne', 
   'creationType': 'Custom', 
   'id': '0gegL00000KSZ0vQAH', 
   'name': 'cgv_reservationsS3_branch_id_map_cgv_branchesS3_branch_id_1760518474183', 
   'owner': 'DataCloud', 
   'sourceField': {'label': 'branch_id', 'name': 'branch_id__c', 'type': 'MktDataModelField'}, 
   'sourceObject': {'keyQualifierField': None, 'label': 'cgv_reservationsS3', 'name': 'cgv_reservationsS3__dlm'}, 
   'status': 'ACTIVE', 
   'targetField': {'label': 'branch_id', 'name': 'branch_id__c', 'type': 'MktDataModelField'}, 
   'targetObject': {'keyQualifierField': None, 'label': 'cgv_branchesS3', 'name': 'cgv_branchesS3__dlm'}}], 
 'totalSize': 1}