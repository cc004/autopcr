import argparse
import importlib
import os


def main():
    parser = argparse.ArgumentParser(
        description="Start AutoPCR as a standalone HTTP server"
    )
    parser.add_argument("--openbao-addr")
    parser.add_argument(
        "--openbao-enabled",
        action="store_true",
        help="Use OpenBao instead of the default local JSON credential/session files",
    )
    parser.add_argument(
        "--openbao-auth-method",
        choices=("token", "approle", "kubernetes"),
    )
    parser.add_argument("--openbao-token-file")
    parser.add_argument("--openbao-role-id")
    parser.add_argument("--openbao-role-id-file")
    parser.add_argument("--openbao-secret-id-file")
    parser.add_argument("--openbao-approle-mount")
    # parser.add_argument("--openbao-k8s-role")
    # parser.add_argument("--openbao-k8s-mount")
    # parser.add_argument("--openbao-k8s-jwt-file")
    args = parser.parse_args()

    os.environ["AUTOPCR_HOSHINO_PLUGIN_MODE"] = "false"
    if args.openbao_enabled:
        os.environ["AUTOPCR_OPENBAO_ENABLED"] = "true"
    if args.openbao_addr is not None:
        os.environ["AUTOPCR_OPENBAO_ADDR"] = args.openbao_addr
    if args.openbao_auth_method is not None:
        os.environ["AUTOPCR_OPENBAO_AUTH_METHOD"] = args.openbao_auth_method
    if args.openbao_token_file is not None:
        os.environ["AUTOPCR_OPENBAO_TOKEN_FILE"] = args.openbao_token_file
    if args.openbao_role_id is not None:
        os.environ["AUTOPCR_OPENBAO_ROLE_ID"] = args.openbao_role_id
    if args.openbao_role_id_file is not None:
        os.environ["AUTOPCR_OPENBAO_ROLE_ID_FILE"] = args.openbao_role_id_file
    if args.openbao_secret_id_file is not None:
        os.environ["AUTOPCR_OPENBAO_SECRET_ID_FILE"] = args.openbao_secret_id_file
    if args.openbao_approle_mount is not None:
        os.environ["AUTOPCR_OPENBAO_APPROLE_MOUNT"] = args.openbao_approle_mount
    # if args.openbao_k8s_role is not None:
    #     os.environ["AUTOPCR_OPENBAO_K8S_ROLE"] = args.openbao_k8s_role
    # if args.openbao_k8s_mount is not None:
    #     os.environ["AUTOPCR_OPENBAO_K8S_MOUNT"] = args.openbao_k8s_mount
    # if args.openbao_k8s_jwt_file is not None:
    #     os.environ["AUTOPCR_OPENBAO_K8S_JWT_FILE"] = args.openbao_k8s_jwt_file

    importlib.import_module("autopcr.http_server.httpserver_standalone")


if __name__ == "__main__":
    main()