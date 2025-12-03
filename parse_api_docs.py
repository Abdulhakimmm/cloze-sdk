import json
import sys
import re

def extract_endpoint_details(path, methods, definitions):
    """Extract detailed information about an endpoint"""
    details = []
    
    for method, spec in methods.items():
        if method not in ['get', 'post', 'put', 'delete', 'patch']:
            continue
            
        endpoint_info = {
            'path': path,
            'method': method.upper(),
            'summary': spec.get('summary', ''),
            'description': spec.get('description', ''),
            'tags': spec.get('tags', []),
            'parameters': [],
            'responses': {},
            'security': spec.get('security', []),
            'consumes': spec.get('consumes', []),
            'produces': spec.get('produces', [])
        }
        
        # Extract parameters
        params = spec.get('parameters', [])
        if params:
            for param in params:
                if param is None:
                    continue
                param_info = {
                    'name': param.get('name', ''),
                    'in': param.get('in', ''),
                    'required': param.get('required', False),
                    'type': param.get('type', ''),
                    'description': param.get('description', ''),
                    'schema': param.get('schema', {}),
                    'enum': param.get('enum', [])
                }
                # Extract schema properties if it's a body parameter
                if param_info['in'] == 'body' and param_info.get('schema'):
                    schema = param_info['schema']
                    if 'properties' in schema:
                        param_info['body_properties'] = schema.get('properties', {})
                    if 'example' in schema:
                        param_info['example'] = schema.get('example')
                endpoint_info['parameters'].append(param_info)
        
        # Extract responses
        for status_code, response in spec.get('responses', {}).items():
            response_info = {
                'description': response.get('description', ''),
                'schema': response.get('schema', {})
            }
            # Extract example from response schema
            if response_info['schema'] and 'example' in response_info['schema']:
                response_info['example'] = response_info['schema'].get('example')
            endpoint_info['responses'][status_code] = response_info
        
        details.append(endpoint_info)
    
    return details

def format_parameter(param):
    """Format a parameter for documentation"""
    req = "**Required**" if param['required'] else "Optional"
    location = param['in']
    desc = param.get('description', '')
    
    result = f"- **`{param['name']}`** ({location}, {req})"
    if desc:
        result += f": {desc}"
    result += "\n"
    
    # Add enum values if present
    if param.get('enum'):
        result += f"  - Allowed values: {', '.join(f'`{v}`' for v in param['enum'])}\n"
    
    # Add body parameter details
    if param['in'] == 'body' and param.get('body_properties'):
        result += "  - Body properties:\n"
        for prop_name, prop_spec in param['body_properties'].items():
            prop_type = prop_spec.get('type', 'object')
            prop_desc = prop_spec.get('description', '')
            prop_enum = prop_spec.get('enum', [])
            result += f"    - `{prop_name}` ({prop_type})"
            if prop_desc:
                result += f": {prop_desc}"
            result += "\n"
            if prop_enum:
                result += f"      - Allowed values: {', '.join(f'`{v}`' for v in prop_enum)}\n"
    
    return result

