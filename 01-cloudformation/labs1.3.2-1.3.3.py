import json
import boto3
import sys

if len(sys.argv) > 1 and sys.argv[1] == "delete":
    delete_mode = True
else:
    delete_mode = False

with open('labs1.3.1-regions.json') as json_file:
    config = json.load(json_file)

for region in config['regions']:
   
    cfn = boto3.client('cloudformation', region_name=region)
    
    stack_name = f"test-stack-{region}"
   
    with open('labs1.3.1.yaml', 'r') as template_file:
        template_body = template_file.read()
    if delete_mode:
        try:
          
            cfn.delete_stack(StackName=stack_name)
            print(f"Stack {stack_name} deleted.")
        except cfn.exceptions.ClientError as e:
          
            if "does not exist" in str(e):
                print(f"Stack {stack_name} does not exist.")
            else:
                raise e
    else:
        try:
           
            cfn.update_stack(
                StackName=stack_name,
                TemplateBody=template_body
            )
            print(f"Stack {stack_name} updated.")
        except cfn.exceptions.ClientError as e:
           
            if "does not exist" in str(e):
                cfn.create_stack(
                    StackName=stack_name,
                    TemplateBody=template_body
                )
                print(f"Stack {stack_name} created.")
            else:
                raise e