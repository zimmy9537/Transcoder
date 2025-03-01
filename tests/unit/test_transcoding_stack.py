import aws_cdk as core
import aws_cdk.assertions as assertions

from transcoding.transcoding_stack import TranscodingStack

# example tests. To run these tests, uncomment this file along with the example
# resource in transcoding/transcoding_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TranscodingStack(app, "transcoding")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
