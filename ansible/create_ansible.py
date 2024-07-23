import argparse

def main(args):
    script = """---
- name: Setup tools
  ansible.builtin.import_playbook: setup-tools.yaml

- name: Setup k3s
  ansible.builtin.import_playbook: setup-k3s.yaml
"""

    if args.enable_mimir:
        script += """
- name: Setup mimir
  ansible.builtin.import_playbook: setup-mimir.yaml
"""

    if args.enable_grafana_dashboard:
        script += """
- name: Setup Grafana Dashboard
  ansible.builtin.import_playbook: setup-grafana-dashboard.yaml
"""

    if args.enable_grafana_agent:
        script += """
- name: Setup Grafana Agent
  ansible.builtin.import_playbook: setup-grafana-agent.yaml
"""

    if args.enable_nvidia_runtime:
        script += """
- name: Setup nvidia runtime
  ansible.builtin.import_playbook: setup-nvidia-runtime.yaml
"""

    with open("ansible.yaml", "w") as file:
        file.write(script)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--enable-mimir",
                        action="store_true",
                        help="Enables mimir storage")
    parser.add_argument("--enable-grafana-dashboard",
                        action="store_true",
                        help="Enables grafana dashboard")
    parser.add_argument("--enable-grafana-agent",
                        action="store_true",
                        help="Enables grafana agent")
    parser.add_argument("--enable-nvidia-runtime",
                        action="store_true",
                        help="Enables nvidia runtime")
    main(parser.parse_args())