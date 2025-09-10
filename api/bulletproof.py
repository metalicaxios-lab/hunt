from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

def handler(request):
    """Pure serverless function handler for Vercel"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': '{"message":"API is working","status":"healthy"}'
    }
