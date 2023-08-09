data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_vpc" "mlflow_vpc" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_hostnames = true
  tags = {
    Name = "mlflow_vpc"
  }
}

resource "aws_internet_gateway" "mlflow_igw" {
  vpc_id = aws_vpc.mlflow_vpc.id
  tags = {
    Name = "mlflow_igw"
  }
}

resource "aws_subnet" "mlflow_public_subnet" {
  vpc_id            = aws_vpc.mlflow_vpc.id
  cidr_block        = var.public_subnets_cidr_blocks
  availability_zone = data.aws_availability_zones.available.names[0]
  tags = {
    Name = "mlflow_public_subnet"
  }
}

resource "aws_subnet" "mlflow_private_subnet" {
  count             = var.subnet_count.private
  vpc_id            = aws_vpc.mlflow_vpc.id
  cidr_block        = var.private_subnets_cidr_blocks[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]
  tags = {
    Name = "mlflow_private_subnet_${count.index}"
  }
}

resource "aws_route_table" "mlflow_public_route_table" {
  vpc_id = aws_vpc.mlflow_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.mlflow_igw.id
  }
  route {
    ipv6_cidr_block = "::/0"
    gateway_id      = aws_internet_gateway.mlflow_igw.id
  }
  tags = {
    Name = "mlflow_public_route_table"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.mlflow_public_subnet.id
  route_table_id = aws_route_table.mlflow_public_route_table.id
}

resource "aws_route_table" "mlflow_private_route_table" {
  vpc_id = aws_vpc.mlflow_vpc.id
}

resource "aws_route_table_association" "private" {
  count          = var.subnet_count.private
  subnet_id      = aws_subnet.mlflow_private_subnet[count.index].id
  route_table_id = aws_route_table.mlflow_private_route_table.id
}

resource "aws_security_group" "mlflow_sg" {
  name        = "mlflow_sg"
  description = "Security group for mlflow"
  vpc_id      = aws_vpc.mlflow_vpc.id
  ingress {
    description = "Allow all inbound traffic"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "Allow SSH inbound traffic"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "mlflow_sg"
  }
}

resource "aws_security_group" "db_sg" {
  name        = "db_sg"
  description = "Security group for database"
  vpc_id      = aws_vpc.mlflow_vpc.id

  ingress {
    description     = "Allow all inbound traffic from mlflow_sg"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.mlflow_sg.id]
  }

  tags = {
    Name = "db_sg"
  }
}

resource "aws_db_subnet_group" "mlflow_db_subnet_group" {
  name       = "mlflow_db_subnet_group"
  subnet_ids = [for subnet in aws_subnet.mlflow_private_subnet : subnet.id]
}

resource "aws_db_instance" "mlflow_db" {
  db_name                = var.settings.database.db_name
  engine                 = var.settings.database.engine
  engine_version         = var.settings.database.engine_version
  instance_class         = var.settings.database.instance_class
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.mlflow_db_subnet_group.name
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  allocated_storage      = var.settings.database.allocated_storage
  skip_final_snapshot    = var.settings.database.skip_final_snapshot
}

resource "aws_s3_bucket" "artifect_bucket" {
  bucket        = var.settings.artifact_bucket.name
  force_destroy = true
  tags = {
    Name = "artifect_bucket"
  }
}

resource "aws_eip" "mlflow_eip" {
  instance = aws_instance.mlflow_server.id
  tags = {
    Name = "mlflow_eip"
  }
}

resource "aws_instance" "mlflow_server" {
  ami                    = var.settings.mlflow_server.ami
  instance_type          = var.settings.mlflow_server.instance_type
  subnet_id              = aws_subnet.mlflow_public_subnet.id
  vpc_security_group_ids = [aws_security_group.mlflow_sg.id]
  key_name               = "mlflow"
  user_data              = <<-EOF
        #!/bin/bash
        sudo yum update
        sudo yum install pip -y
        EOF
  tags = {
    Name = "mlflow_server"
  }
}
