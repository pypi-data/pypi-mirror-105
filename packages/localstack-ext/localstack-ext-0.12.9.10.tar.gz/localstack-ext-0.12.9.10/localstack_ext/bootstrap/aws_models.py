from localstack.utils.aws import aws_models
WIHOc=super
WIHOL=None
WIHOY=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  WIHOc(LambdaLayer,self).__init__(arn)
  self.cwd=WIHOL
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.WIHOY.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,WIHOY,env=WIHOL):
  WIHOc(RDSDatabase,self).__init__(WIHOY,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,WIHOY,env=WIHOL):
  WIHOc(RDSCluster,self).__init__(WIHOY,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,WIHOY,env=WIHOL):
  WIHOc(AppSyncAPI,self).__init__(WIHOY,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,WIHOY,env=WIHOL):
  WIHOc(AmplifyApp,self).__init__(WIHOY,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,WIHOY,env=WIHOL):
  WIHOc(ElastiCacheCluster,self).__init__(WIHOY,env=env)
class TransferServer(BaseComponent):
 def __init__(self,WIHOY,env=WIHOL):
  WIHOc(TransferServer,self).__init__(WIHOY,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,WIHOY,env=WIHOL):
  WIHOc(CloudFrontDistribution,self).__init__(WIHOY,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,WIHOY,env=WIHOL):
  WIHOc(CodeCommitRepository,self).__init__(WIHOY,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
