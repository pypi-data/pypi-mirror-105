from localstack.utils.aws import aws_models
ekgIh=super
ekgIa=None
ekgIN=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  ekgIh(LambdaLayer,self).__init__(arn)
  self.cwd=ekgIa
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.ekgIN.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,ekgIN,env=ekgIa):
  ekgIh(RDSDatabase,self).__init__(ekgIN,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,ekgIN,env=ekgIa):
  ekgIh(RDSCluster,self).__init__(ekgIN,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,ekgIN,env=ekgIa):
  ekgIh(AppSyncAPI,self).__init__(ekgIN,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,ekgIN,env=ekgIa):
  ekgIh(AmplifyApp,self).__init__(ekgIN,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,ekgIN,env=ekgIa):
  ekgIh(ElastiCacheCluster,self).__init__(ekgIN,env=env)
class TransferServer(BaseComponent):
 def __init__(self,ekgIN,env=ekgIa):
  ekgIh(TransferServer,self).__init__(ekgIN,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,ekgIN,env=ekgIa):
  ekgIh(CloudFrontDistribution,self).__init__(ekgIN,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,ekgIN,env=ekgIa):
  ekgIh(CodeCommitRepository,self).__init__(ekgIN,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
