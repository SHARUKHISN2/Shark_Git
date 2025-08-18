module "test_module" {
  source = "./modules/single-ec2"
  
  env = 'dev'
  ami = 'ami-test123'
}
