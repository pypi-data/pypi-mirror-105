from localstack.utils.aws import aws_models
Xshwe=super
Xshwc=None
XshwJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Xshwe(LambdaLayer,self).__init__(arn)
  self.cwd=Xshwc
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.XshwJ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,XshwJ,env=Xshwc):
  Xshwe(RDSDatabase,self).__init__(XshwJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,XshwJ,env=Xshwc):
  Xshwe(RDSCluster,self).__init__(XshwJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,XshwJ,env=Xshwc):
  Xshwe(AppSyncAPI,self).__init__(XshwJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,XshwJ,env=Xshwc):
  Xshwe(AmplifyApp,self).__init__(XshwJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,XshwJ,env=Xshwc):
  Xshwe(ElastiCacheCluster,self).__init__(XshwJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,XshwJ,env=Xshwc):
  Xshwe(TransferServer,self).__init__(XshwJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,XshwJ,env=Xshwc):
  Xshwe(CloudFrontDistribution,self).__init__(XshwJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,XshwJ,env=Xshwc):
  Xshwe(CodeCommitRepository,self).__init__(XshwJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
