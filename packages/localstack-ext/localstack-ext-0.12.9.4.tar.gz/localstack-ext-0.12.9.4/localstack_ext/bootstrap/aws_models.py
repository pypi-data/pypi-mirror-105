from localstack.utils.aws import aws_models
nDGhu=super
nDGhy=None
nDGhf=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  nDGhu(LambdaLayer,self).__init__(arn)
  self.cwd=nDGhy
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.nDGhf.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,nDGhf,env=nDGhy):
  nDGhu(RDSDatabase,self).__init__(nDGhf,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,nDGhf,env=nDGhy):
  nDGhu(RDSCluster,self).__init__(nDGhf,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,nDGhf,env=nDGhy):
  nDGhu(AppSyncAPI,self).__init__(nDGhf,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,nDGhf,env=nDGhy):
  nDGhu(AmplifyApp,self).__init__(nDGhf,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,nDGhf,env=nDGhy):
  nDGhu(ElastiCacheCluster,self).__init__(nDGhf,env=env)
class TransferServer(BaseComponent):
 def __init__(self,nDGhf,env=nDGhy):
  nDGhu(TransferServer,self).__init__(nDGhf,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,nDGhf,env=nDGhy):
  nDGhu(CloudFrontDistribution,self).__init__(nDGhf,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,nDGhf,env=nDGhy):
  nDGhu(CodeCommitRepository,self).__init__(nDGhf,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
