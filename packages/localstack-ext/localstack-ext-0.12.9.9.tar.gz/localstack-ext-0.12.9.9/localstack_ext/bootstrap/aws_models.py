from localstack.utils.aws import aws_models
xtXGb=super
xtXGR=None
xtXGP=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  xtXGb(LambdaLayer,self).__init__(arn)
  self.cwd=xtXGR
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.xtXGP.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,xtXGP,env=xtXGR):
  xtXGb(RDSDatabase,self).__init__(xtXGP,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,xtXGP,env=xtXGR):
  xtXGb(RDSCluster,self).__init__(xtXGP,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,xtXGP,env=xtXGR):
  xtXGb(AppSyncAPI,self).__init__(xtXGP,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,xtXGP,env=xtXGR):
  xtXGb(AmplifyApp,self).__init__(xtXGP,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,xtXGP,env=xtXGR):
  xtXGb(ElastiCacheCluster,self).__init__(xtXGP,env=env)
class TransferServer(BaseComponent):
 def __init__(self,xtXGP,env=xtXGR):
  xtXGb(TransferServer,self).__init__(xtXGP,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,xtXGP,env=xtXGR):
  xtXGb(CloudFrontDistribution,self).__init__(xtXGP,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,xtXGP,env=xtXGR):
  xtXGb(CodeCommitRepository,self).__init__(xtXGP,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
