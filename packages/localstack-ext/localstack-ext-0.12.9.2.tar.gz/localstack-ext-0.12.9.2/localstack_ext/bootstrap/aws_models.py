from localstack.utils.aws import aws_models
hrHWO=super
hrHWp=None
hrHWL=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  hrHWO(LambdaLayer,self).__init__(arn)
  self.cwd=hrHWp
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.hrHWL.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,hrHWL,env=hrHWp):
  hrHWO(RDSDatabase,self).__init__(hrHWL,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,hrHWL,env=hrHWp):
  hrHWO(RDSCluster,self).__init__(hrHWL,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,hrHWL,env=hrHWp):
  hrHWO(AppSyncAPI,self).__init__(hrHWL,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,hrHWL,env=hrHWp):
  hrHWO(AmplifyApp,self).__init__(hrHWL,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,hrHWL,env=hrHWp):
  hrHWO(ElastiCacheCluster,self).__init__(hrHWL,env=env)
class TransferServer(BaseComponent):
 def __init__(self,hrHWL,env=hrHWp):
  hrHWO(TransferServer,self).__init__(hrHWL,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,hrHWL,env=hrHWp):
  hrHWO(CloudFrontDistribution,self).__init__(hrHWL,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,hrHWL,env=hrHWp):
  hrHWO(CodeCommitRepository,self).__init__(hrHWL,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
