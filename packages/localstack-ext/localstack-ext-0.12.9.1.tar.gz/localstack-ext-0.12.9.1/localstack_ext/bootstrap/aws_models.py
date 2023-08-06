from localstack.utils.aws import aws_models
uNkiW=super
uNkir=None
uNkif=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  uNkiW(LambdaLayer,self).__init__(arn)
  self.cwd=uNkir
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.uNkif.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,uNkif,env=uNkir):
  uNkiW(RDSDatabase,self).__init__(uNkif,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,uNkif,env=uNkir):
  uNkiW(RDSCluster,self).__init__(uNkif,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,uNkif,env=uNkir):
  uNkiW(AppSyncAPI,self).__init__(uNkif,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,uNkif,env=uNkir):
  uNkiW(AmplifyApp,self).__init__(uNkif,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,uNkif,env=uNkir):
  uNkiW(ElastiCacheCluster,self).__init__(uNkif,env=env)
class TransferServer(BaseComponent):
 def __init__(self,uNkif,env=uNkir):
  uNkiW(TransferServer,self).__init__(uNkif,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,uNkif,env=uNkir):
  uNkiW(CloudFrontDistribution,self).__init__(uNkif,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,uNkif,env=uNkir):
  uNkiW(CodeCommitRepository,self).__init__(uNkif,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
