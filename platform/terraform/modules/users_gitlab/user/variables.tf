variable "username" {
  type        = string
  description = "a distinct username that is unique to this user throughout the platform"
}

variable "user_disabled" {
  type    = bool
  default = false
}

variable "userpass_accessor" {
  type = string
}

variable "gitlab_username" {
  type = string
}

variable "email" {
  type = string
}

variable "first_name" {
  type = string
}

variable "last_name" {
  type = string
}

variable "gitlab_team_slugs" {
  type        = list(string)
  description = "the gitlab team slugs to place the user"
  default     = []
}

variable "acl_policies" {
  type = list(string)
}

variable "oidc_groups_for_user" {
  type = list(string)
}

variable "vcs_owner" {
  type    = string
}