def format_documentation(endpoints, definitions):
    """Format endpoints into markdown documentation"""
    doc = "# Cloze API Documentation\n\n"
    doc += "This document contains comprehensive documentation for all Cloze API endpoints and webhooks.\n\n"
    doc += "**Base URL:** `https://api.cloze.com`\n\n"
    doc += "**API Version:** 2025.10\n\n"
    doc += "## Table of Contents\n\n"
    
    # Group endpoints by tag/category
    categories = {}
    for endpoint in endpoints:
        for detail in endpoint['details']:
            for tag in detail['tags']:
                if tag not in categories:
                    categories[tag] = []
                categories[tag].append({
                    'path': detail['path'],
                    'method': detail['method'],
                    'summary': detail['summary'],
                    'description': detail['description'],
                    'parameters': detail['parameters'],
                    'responses': detail['responses'],
                    'security': detail['security'],
                    'consumes': detail['consumes'],
                    'produces': detail['produces']
                })
    
    # Generate table of contents
    category_order = ['Analytics', 'Team', 'Account', 'Projects', 'People', 'Companies', 
                     'Timeline', 'Webhooks', 'Messages']
    
    for category in category_order:
        if category in categories:
            doc += f"- [{category}](#{category.lower().replace(' ', '-')})\n"
    
    doc += "\n---\n\n"
    
    # Document each category
    for category in category_order:
        if category not in categories:
            continue
            
        doc += f"## {category}\n\n"
        
        for endpoint in sorted(categories[category], key=lambda x: (x['path'], x['method'])):
            doc += f"### {endpoint['method']} {endpoint['path']}\n\n"
            doc += f"**Summary:** {endpoint['summary']}\n\n"
            
            if endpoint['description']:
                # Clean up description (remove HTML tags, fix formatting)
                desc = endpoint['description']
                desc = re.sub(r'<br\s*/?>', '\n', desc)
                desc = re.sub(r'<[^>]+>', '', desc)
                doc += f"**Description:**\n\n{desc}\n\n"
            
            # Security requirements
            if endpoint['security']:
                doc += "**Authentication:**\n"
                for sec in endpoint['security']:
                    if isinstance(sec, dict):
                        for auth_type, scopes in sec.items():
                            if auth_type == 'OAuth2':
                                doc += f"- OAuth 2.0 (scopes: {', '.join(scopes)})\n"
                            elif auth_type == 'bearer':
                                doc += "- Bearer token (API key)\n"
                            elif auth_type == 'apiKey':
                                doc += "- API Key (query parameter or header)\n"
                    elif sec == 'bearer':
                        doc += "- Bearer token (API key)\n"
                    elif sec == 'apiKey':
                        doc += "- API Key (query parameter or header)\n"
                doc += "\n"
            
            # Content types
            if endpoint.get('consumes'):
                doc += f"**Request Content-Type:** {', '.join(endpoint['consumes'])}\n\n"
            if endpoint.get('produces'):
                doc += f"**Response Content-Type:** {', '.join(endpoint['produces'])}\n\n"
            
            # Parameters
            if endpoint['parameters']:
                doc += "**Parameters:**\n\n"
                for param in endpoint['parameters']:
                    doc += format_parameter(param)
                doc += "\n"
            
            # Request example (from body parameter)
            for param in endpoint['parameters']:
                if param['in'] == 'body' and param.get('example'):
                    doc += "**Request Example:**\n\n"
                    doc += "```json\n"
                    doc += json.dumps(param['example'], indent=2)
                    doc += "\n```\n\n"
                    break
            
            # Responses
            if endpoint['responses']:
                doc += "**Responses:**\n\n"
                for status_code, response in sorted(endpoint['responses'].items()):
                    doc += f"- **`{status_code}`**: {response['description']}\n"
                    if response.get('example'):
                        doc += "\n  **Example Response:**\n\n"
                        doc += "  ```json\n"
                        doc += "  " + json.dumps(response['example'], indent=2).replace('\n', '\n  ')
                        doc += "\n  ```\n"
                doc += "\n"
            
            doc += "---\n\n"
    
    # Add webhook events section
    doc += "## Webhook Events\n\n"
    doc += "Cloze supports the following webhook event types:\n\n"
    doc += "- `person.change` - Notifications when a person relation changes\n"
    doc += "- `project.change` - Notifications when a project relation changes\n"
    doc += "- `company.change` - Notifications when a company relation changes\n"
    doc += "- `person.audit.change` - Notifications with audit trail information when a person relation changes\n"
    doc += "- `project.audit.change` - Notifications with audit trail information when a project relation changes\n"
    doc += "- `company.audit.change` - Notifications with audit trail information when a company relation changes\n\n"
    doc += "### Webhook Notification Format\n\n"
    doc += "Webhook notifications are delivered as HTTP POST requests to your callback URL. "
    doc += "The request body contains the changed relation data in the same format used by the API for creating/updating relations.\n\n"
    doc += "### Webhook Headers\n\n"
    doc += "- `X-Cloze-Subscription-ID`: The unique subscription identifier\n"
    doc += "- `X-Cloze-Client-Reference`: The client reference (if provided during subscription)\n\n"
    doc += "### Webhook Response Requirements\n\n"
    doc += "Your webhook endpoint must respond with one of the following:\n\n"
    doc += "- `text/plain` content-type with body `OK`\n"
    doc += "- `application/json` content-type with body `{\"status\": \"ok\"}`\n\n"
    doc += "Any other response will result in subscription suspension.\n\n"
    
    return doc

def main():
    with open('swagger.json', 'r', encoding='utf-8') as f:
        swagger = json.load(f)
    
    endpoints = []
    paths = swagger.get('paths', {})
    
    for path, methods in paths.items():
        endpoint = {
            'path': path,
            'details': extract_endpoint_details(path, methods, swagger.get('definitions', {}))
        }
        endpoints.append(endpoint)
    
    # Generate documentation
    documentation = format_documentation(endpoints, swagger.get('definitions', {}))
    
    # Write to file
    with open('API_DOCUMENTATION.md', 'w', encoding='utf-8') as f:
        f.write(documentation)
    
    print(f"Documentation generated successfully!")
    print(f"Total endpoints documented: {sum(len(e['details']) for e in endpoints)}")

if __name__ == '__main__':
    main()

