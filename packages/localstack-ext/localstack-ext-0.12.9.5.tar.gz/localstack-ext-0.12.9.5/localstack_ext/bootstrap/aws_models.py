from localstack.utils.aws import aws_models
XIhKm=super
XIhKR=None
XIhKn=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  XIhKm(LambdaLayer,self).__init__(arn)
  self.cwd=XIhKR
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.XIhKn.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,XIhKn,env=XIhKR):
  XIhKm(RDSDatabase,self).__init__(XIhKn,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,XIhKn,env=XIhKR):
  XIhKm(RDSCluster,self).__init__(XIhKn,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,XIhKn,env=XIhKR):
  XIhKm(AppSyncAPI,self).__init__(XIhKn,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,XIhKn,env=XIhKR):
  XIhKm(AmplifyApp,self).__init__(XIhKn,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,XIhKn,env=XIhKR):
  XIhKm(ElastiCacheCluster,self).__init__(XIhKn,env=env)
class TransferServer(BaseComponent):
 def __init__(self,XIhKn,env=XIhKR):
  XIhKm(TransferServer,self).__init__(XIhKn,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,XIhKn,env=XIhKR):
  XIhKm(CloudFrontDistribution,self).__init__(XIhKn,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,XIhKn,env=XIhKR):
  XIhKm(CodeCommitRepository,self).__init__(XIhKn,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
