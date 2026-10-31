ui = false
disable_mlock = true
api_addr = "http://openbao:8200"
cluster_addr = "http://openbao:8201"

storage "raft" {
  path = "/openbao/file"
  node_id = "autopcr-openbao-1"
}

listener "tcp" {
  address         = "0.0.0.0:8200"
  cluster_address = "0.0.0.0:8201"
  tls_disable     = true
}

audit "file" "audit-log" {
  description = "File audit device for the docker-compose deployment"
  options = {
    file_path = "/openbao/audit/audit.log"
  }
}