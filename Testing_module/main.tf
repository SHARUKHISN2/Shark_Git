module "test_module" {
  source = "./modules/single-ec2"
  
  env = ${{ values.env }}
  ami = ${{ values.ami }}
}
