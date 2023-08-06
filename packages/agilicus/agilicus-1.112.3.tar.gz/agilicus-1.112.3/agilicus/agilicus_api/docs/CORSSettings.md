# CORSSettings

CORSSettings controls the Cross-Origin Resource Sharing (CORS) policy of an Application. This allows an application to control which origins may request content from it. 
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allow_origins** | [**list[CORSOrigin]**](CORSOrigin.md) | Lists the origins allowed to access the resources of this application. Any matching origin will have its value echoed back in the &#x60;Access-Control-Allow-Origin&#x60; header.  | 
**allow_methods** | **list[str]** | The methods for which to allow access to resources. These correspond to the &#x60;Access-Conrol-Allow-Methods&#x60; header, into which they are joined by commas. If this value is null, then the methods are wildcarded. Set a value to &#39;*&#39; to wildcard.  | 
**allow_headers** | **list[str]** | The headers which may be sent in a request to resources from this application. These correspond to the &#x60;Access-Conrol-Allow-Headers&#x60; header, into which they are joined by commas. If this value is null, then the headers are wildcarded. Set a value to &#39;*&#39; to wildcard.  | 
**expose_headers** | **list[str]** | The response headers which the javascript running in the browser may access for resources from this application. These correspond to the &#x60;Access-Conrol-Expose-Headers&#x60; header, into which they are joined by commas. If this value is null, then the headers are wildcarded. Set a value to &#39;*&#39; to wildcard.  | 
**max_age_seconds** | **int** | This sets the &#x60;Access-Control-Max-Age&#x60; which controls the maximum number of seconds for which the results of the CORS preflight check may be cached. -1 disables caching.  | 
**allow_credentials** | **bool** | Whether credentials may be sent in requests. This corresponds to the &#x60;Access-Control-Allow-Credentials&#x60; header.  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


