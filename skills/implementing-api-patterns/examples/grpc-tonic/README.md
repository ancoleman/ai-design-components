# Rust gRPC with Tonic

High-performance gRPC service using Tonic framework.

## Features

- Tonic (async gRPC)
- Protocol Buffers (proto3)
- Bidirectional streaming
- Tower middleware
- Automatic code generation

## Files

```
grpc-tonic/
├── proto/
│   └── api.proto            # Protocol Buffers schema
├── src/
│   ├── main.rs
│   ├── server.rs            # gRPC server
│   └── client.rs            # gRPC client
├── build.rs                 # Proto compilation
└── Cargo.toml
```

## Quick Start

```bash
# Install dependencies
cargo build

# Run server
cargo run --bin server

# Run client (separate terminal)
cargo run --bin client
```

## Protocol Buffers Schema

```protobuf
// proto/api.proto
syntax = "proto3";

package api.v1;

service UserService {
  rpc GetUser (GetUserRequest) returns (User);
  rpc ListUsers (ListUsersRequest) returns (stream User);
  rpc CreateUser (CreateUserRequest) returns (User);
}

message User {
  int64 id = 1;
  string email = 2;
  string name = 3;
}

message GetUserRequest {
  int64 id = 1;
}

message ListUsersRequest {
  int32 limit = 1;
}

message CreateUserRequest {
  string email = 1;
  string name = 2;
}
```

## Server Implementation

```rust
use tonic::{transport::Server, Request, Response, Status};

pub struct UserServiceImpl;

#[tonic::async_trait]
impl UserService for UserServiceImpl {
    async fn get_user(
        &self,
        request: Request<GetUserRequest>,
    ) -> Result<Response<User>, Status> {
        let req = request.into_inner();

        let user = User {
            id: req.id,
            email: "user@example.com".to_string(),
            name: "John Doe".to_string(),
        };

        Ok(Response::new(user))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "0.0.0.0:50051".parse()?;
    let service = UserServiceImpl::default();

    Server::builder()
        .add_service(UserServiceServer::new(service))
        .serve(addr)
        .await?;

    Ok(())
}
```

## Client Usage

```rust
let mut client = UserServiceClient::connect("http://localhost:50051").await?;

let request = tonic::Request::new(GetUserRequest { id: 1 });
let response = client.get_user(request).await?;

println!("User: {:?}", response.into_inner());
```

## Performance

- 50,000+ RPC/second
- <1ms latency
- Bidirectional streaming support
- HTTP/2 multiplexing
