from localstack.utils.aws import aws_models
lDdFb=super
lDdFP=None
lDdFO=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  lDdFb(LambdaLayer,self).__init__(arn)
  self.cwd=lDdFP
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.lDdFO.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,lDdFO,env=lDdFP):
  lDdFb(RDSDatabase,self).__init__(lDdFO,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,lDdFO,env=lDdFP):
  lDdFb(RDSCluster,self).__init__(lDdFO,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,lDdFO,env=lDdFP):
  lDdFb(AppSyncAPI,self).__init__(lDdFO,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,lDdFO,env=lDdFP):
  lDdFb(AmplifyApp,self).__init__(lDdFO,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,lDdFO,env=lDdFP):
  lDdFb(ElastiCacheCluster,self).__init__(lDdFO,env=env)
class TransferServer(BaseComponent):
 def __init__(self,lDdFO,env=lDdFP):
  lDdFb(TransferServer,self).__init__(lDdFO,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,lDdFO,env=lDdFP):
  lDdFb(CloudFrontDistribution,self).__init__(lDdFO,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,lDdFO,env=lDdFP):
  lDdFb(CodeCommitRepository,self).__init__(lDdFO,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
