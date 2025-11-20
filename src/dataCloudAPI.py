import requests
from utils import getSettings
from oauthAPI import getOauthToken

def getAllSobjects(instance_url,access_token): # 모든 SObject의 메타데이터 가져오기
    '''
    API문서: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_describeGlobal.htm
    '''
    # 헤더
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    # 요청 URL
    settings = getSettings()
    api_version = settings['api_version']
    url = f"{instance_url}/services/data/{api_version}/sobjects"
    try:
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e: # 통신 오류
        print(f'HTTP 오류: {e.response.status_code}')
        print(f'응답: {e.response.text}')
        return None
    except Exception as e: # 기타 오류
        print(f'SObject 호출 오류: {e}')
        return None


def getDataModelObject(instance_url,access_token,dataModelObjectName): # 해당 DMO의 모든 정보 불러오기
    '''
    API문서: https://developer.salesforce.com/docs/data/connectapi/references/spec?meta=getDataModelObject
    '''
    # URI parameters
    dne_cdpInstanceUrl = instance_url
    settings = getSettings()
    api_version = settings['api_version']
    # 요청 URL
    url = f'{dne_cdpInstanceUrl}/services/data/{api_version}/ssot/data-model-objects/{dataModelObjectName}'
    # 헤더
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url,headers=headers)
        return response.json()
    except requests.exceptions.HTTPError as e: # 통신 오류
        print(f'HTTP 오류: {e.response.status_code}')
        print(f'응답: {e.response.text}')
        return None
    except Exception as e: # 기타 오류
        print(f'getDataModelObject() 오류: {e}')
        return None

# def getObjectDetails(instance_url, access_token, dataModelObjectName):
#     """특정 객체의 상세 정보 (필드 포함) 가져오기"""
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json'
#     }
#     url = f"{instance_url}/services/data/v59.0/sobjects/{dataModelObjectName}/describe"
    
#     try:
#         response = requests.get(url, headers=headers)
#         return response.json()
#     except Exception as e:
#         print(f'getObjectDetails 오류: {e}')
#         return None

def getFieldSourceTargetRelationshipCollection(instance_url , access_token , dataModelObjectName):
    #url
    settings = getSettings()
    api_version = settings['api_version']
    dne_cdpInstanceUrl = instance_url
    url = f'{dne_cdpInstanceUrl}/services/data/{api_version}/ssot/data-model-objects/{dataModelObjectName}/relationships'
    # 헤더
    header = {
        'Authorization': f'Bearer {access_token}'
    }
    try:
        response = requests.get(headers=header , url=url)
        return response.json()
    except Exception as e:
        print(f'getFieldSourceTargetRelationshipCollection 오류: {e}')
        print(f'DMO Name: {dataModelObjectName}')
        return None

# 테스트용 코드
if __name__ == '__main__':
    '''
    토큰, Dne_cdpInstanceUrl 발급
    '''
    oauth = getOauthToken()
    ACCESS_TOKEN = oauth['access_token']
    INSTANCE_URL = oauth['instance_url']

    '''
    getDataModelObject() Test
    '''
    # # ex) getDataModelObject() -> cgv_branchesS3__dlm 추출
    # objectName = 'cgv_branchesS3__dlm' 
    # dmo = getDataModelObject(instance_url=INSTANCE_URL,access_token=ACCESS_TOKEN,dataModelObjectName=objectName)
    # print(dmo)

    '''
    getAllSobjects() Test
    '''
    # # getAllSobjects()
    # allSobjects = getAllSobjects(instance_url=INSTANCE_URL,access_token=ACCESS_TOKEN)
    # print(allSobjects)
    
    '''
    Object Detail Test
    '''
    #dmoName = 'cgv_branchesS3__dlm'
    # res = getObjectDetails(instance_url = INSTANCE_URL, access_token = ACCESS_TOKEN, dataModelObjectName = dmoName)
    # keys = list(res.keys())
    # fields = res['fields']
    # for field in fields:
    #     idLookup = field.get('idLookup')
    #     if idLookup:
    #         name = field.get('name')
    #         print(name)
    list = ['ssot__Individual__dlm','ssot__ContactPointEmail__dlm', 'ssot__ContactPointPhone__dlm']
    dmoName = 'ssot__Individual__dlm'
    relationships = getFieldSourceTargetRelationshipCollection(INSTANCE_URL , ACCESS_TOKEN , list[1])
    relationships = relationships.get('relationships')
    for relation in relationships:
        print(relation)
    

  




