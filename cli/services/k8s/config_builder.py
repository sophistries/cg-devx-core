import pkg_resources
import yaml

from cli.common.const.common_path import LOCAL_FOLDER


def create_k8s_config(command: str, command_args: [], cloud_provider_auth_env_vars: dict, kubeconfig_params: dict,
                      kubeconfig_name: str = "kubeconfig.yaml") -> str:
    kubeconfig_path = LOCAL_FOLDER / kubeconfig_name
    template_file_path = pkg_resources.resource_filename('cli.services.k8s', "kubeconfig.yaml")

    with open(template_file_path, "r") as file:
        kubeconf = yaml.safe_load(file.read())
        kubeconf["users"][0]["user"]["exec"]["command"] = command
        kubeconf["users"][0]["user"]["exec"]["args"] = command_args
        envs = []
        for k, v in cloud_provider_auth_env_vars.items():
            envs.append({"name": k, "value": v})
        kubeconf["users"][0]["user"]["exec"]["env"] = envs
        data = yaml.dump(kubeconf)
        for k, v in kubeconfig_params.items():
            data = data.replace(k, v)

    with open(kubeconfig_path, "w") as file:
        file.write(data)

    return str(kubeconfig_path)
