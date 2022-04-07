How to get access token  https://cloud.google.com/sdk/gcloud/reference/auth/application-default/print-access-token

Workflow execution REST API  https://cloud.google.com/workflows/docs/executing-workflow#rest-api
                             https://cloud.google.com/workflows/docs/passing-runtime-arguments


Request 

{"argument": "{\"pName\":\"Laptop\",\"quantity\":\"60\"}"}

Put an Order for Approval (executing the workflow) via API Gateway

curl --request POST \
  --url http://YOUR_VM:8080/orders \
  --header 'Authorization: Bearer YOUR_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{"argument": "{\"pName\":\"Laptop\",\"quantity\":\"60\"}"}'
 
The result from the above call will include an EXECUTION ID, for example,

{
  "argument": "{\"pName\":\"Laptop\",\"quantity\":\"60\"}",
  "name": "projects/913700463742/locations/us-central1/workflows/order-approval-process-1/executions/366b3c47-85fd-4bec-aace-fab495953644",
  "startTime": "2021-04-23T10:03:17.412308038Z",
  "state": "ACTIVE",
  "workflowRevisionId": "000009-e3c"
}

e.g., 366b3c47-85fd-4bec-aace-fab495953644
  
Get the result of the execution via API gateway

curl --request GET \
  --url http://YOUR_VM:8080/orders/EXEUTION_ID \
  --header 'Authorization: Bearer YOUR_TOKEN'
  
  e.g, EXEUTION_ID 366b3c47-85fd-4bec-aace-fab495953644
