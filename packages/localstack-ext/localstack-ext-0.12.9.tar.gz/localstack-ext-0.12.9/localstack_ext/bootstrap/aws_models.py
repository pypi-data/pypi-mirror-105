from localstack.utils.aws import aws_models
gHkpe=super
gHkpW=None
gHkpV=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  gHkpe(LambdaLayer,self).__init__(arn)
  self.cwd=gHkpW
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.gHkpV.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,gHkpV,env=gHkpW):
  gHkpe(RDSDatabase,self).__init__(gHkpV,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,gHkpV,env=gHkpW):
  gHkpe(RDSCluster,self).__init__(gHkpV,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,gHkpV,env=gHkpW):
  gHkpe(AppSyncAPI,self).__init__(gHkpV,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,gHkpV,env=gHkpW):
  gHkpe(AmplifyApp,self).__init__(gHkpV,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,gHkpV,env=gHkpW):
  gHkpe(ElastiCacheCluster,self).__init__(gHkpV,env=env)
class TransferServer(BaseComponent):
 def __init__(self,gHkpV,env=gHkpW):
  gHkpe(TransferServer,self).__init__(gHkpV,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,gHkpV,env=gHkpW):
  gHkpe(CloudFrontDistribution,self).__init__(gHkpV,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,gHkpV,env=gHkpW):
  gHkpe(CodeCommitRepository,self).__init__(gHkpV,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
