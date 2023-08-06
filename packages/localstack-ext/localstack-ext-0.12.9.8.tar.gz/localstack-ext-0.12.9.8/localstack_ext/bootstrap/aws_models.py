from localstack.utils.aws import aws_models
YfMjb=super
YfMjL=None
YfMjA=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  YfMjb(LambdaLayer,self).__init__(arn)
  self.cwd=YfMjL
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.YfMjA.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,YfMjA,env=YfMjL):
  YfMjb(RDSDatabase,self).__init__(YfMjA,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,YfMjA,env=YfMjL):
  YfMjb(RDSCluster,self).__init__(YfMjA,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,YfMjA,env=YfMjL):
  YfMjb(AppSyncAPI,self).__init__(YfMjA,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,YfMjA,env=YfMjL):
  YfMjb(AmplifyApp,self).__init__(YfMjA,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,YfMjA,env=YfMjL):
  YfMjb(ElastiCacheCluster,self).__init__(YfMjA,env=env)
class TransferServer(BaseComponent):
 def __init__(self,YfMjA,env=YfMjL):
  YfMjb(TransferServer,self).__init__(YfMjA,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,YfMjA,env=YfMjL):
  YfMjb(CloudFrontDistribution,self).__init__(YfMjA,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,YfMjA,env=YfMjL):
  YfMjb(CodeCommitRepository,self).__init__(YfMjA,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
