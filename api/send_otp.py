import json

def handler(request):
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    if request.method == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        import urllib.request
        import urllib.parse
        
        body = json.loads(request.body)
        mobile = body.get('mobile', '')
        otp = body.get('otp', '')
        
        if not mobile or not otp:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'success': False, 'error': 'mobile and otp required'})
            }
        
        # Fast2SMS API
        API_KEY = 'c7vqZWIAUo6tHSYJXLe83OlmzPKxg52dTs0ipay9GkFEhwrQMNh8m5FlMHfSsqtETC4nQIGjJV9DwW7z'
        
        url = f'https://www.fast2sms.com/dev/bulkV2?authorization={API_KEY}&variables_values={otp}&route=otp&numbers={mobile}'
        
        req = urllib.request.Request(url, headers={'cache-control': 'no-cache'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'success': True, 'result': result})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'success': False, 'error': str(e)})
        }
