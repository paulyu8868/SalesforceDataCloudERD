from utils import *
from oauthAPI import getOauthToken
from dataCloudAPI import *


def getAllDmoApiNames(url,token): # DMO(dlm)만 필터링 -> 모든 DMO의 API 이름만 담기
    '''
    설명: 모든 DMO API 이름 목록 반환
    필터링 기준: API명이 __dlm 으로 끝나는 Sobject
    반환 타입: list
    '''
    # 모든 SObject 호출
    sobjects = getAllSobjects(instance_url=url,access_token=token)
    sobjects = sobjects['sobjects']
    # dmo api명 배열
    dmoApiNames = []
    for obj in sobjects:
        name = obj['name'] 
        if name.endswith('__dlm'): # api명이 __dlm으로 끝나는 Object만 담기
            dmoApiNames.append(name)
    return dmoApiNames # 모든 DMO의 API 이름이 담긴 배열 반환

def fieldFiltering(fields): # 실제 사용하는 DMO인지 체크
    filtered = []
    for field in fields:
        creationType = field.get('creationType')
        isMapped = field.get('isMapped')
        if (creationType != 'System') and isMapped: # 시스템 필드가 아니고 매핑된 애들만 count
           filtered.append(field)
    return filtered

def getAllDmoFields(url,token):
    '''
    설명: 모든 필드 메타데이터 + DMO 레이블명 가져오기
    - 키값은 API명으로 조회 가능 ex) allDmoFieldsDict.get('dmo_api_name')
    반환타입: list(dict,dict)
    '''
    # 전체 DMO API명 가져오기
    dmoApiNames = getAllDmoApiNames(url,token)
    # dmo 필드 메타데이타 , dmo 레이블
    allDmoFieldsDict = dict() # key(DMO API name),value(Field 메타데이터 리스트)
    allDmoLabelDict = dict() # key(DMO API name), value(DMO Label)
    for dmoApiName in dmoApiNames:
        fieldsInfo = getDataModelObject(url,token,dmoApiName) # 해당 DMO의 메타데이터 호출
        if fieldsInfo.get('creationType') != 'System': # Custom,Standard 오브젝트만 추출
          # 필드 정보 담기
          fieldsMeta = fieldsInfo['fields'] # 필드 메타데이터 배열
          fieldsMeta = fieldFiltering(fieldsMeta)
          if len(fieldsMeta)>0:
            allDmoFieldsDict[dmoApiName] = fieldsMeta
            # Label 담기
            dmoLabel = fieldsInfo['label']
            allDmoLabelDict[dmoApiName] = dmoLabel
    return [allDmoFieldsDict , allDmoLabelDict] # dmo 필드 메타데이터 딕셔너리 , dmo 레이블 딕셔너리

def getAllRelationshipsByErdFormat(url,token,allDmoApiNames):
    resByApiName = set()
    resByLabel = set()
    #checkList = ['ssot__ContactPointEmail__dlm','ssot__ContactPointPhone__dlm','ssot__Individual__dlm','UnifiedIndividual__dlm']
    for dmoApiName in allDmoApiNames:
        relationships = getFieldSourceTargetRelationshipCollection(instance_url= url , access_token= token, dataModelObjectName= dmoApiName) 
        if relationships: # relationship 있을때만
            relationships = relationships['relationships'] # 리스트 반환
            # 모든 relationships 순회
            for relationship in relationships:
                # if dmoApiName in checkList:
                #     print(relationship)
                '''정보 추출'''
                # 필터링 정보
                creationType = relationship['creationType']
                cardinality = relationship['cardinality']
                status = relationship['status']
                # 소스필드 정보
                sourceField = relationship['sourceField']
                sourceFieldLabel = sourceField['label']
                sourceFieldApiName = sourceField['name']
                sourceObject = relationship['sourceObject']
                sourceObjectLabel = sourceObject['label']
                sourceObjectApiName = sourceObject['name']
                # 타켓 필드 정보
                targetField = relationship['targetField']
                targetFieldLabel = targetField['label']
                targetFieldApiName = targetField['name']
                targetObject = relationship['targetObject']
                targetObjectLabel = targetObject['label']
                targetObjectApiName = targetObject['name']
                # 포멧
                #isSameName = sourceObjectApiName==dmoApiName
                checkSourceObject = sourceObjectApiName in allDmoApiNames
                checkTargetObject = targetObjectApiName in allDmoApiNames
                if creationType != 'Segment_Membership' and checkSourceObject and checkTargetObject:
                  if cardinality == 'ManyToOne':
                      branch = '>'
                      apiNameFormat = f'Ref: {sourceObjectApiName}.{sourceFieldApiName} {branch} {targetObjectApiName}.{targetFieldApiName}'
                      labelFormet = f'Ref: {sourceObjectLabel}.{sourceFieldLabel} {branch} {targetObjectLabel}.{targetFieldLabel}'
                  elif cardinality == 'OneToOne':
                      branch = '-'
                      apiNameFormat = f'Ref: {sourceObjectApiName}.{sourceFieldApiName} {branch} {targetObjectApiName}.{targetFieldApiName}'
                      labelFormet = f'Ref: {sourceObjectLabel}.{sourceFieldLabel} {branch} {targetObjectLabel}.{targetFieldLabel}'
                  else:
                      print(f"Cardinality 예외:{cardinality}")
                      continue
                  resByApiName.add(apiNameFormat)
                  resByLabel.add(labelFormet)
    return [resByApiName,resByLabel]

if __name__ == '__main__':
    # 토큰,인스턴스 URL 발급
    oauthInfo = getOauthToken() 
    ACCESS_TOKEN = oauthInfo['access_token'] # 토큰
    INSTANCE_URL = oauthInfo['instance_url'] # dne_Instance

    '''모든 DMO 이름 및 필드 정보 추출'''
    allDmoFields, allDmoLabels = getAllDmoFields(url=INSTANCE_URL,token=ACCESS_TOKEN) # 모든 필드 정보 딕셔너리
    allDmoApiNames = list(allDmoFields.keys()) # 모든 DMO API 이름 리스트
    '''relationship 추출'''
    relationshipsByApiName , relationshipsByLabel = getAllRelationshipsByErdFormat(INSTANCE_URL,ACCESS_TOKEN,allDmoApiNames)
 
    
    '''특정 테이블만 출력'''
    # tableName = 'cgv_branchesS3__dlm'
    # cgvFields = allDmoFields[tableName]
    # print(erdFormatByApiName(tableName = tableName , fields= cgvFields))

    '''모든 테이블 출력(API Name으로 출력)'''
    # for dmoApiName in allDmoApiNames: # 테이블 출력
    #     fields = allDmoFields[dmoApiName]
    #     print(erdFormatByApiName(tableName=dmoApiName , fields=fields))
    # print('// ======== relationships 출력 ========')
    for relationship in relationshipsByApiName: # relationships 출력
        print(relationship)


    '''모든 테이블 출력(Label로 출력)'''
    # for dmoApiName in allDmoApiNames:
    #   fields = allDmoFields[dmoApiName]
    #   print(erdFormatByLabel(tableName=dmoApiName , fields=fields, allDmoLabels = allDmoLabels))

    




