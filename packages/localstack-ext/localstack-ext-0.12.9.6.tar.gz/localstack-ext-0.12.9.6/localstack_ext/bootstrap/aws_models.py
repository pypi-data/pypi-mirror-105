from localstack.utils.aws import aws_models
VbSos=super
VbSof=None
VbSoK=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  VbSos(LambdaLayer,self).__init__(arn)
  self.cwd=VbSof
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.VbSoK.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,VbSoK,env=VbSof):
  VbSos(RDSDatabase,self).__init__(VbSoK,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,VbSoK,env=VbSof):
  VbSos(RDSCluster,self).__init__(VbSoK,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,VbSoK,env=VbSof):
  VbSos(AppSyncAPI,self).__init__(VbSoK,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,VbSoK,env=VbSof):
  VbSos(AmplifyApp,self).__init__(VbSoK,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,VbSoK,env=VbSof):
  VbSos(ElastiCacheCluster,self).__init__(VbSoK,env=env)
class TransferServer(BaseComponent):
 def __init__(self,VbSoK,env=VbSof):
  VbSos(TransferServer,self).__init__(VbSoK,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,VbSoK,env=VbSof):
  VbSos(CloudFrontDistribution,self).__init__(VbSoK,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,VbSoK,env=VbSof):
  VbSos(CodeCommitRepository,self).__init__(VbSoK,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
