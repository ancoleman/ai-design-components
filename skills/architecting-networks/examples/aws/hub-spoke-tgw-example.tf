/**
 * Hub-and-Spoke (Transit Gateway) Architecture Example - AWS
 *
 * Demonstrates: Transit Gateway connecting multiple VPCs
 *
 * Use Case: 5+ VPCs need communication, centralized security, hybrid connectivity
 *
 * Prerequisites:
 * - Terraform >= 1.0
 * - AWS provider configured
 *
 * Usage:
 * terraform init
 * terraform plan
 * terraform apply
 */

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# Transit Gateway (Hub)
resource "aws_ec2_transit_gateway" "main" {
  description                     = "Main Transit Gateway for hub-spoke"
  amazon_side_asn                 = 64512
  default_route_table_association = "disable"  # Use custom route tables
  default_route_table_propagation = "disable"
  dns_support                     = "enable"
  vpn_ecmp_support               = "enable"

  tags = {
    Name    = "main-tgw"
    Pattern = "hub-spoke"
  }
}

# Production VPC (Spoke)
module "vpc_prod" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "prod-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]

  enable_nat_gateway   = true
  one_nat_gateway_per_az = true
  enable_dns_hostnames = true

  tags = {
    Environment = "production"
    Role        = "spoke"
  }
}

# Development VPC (Spoke)
module "vpc_dev" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "dev-vpc"
  cidr = "10.1.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.1.1.0/24", "10.1.2.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = true  # Cost optimization for dev
  enable_dns_hostnames = true

  tags = {
    Environment = "development"
    Role        = "spoke"
  }
}

# Shared Services VPC (Spoke)
module "vpc_shared" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "shared-services-vpc"
  cidr = "10.2.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.2.1.0/24", "10.2.2.0/24", "10.2.3.0/24"]

  enable_nat_gateway   = true
  one_nat_gateway_per_az = true
  enable_dns_hostnames = true

  tags = {
    Environment = "shared"
    Role        = "spoke"
  }
}

# TGW Attachment: Production VPC
resource "aws_ec2_transit_gateway_vpc_attachment" "prod" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id
  vpc_id             = module.vpc_prod.vpc_id
  subnet_ids         = module.vpc_prod.private_subnets

  dns_support                                     = "enable"
  transit_gateway_default_route_table_association = false
  transit_gateway_default_route_table_propagation = false

  tags = {
    Name = "prod-tgw-attachment"
  }
}

# TGW Attachment: Development VPC
resource "aws_ec2_transit_gateway_vpc_attachment" "dev" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id
  vpc_id             = module.vpc_dev.vpc_id
  subnet_ids         = module.vpc_dev.private_subnets

  dns_support                                     = "enable"
  transit_gateway_default_route_table_association = false
  transit_gateway_default_route_table_propagation = false

  tags = {
    Name = "dev-tgw-attachment"
  }
}

# TGW Attachment: Shared Services VPC
resource "aws_ec2_transit_gateway_vpc_attachment" "shared" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id
  vpc_id             = module.vpc_shared.vpc_id
  subnet_ids         = module.vpc_shared.private_subnets

  dns_support                                     = "enable"
  transit_gateway_default_route_table_association = false
  transit_gateway_default_route_table_propagation = false

  tags = {
    Name = "shared-tgw-attachment"
  }
}

# TGW Route Table: Production
resource "aws_ec2_transit_gateway_route_table" "prod" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id

  tags = {
    Name = "prod-tgw-rt"
  }
}

# TGW Route Table: Development
resource "aws_ec2_transit_gateway_route_table" "dev" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id

  tags = {
    Name = "dev-tgw-rt"
  }
}

# TGW Route Table: Shared Services
resource "aws_ec2_transit_gateway_route_table" "shared" {
  transit_gateway_id = aws_ec2_transit_gateway.main.id

  tags = {
    Name = "shared-tgw-rt"
  }
}

# Associate Production VPC with its route table
resource "aws_ec2_transit_gateway_route_table_association" "prod" {
  transit_gateway_attachment_id  = aws_ec2_transit_gateway_vpc_attachment.prod.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.prod.id
}

