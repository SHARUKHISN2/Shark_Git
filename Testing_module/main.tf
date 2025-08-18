module "test_module" {
  source = "./modules/single-ec2"
  
  env = "{{ env }}"
  ami = "{{ ami }}"
}
