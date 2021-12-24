resource "google_cloudbuild_trigger" "mc-chimera-pr" {
  name        = "mc-chimera-pr"
  description = "MC Chimera: pr"

  github {
    owner = "masaki925"
    name  = "mc_chimera"

    pull_request {
      branch = "^main$"
    }
  }

  filename = "cloudbuild.yaml"

  substitutions = {
    _ENV = "pr-"
  }
}

resource "google_cloudbuild_trigger" "mc-chimera-dev" {
  name        = "mc-chimera-dev"
  description = "MC Chimera: dev"

  github {
    owner = "masaki925"
    name  = "mc_chimera"

    push {
      branch = "^main$"
    }
  }

  filename = "cloudbuild.yaml"

  substitutions = {
    _ENV = "dev"
  }
}

