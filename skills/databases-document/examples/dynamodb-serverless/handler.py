"""
DynamoDB + AWS Lambda Serverless Example
Production-ready serverless API with single-table design.
"""

import json
import os
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict


# DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
table = dynamodb.Table(os.getenv('TABLE_NAME', 'AppData'))


class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder for Decimal types"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """Generate API Gateway response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }


def create_user(event, context):
    """
    Create a new user
    POST /users
    Body: { "email": "user@example.com", "name": "Jane Doe" }
    """
    try:
        body = json.loads(event['body'])
        email = body['email']
        name = body['name']
        user_id = f"USER#{email.replace('@', '_at_')}"

        # Put user metadata
        table.put_item(
            Item={
                'PK': user_id,
                'SK': 'METADATA',
                'email': email,
                'name': name,
                'createdAt': datetime.utcnow().isoformat(),
                'updatedAt': datetime.utcnow().isoformat()
            },
            ConditionExpression='attribute_not_exists(PK)'  # Prevent duplicates
        )

        return response(201, {
            'message': 'User created',
            'userId': user_id,
            'email': email,
            'name': name
        })

    except table.meta.client.exceptions.ConditionalCheckFailedException:
        return response(409, {'error': 'User already exists'})
    except Exception as e:
        return response(500, {'error': str(e)})


def get_user(event, context):
    """
    Get user by email
    GET /users/{email}
    """
    try:
        email = event['pathParameters']['email']
        user_id = f"USER#{email.replace('@', '_at_')}"

        result = table.get_item(
            Key={'PK': user_id, 'SK': 'METADATA'}
        )

        if 'Item' not in result:
            return response(404, {'error': 'User not found'})

        return response(200, result['Item'])

    except Exception as e:
        return response(500, {'error': str(e)})


def create_order(event, context):
    """
    Create a new order
    POST /orders
    Body: {
        "userId": "USER#user_at_example_com",
        "items": [...],
        "totalAmount": 249.97
    }
    """
    try:
        body = json.loads(event['body'])
        user_id = body['userId']
        items = body['items']
        total_amount = Decimal(str(body['totalAmount']))

        # Verify user exists
        user = table.get_item(Key={'PK': user_id, 'SK': 'METADATA'})
        if 'Item' not in user:
            return response(404, {'error': 'User not found'})

        # Generate order ID
        timestamp = datetime.utcnow().isoformat()
        order_id = f"ORDER#{timestamp.replace(':', '-')}"
        order_number = f"ORD-{timestamp[:10]}-{timestamp[11:13]}{timestamp[14:16]}"

        # Single-table design: multiple items
        with table.batch_writer() as batch:
            # 1. Order metadata (PK: ORDER#..., SK: METADATA)
            batch.put_item(Item={
                'PK': order_id,
                'SK': 'METADATA',
                'userId': user_id,
                'orderNumber': order_number,
                'totalAmount': total_amount,
                'status': 'pending',
                'createdAt': timestamp
            })

            # 2. User's order reference (PK: USER#..., SK: ORDER#...)
            batch.put_item(Item={
                'PK': user_id,
                'SK': order_id,
                'orderNumber': order_number,
                'totalAmount': total_amount,
                'status': 'pending',
                'createdAt': timestamp
            })

            # 3. Order items (PK: ORDER#..., SK: ITEM#...)
            for idx, item in enumerate(items):
                batch.put_item(Item={
                    'PK': order_id,
                    'SK': f"ITEM#{idx:03d}",
                    'productId': item['productId'],
                    'quantity': item['quantity'],
                    'price': Decimal(str(item['price'])),
                    'name': item['name']
                })

        return response(201, {
            'message': 'Order created',
            'orderId': order_id,
            'orderNumber': order_number
        })

    except Exception as e:
        return response(500, {'error': str(e)})


def get_order(event, context):
    """
    Get order by ID (including all items)
    GET /orders/{orderId}
    """
    try:
        order_id = event['pathParameters']['orderId']

        # Query all items for this order
        result = table.query(
            KeyConditionExpression=Key('PK').eq(order_id)
        )

        if not result['Items']:
            return response(404, {'error': 'Order not found'})

        # Separate metadata and items
        order_data = None
        items = []

        for item in result['Items']:
            if item['SK'] == 'METADATA':
                order_data = item
            elif item['SK'].startswith('ITEM#'):
                items.append(item)

        if not order_data:
            return response(404, {'error': 'Order not found'})

        order_data['items'] = items

        return response(200, order_data)

    except Exception as e:
        return response(500, {'error': str(e)})


def list_user_orders(event, context):
    """
    List all orders for a user
    GET /users/{userId}/orders
    """
    try:
        user_id = event['pathParameters']['userId']

        # Query all orders for user (PK = USER#..., SK begins_with ORDER#)
        result = table.query(
            KeyConditionExpression=Key('PK').eq(user_id) & Key('SK').begins_with('ORDER#'),
            ScanIndexForward=False  # Descending order (most recent first)
        )

        return response(200, {
            'userId': user_id,
            'orderCount': result['Count'],
            'orders': result['Items']
        })

    except Exception as e:
        return response(500, {'error': str(e)})


def update_order_status(event, context):
    """
    Update order status
    PUT /orders/{orderId}/status
    Body: { "status": "shipped" }
    """
    try:
        order_id = event['pathParameters']['orderId']
        body = json.loads(event['body'])
        new_status = body['status']

        # Update order metadata
        result = table.update_item(
            Key={'PK': order_id, 'SK': 'METADATA'},
            UpdateExpression='SET #status = :status, updatedAt = :updatedAt',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': new_status,
                ':updatedAt': datetime.utcnow().isoformat()
            },
            ConditionExpression='attribute_exists(PK)',
            ReturnValues='ALL_NEW'
        )

        # Also update user's order reference
        user_id = result['Attributes']['userId']
        table.update_item(
            Key={'PK': user_id, 'SK': order_id},
            UpdateExpression='SET #status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': new_status}
        )

        return response(200, {
            'message': 'Order status updated',
            'order': result['Attributes']
        })

    except table.meta.client.exceptions.ConditionalCheckFailedException:
        return response(404, {'error': 'Order not found'})
    except Exception as e:
        return response(500, {'error': str(e)})


def list_orders_by_status(event, context):
    """
    List orders by status using GSI
    GET /orders/status/{status}
    Requires GSI: StatusIndex (PK: status, SK: createdAt)
    """
    try:
        status_value = event['pathParameters']['status']

        # Query GSI
        result = table.query(
            IndexName='StatusIndex',
            KeyConditionExpression=Key('status').eq(status_value),
            ScanIndexForward=False  # Most recent first
        )

        return response(200, {
            'status': status_value,
            'count': result['Count'],
            'orders': result['Items']
        })

    except Exception as e:
        return response(500, {'error': str(e)})


def health_check(event, context):
    """Health check endpoint"""
    try:
        # Verify table exists
        table.table_status
        return response(200, {
            'status': 'healthy',
            'service': 'DynamoDB Lambda API',
            'tableName': table.table_name
        })
    except Exception as e:
        return response(500, {
            'status': 'unhealthy',
            'error': str(e)
        })
