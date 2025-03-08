"""
API templates for the API Gateway
"""

ERROR_MAPPING_TEMPLATE = """
# set($inputRoot=$input.path('$'))
# set($body=$util.parseJson($input.path('$.body')))
{
  "statusCode": "$body.statusCode",
  "body": {
    "message": "$body.body.message"
  }
}
"""

OUTPUT_MAPPING_TEMPLATE = """
#set($context.responseOverride.status = $input.path('$.statusCode'))
$input.json('$.body')
"""

REQUEST_TEMPLATE = """
#set($allParams = $input.params())
{
  "body": $input.json('$'),
  "params": {
  #foreach($type in $allParams.keySet())
    #set($params = $allParams.get($type))
  "$type": {
      #foreach($paramName in $params.keySet())
      "$paramName": "$util.escapeJavaScript($params.get($paramName))"
        #if($foreach.hasNext), #end
      #end
  }
    #if($foreach.hasNext), #end
  #end
  },
  "context": {
    "api-id": "$context.apiId",
    "http-method": "$context.httpMethod",
    "resource-path": "$context.resourcePath"
  }
}
"""