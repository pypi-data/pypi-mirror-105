from localstack.utils.aws import aws_models
DhPBx=super
DhPBs=None
DhPBy=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  DhPBx(LambdaLayer,self).__init__(arn)
  self.cwd=DhPBs
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.DhPBy.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,DhPBy,env=DhPBs):
  DhPBx(RDSDatabase,self).__init__(DhPBy,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,DhPBy,env=DhPBs):
  DhPBx(RDSCluster,self).__init__(DhPBy,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,DhPBy,env=DhPBs):
  DhPBx(AppSyncAPI,self).__init__(DhPBy,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,DhPBy,env=DhPBs):
  DhPBx(AmplifyApp,self).__init__(DhPBy,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,DhPBy,env=DhPBs):
  DhPBx(ElastiCacheCluster,self).__init__(DhPBy,env=env)
class TransferServer(BaseComponent):
 def __init__(self,DhPBy,env=DhPBs):
  DhPBx(TransferServer,self).__init__(DhPBy,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,DhPBy,env=DhPBs):
  DhPBx(CloudFrontDistribution,self).__init__(DhPBy,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,DhPBy,env=DhPBs):
  DhPBx(CodeCommitRepository,self).__init__(DhPBy,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
