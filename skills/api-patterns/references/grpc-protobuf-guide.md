# gRPC and Protocol Buffers Guide

## Overview

gRPC is a high-performance RPC framework using Protocol Buffers for service-to-service communication. This guide covers proto3 syntax, service definitions, streaming patterns, and implementation examples.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Protocol Buffers (Proto3)](#protocol-buffers-proto3)
- [Service Definitions](#service-definitions)
- [Streaming Patterns](#streaming-patterns)
- [Rust: Tonic](#rust-tonic)
- [Go: Connect-Go](#go-connect-go)
- [Python: grpcio](#python-grpcio)
- [Error Handling](#error-handling)

## Core Concepts

### When to Use gRPC

✅ **Use gRPC when:**
- Service-to-service communication (microservices)
- High-performance requirements
- Strong typing and contract enforcement needed
- Bidirectional streaming needed
- Polyglot services (multiple languages)

❌ **Avoid gRPC when:**
- Browser clients (limited support, use Connect-Go for browser compatibility)
- Simple CRUD APIs (REST simpler)
- Human-readable debugging required (binary protocol)
- Public APIs (REST more accessible)

### gRPC vs REST

| Feature | gRPC | REST |
|---------|------|------|
| **Protocol** | HTTP/2 (binary) | HTTP/1.1 (text) |
| **Performance** | Faster (binary, multiplexing) | Slower (text, no multiplexing) |
| **Streaming** | Bidirectional built-in | Limited (SSE for server-side) |
| **Contract** | Protobuf schema (strict) | OpenAPI (optional) |
| **Browser** | Limited (gRPC-Web required) | Native support |
| **Debugging** | Harder (binary) | Easier (text) |
| **Code generation** | Required | Optional |

## Protocol Buffers (Proto3)

### Basic Syntax

```protobuf
// user.proto
syntax = "proto3";

package example.v1;

// Message definition
message User {
  string id = 1;
  string name = 2;
  string email = 3;
  int32 age = 4;
  Role role = 5;
  repeated string tags = 6;  // List of strings
  google.protobuf.Timestamp created_at = 7;
}

// Enum definition
enum Role {
  ROLE_UNSPECIFIED = 0;  // First value must be 0
  ROLE_USER = 1;
  ROLE_ADMIN = 2;
  ROLE_MODERATOR = 3;
}
```

### Field Numbers

**Rules:**
- Must be unique within a message
- Cannot be changed once in use (breaks compatibility)
- 1-15 use 1 byte (use for frequently set fields)
- 16-2047 use 2 bytes
- 19000-19999 are reserved

### Data Types

| Proto Type | Go | Rust | Python | TypeScript |
|------------|----|----- |--------|------------|
| `double` | float64 | f64 | float | number |
| `float` | float32 | f32 | float | number |
| `int32` | int32 | i32 | int | number |
| `int64` | int64 | i64 | int | number/string |
| `bool` | bool | bool | bool | boolean |
| `string` | string | String | str | string |
| `bytes` | []byte | Vec<u8> | bytes | Uint8Array |

### Nested Messages

```protobuf
message User {
  string id = 1;
  string name = 2;
  Address address = 3;

  message Address {
    string street = 1;
    string city = 2;
    string country = 3;
  }
}
```

### Maps

```protobuf
message UserProfile {
  string user_id = 1;
  map<string, string> metadata = 2;  // Key-value pairs
}
```

### Oneof (Union Types)

```protobuf
message SearchRequest {
  string query = 1;

  oneof filter {
    string tag = 2;
    string category = 3;
    int32 year = 4;
  }
}
```

### Importing Other Protos

```protobuf
import "google/protobuf/timestamp.proto";
import "common/types.proto";

message Post {
  string id = 1;
  string title = 2;
  google.protobuf.Timestamp created_at = 3;
  common.User author = 4;
}
```

## Service Definitions

### Basic Service

```protobuf
syntax = "proto3";

package user.v1;

service UserService {
  // Unary RPC (single request, single response)
  rpc GetUser(GetUserRequest) returns (GetUserResponse);

  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);

  rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);

  rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);

  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
}

message GetUserRequest {
  string id = 1;
}

message GetUserResponse {
  User user = 1;
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
}

message CreateUserResponse {
  User user = 1;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
}

message ListUsersResponse {
  repeated User users = 1;
  string next_page_token = 2;
}

message User {
  string id = 1;
  string name = 2;
  string email = 3;
  google.protobuf.Timestamp created_at = 4;
}
```

## Streaming Patterns

### Server Streaming

Server sends multiple responses to single client request:

```protobuf
service LogService {
  // Server streams log entries
  rpc StreamLogs(StreamLogsRequest) returns (stream LogEntry);
}

message StreamLogsRequest {
  string service_name = 1;
  google.protobuf.Timestamp start_time = 2;
}

message LogEntry {
  google.protobuf.Timestamp timestamp = 1;
  string level = 2;
  string message = 3;
}
```

### Client Streaming

Client sends multiple requests, server responds once:

```protobuf
service UploadService {
  // Client streams file chunks
  rpc UploadFile(stream FileChunk) returns (UploadResponse);
}

message FileChunk {
  bytes data = 1;
}

message UploadResponse {
  string file_id = 1;
  int64 size = 2;
}
```

### Bidirectional Streaming

Both client and server stream messages:

```protobuf
service ChatService {
  // Bidirectional chat
  rpc Chat(stream ChatMessage) returns (stream ChatMessage);
}

message ChatMessage {
  string user_id = 1;
  string message = 2;
  google.protobuf.Timestamp timestamp = 3;
}
```

## Rust: Tonic

### Installation

```toml
# Cargo.toml
[dependencies]
tonic = "0.11"
prost = "0.12"
tokio = { version = "1", features = ["full"] }

[build-dependencies]
tonic-build = "0.11"
```

### Build Script

```rust
// build.rs
fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_build::compile_protos("proto/user.proto")?;
    Ok(())
}
```

### Server Implementation

```rust
use tonic::{transport::Server, Request, Response, Status};

pub mod user {
    tonic::include_proto!("user.v1");
}

use user::user_service_server::{UserService, UserServiceServer};
use user::{GetUserRequest, GetUserResponse, User};

#[derive(Default)]
pub struct MyUserService {}

#[tonic::async_trait]
impl UserService for MyUserService {
    async fn get_user(
        &self,
        request: Request<GetUserRequest>
    ) -> Result<Response<GetUserResponse>, Status> {
        let req = request.into_inner();

        let user = match get_user_from_db(&req.id).await {
            Some(u) => u,
            None => return Err(Status::not_found("User not found"))
        };

        Ok(Response::new(GetUserResponse {
            user: Some(user)
        }))
    }

    async fn list_users(
        &self,
        request: Request<ListUsersRequest>
    ) -> Result<Response<ListUsersResponse>, Status> {
        let req = request.into_inner();
        let users = get_users_from_db(req.page_size, &req.page_token).await;

        Ok(Response::new(ListUsersResponse {
            users,
            next_page_token: "next_token".to_string()
        }))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "0.0.0.0:50051".parse()?;
    let user_service = MyUserService::default();

    Server::builder()
        .add_service(UserServiceServer::new(user_service))
        .serve(addr)
        .await?;

    Ok(())
}
```

### Server Streaming

```rust
use tokio_stream::wrappers::ReceiverStream;
use tokio::sync::mpsc;

impl LogService for MyLogService {
    type StreamLogsStream = ReceiverStream<Result<LogEntry, Status>>;

    async fn stream_logs(
        &self,
        request: Request<StreamLogsRequest>
    ) -> Result<Response<Self::StreamLogsStream>, Status> {
        let (tx, rx) = mpsc::channel(128);

        tokio::spawn(async move {
            for i in 0..10 {
                let log = LogEntry {
                    timestamp: Some(prost_types::Timestamp::from(SystemTime::now())),
                    level: "INFO".to_string(),
                    message: format!("Log entry {}", i)
                };

                tx.send(Ok(log)).await.unwrap();
                tokio::time::sleep(Duration::from_secs(1)).await;
            }
        });

        Ok(Response::new(ReceiverStream::new(rx)))
    }
}
```

### Client Implementation

```rust
use user::user_service_client::UserServiceClient;
use user::GetUserRequest;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut client = UserServiceClient::connect("http://[::1]:50051").await?;

    let request = tonic::Request::new(GetUserRequest {
        id: "123".to_string()
    });

    let response = client.get_user(request).await?;

    println!("User: {:?}", response.into_inner().user);

    Ok(())
}
```

## Go: Connect-Go

Connect-Go provides gRPC-compatible APIs that work in browsers.

### Installation

```bash
go install connectrpc.com/connect/cmd/protoc-gen-connect-go@latest
```

### Code Generation

```bash
protoc --go_out=. --go_opt=paths=source_relative \
       --connect-go_out=. --connect-go_opt=paths=source_relative \
       user/v1/user.proto
```

### Server Implementation

```go
package main

import (
    "context"
    "net/http"

    "connectrpc.com/connect"
    userv1 "example.com/user/v1"
    "example.com/user/v1/userv1connect"
)

type UserServiceHandler struct{}

func (s *UserServiceHandler) GetUser(
    ctx context.Context,
    req *connect.Request[userv1.GetUserRequest],
) (*connect.Response[userv1.GetUserResponse], error) {
    user, err := getUserFromDB(req.Msg.Id)
    if err != nil {
        return nil, connect.NewError(connect.CodeNotFound, err)
    }

    return connect.NewResponse(&userv1.GetUserResponse{
        User: user,
    }), nil
}

func main() {
    handler := &UserServiceHandler{}
    path, handlerFunc := userv1connect.NewUserServiceHandler(handler)

    http.Handle(path, handlerFunc)
    http.ListenAndServe(":8080", nil)
}
```

### Client (Browser-Compatible)

```typescript
import { createPromiseClient } from '@connectrpc/connect'
import { createConnectTransport } from '@connectrpc/connect-web'
import { UserService } from './gen/user/v1/user_connect'

const transport = createConnectTransport({
  baseUrl: 'http://localhost:8080'
})

const client = createPromiseClient(UserService, transport)

async function getUser(id: string) {
  const response = await client.getUser({ id })
  console.log(response.user)
}
```

## Python: grpcio

### Installation

```bash
pip install grpcio grpcio-tools
```

### Code Generation

```bash
python -m grpc_tools.protoc \
    -I./proto \
    --python_out=. \
    --grpc_python_out=. \
    proto/user.proto
```

### Server Implementation

```python
import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc

class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        user = get_user_from_db(request.id)

        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return user_pb2.GetUserResponse()

        return user_pb2.GetUserResponse(user=user)

    def ListUsers(self, request, context):
        users = get_users_from_db(
            page_size=request.page_size,
            page_token=request.page_token
        )

        return user_pb2.ListUsersResponse(
            users=users,
            next_page_token="next_token"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

### Client Implementation

```python
import grpc
import user_pb2
import user_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)

        response = stub.GetUser(user_pb2.GetUserRequest(id='123'))
        print(f"User: {response.user}")

if __name__ == '__main__':
    run()
```

## Error Handling

### gRPC Status Codes

| Code | HTTP | Meaning | When to Use |
|------|------|---------|-------------|
| OK | 200 | Success | Successful operation |
| CANCELLED | 499 | Cancelled | Client cancelled |
| UNKNOWN | 500 | Unknown error | Unknown server error |
| INVALID_ARGUMENT | 400 | Invalid argument | Validation failed |
| DEADLINE_EXCEEDED | 504 | Timeout | Operation timeout |
| NOT_FOUND | 404 | Not found | Resource not found |
| ALREADY_EXISTS | 409 | Already exists | Duplicate resource |
| PERMISSION_DENIED | 403 | Permission denied | Authorization failed |
| UNAUTHENTICATED | 401 | Unauthenticated | Authentication required |
| RESOURCE_EXHAUSTED | 429 | Rate limited | Quota exceeded |
| FAILED_PRECONDITION | 400 | Precondition failed | Operation can't be performed |
| ABORTED | 409 | Aborted | Concurrent modification |
| OUT_OF_RANGE | 400 | Out of range | Invalid range |
| UNIMPLEMENTED | 501 | Not implemented | Method not implemented |
| INTERNAL | 500 | Internal error | Internal server error |
| UNAVAILABLE | 503 | Unavailable | Service unavailable |
| DATA_LOSS | 500 | Data loss | Unrecoverable data loss |

### Rust Error Handling

```rust
use tonic::{Status, Code};

impl UserService for MyUserService {
    async fn get_user(
        &self,
        request: Request<GetUserRequest>
    ) -> Result<Response<GetUserResponse>, Status> {
        let user = get_user_from_db(&request.into_inner().id)
            .await
            .map_err(|e| Status::new(Code::NotFound, format!("User not found: {}", e)))?;

        Ok(Response::new(GetUserResponse { user: Some(user) }))
    }
}
```

## Best Practices

1. **Use proto3 syntax** - Latest version with better defaults
2. **Version your services** - Use package names like `user.v1`, `user.v2`
3. **Reserve field numbers** - When removing fields, mark as `reserved`
4. **Use streaming for large data** - Don't send large responses in single message
5. **Implement health checks** - Use gRPC health checking protocol
6. **Enable reflection** - For debugging with tools like grpcurl
7. **Use interceptors** - For logging, auth, metrics
8. **Handle backpressure** - Limit concurrent requests
9. **Set timeouts** - Prevent hanging connections
10. **Document your services** - Comments in proto files

## Performance Tips

**Use HTTP/2 multiplexing:**
- Single connection for multiple RPCs
- Reduces connection overhead

**Enable compression:**
```rust
Server::builder()
    .add_service(
        UserServiceServer::new(service)
            .send_compressed(CompressionEncoding::Gzip)
            .accept_compressed(CompressionEncoding::Gzip)
    )
```

**Connection pooling:**
- Reuse gRPC channels
- Don't create new channel per request

**Batch requests when possible:**
- Use repeated fields for batch operations
- Reduces network round trips
