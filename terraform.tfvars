variable "admin_username" {
  description = "The username of the admin account"
}

variable "admin_password" {
  description = "The password of the admin account"
  sensitive   = true
}

#...

os_profile {
  computer_name  = "hostname"
  admin_username = var.admin_username
  admin_password = var.admin_password
}
