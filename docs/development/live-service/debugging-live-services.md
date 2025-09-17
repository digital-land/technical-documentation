# Debugging Live Services

## Async processor API

TBC

## Main application (digital-land.info)

TBC

## Planning data design

TBC

## Check and Provide service

### Check service error

When the check service is returning an error, the best way to debug it is to use the async processor API to check the data.

To do this, follow the steps below:

1. Get a check request ID from the check service.
   This can be found in the URL of the check tool. It will be a long string of characters, for example: `https://provide.planning.data.gov.uk/check/results/bJKVgr5DmDCwXYgCLX4umk/28` the ID would be `bJKVgr5DmDCwXYgCLX4umk`.
2. Use the async processor API to check the data.
   The API is available at `http://production-pub-async-api-lb-636110663.eu-west-2.elb.amazonaws.com/requests/{check_request_id}`.
   This will return the check request status and the results.
   The results will be a JSON object with the following fields:
   - `status`: The status of the check request.
   - `response.data`: The results of the check request.
   - `response.error`: The errors of the check request.
3. The status can be `COMPLETE`, but may still have `response.error`.
4. If the status is `COMPLETE` and there is no `response.error`, then the data is valid.
