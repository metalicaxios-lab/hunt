def handler(event, context):
    """Test endpoint for Vercel"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': '{"message":"Test endpoint working","status":"success"}'
    }