# Associate Development VPC with its route table
resource "aws_ec2_transit_gateway_route_table_association" "dev" {
  transit_gateway_attachment_id  = aws_ec2_transit_gateway_vpc_attachment.dev.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.dev.id
}

# Associate Shared Services VPC with its route table
resource "aws_ec2_transit_gateway_route_table_association" "shared" {
  transit_gateway_attachment_id  = aws_ec2_transit_gateway_vpc_attachment.shared.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.shared.id
}

# Route: Production can reach Shared Services
resource "aws_ec2_transit_gateway_route" "prod_to_shared" {
  destination_cidr_block         = module.vpc_shared.vpc_cidr_block
  transit_gateway_attachment_id  = aws_ec2_transit_gateway_vpc_attachment.shared.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.prod.id
}

# Route: Development can reach Shared Services
resource "aws_ec2_transit_gateway_route" "dev_to_shared" {
  destination_cidr_block         = module.vpc_shared.vpc_cidr_block
  transit_gateway_attachment_id  = aws_ec2_transit_gateway_vpc_attachment.shared.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.dev.id
}

# Route: Shared Services can reach Production
resource "aws_ec2_transit_gateway_route" "shared_to_prod" {
  destination_cidr_block         = module.vpc_prod.vpc_cidr_block
  transit_gateway_attachment_id  = aws_ec2_transit_gateway_vpc_attachment.prod.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.shared.id
}

# Route: Shared Services can reach Development
resource "aws_ec2_transit_gateway_route" "shared_to_dev" {
  destination_cidr_block         = module.vpc_dev.vpc_cidr_block
  transit_gateway_attachment_id  = aws_ec2_transit_gateway_vpc_attachment.dev.id
  transit_gateway_route_table_id = aws_ec2_transit_gateway_route_table.shared.id
}

# VPC Routes: Production private subnets to TGW
resource "aws_route" "prod_private_to_tgw" {
  count = length(module.vpc_prod.private_route_table_ids)

  route_table_id         = module.vpc_prod.private_route_table_ids[count.index]
  destination_cidr_block = "10.0.0.0/8"  # All RFC1918 10.x traffic to TGW
  transit_gateway_id     = aws_ec2_transit_gateway.main.id
}

# VPC Routes: Development private subnets to TGW
resource "aws_route" "dev_private_to_tgw" {
  count = length(module.vpc_dev.private_route_table_ids)

  route_table_id         = module.vpc_dev.private_route_table_ids[count.index]
  destination_cidr_block = "10.0.0.0/8"
  transit_gateway_id     = aws_ec2_transit_gateway.main.id
}

# VPC Routes: Shared Services private subnets to TGW
resource "aws_route" "shared_private_to_tgw" {
  count = length(module.vpc_shared.private_route_table_ids)

  route_table_id         = module.vpc_shared.private_route_table_ids[count.index]
  destination_cidr_block = "10.0.0.0/8"
  transit_gateway_id     = aws_ec2_transit_gateway.main.id
}

# Outputs
output "transit_gateway_id" {
  description = "Transit Gateway ID"
  value       = aws_ec2_transit_gateway.main.id
}

output "prod_vpc_id" {
  description = "Production VPC ID"
  value       = module.vpc_prod.vpc_id
}

output "dev_vpc_id" {
  description = "Development VPC ID"
  value       = module.vpc_dev.vpc_id
}

output "shared_vpc_id" {
  description = "Shared Services VPC ID"
  value       = module.vpc_shared.vpc_id
}

output "routing_summary" {
  description = "Routing summary"
  value = {
    prod_to_shared    = "10.0.0.0/16 → TGW → 10.2.0.0/16"
    dev_to_shared     = "10.1.0.0/16 → TGW → 10.2.0.0/16"
    shared_to_prod    = "10.2.0.0/16 → TGW → 10.0.0.0/16"
    shared_to_dev     = "10.2.0.0/16 → TGW → 10.1.0.0/16"
    prod_to_dev_blocked = "No direct route (security isolation)"
  }
}
