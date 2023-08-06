from localstack.utils.aws import aws_models
AMJRq=super
AMJRe=None
AMJRX=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  AMJRq(LambdaLayer,self).__init__(arn)
  self.cwd=AMJRe
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.AMJRX.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,AMJRX,env=AMJRe):
  AMJRq(RDSDatabase,self).__init__(AMJRX,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,AMJRX,env=AMJRe):
  AMJRq(RDSCluster,self).__init__(AMJRX,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,AMJRX,env=AMJRe):
  AMJRq(AppSyncAPI,self).__init__(AMJRX,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,AMJRX,env=AMJRe):
  AMJRq(AmplifyApp,self).__init__(AMJRX,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,AMJRX,env=AMJRe):
  AMJRq(ElastiCacheCluster,self).__init__(AMJRX,env=env)
class TransferServer(BaseComponent):
 def __init__(self,AMJRX,env=AMJRe):
  AMJRq(TransferServer,self).__init__(AMJRX,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,AMJRX,env=AMJRe):
  AMJRq(CloudFrontDistribution,self).__init__(AMJRX,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,AMJRX,env=AMJRe):
  AMJRq(CodeCommitRepository,self).__init__(AMJRX,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
