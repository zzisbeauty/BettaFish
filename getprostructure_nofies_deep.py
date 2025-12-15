import os


def print_project_structure_dirs_only(
    root_path: str,
    ignore_dirs=None,
    ignore_paths=None
):
    """
    只打印项目目录结构（不输出文件）
    - 根目录视为第 1 级
    - 最多输出到第 N 级目录
    """

    MAX_DEPTH = 5

    if ignore_dirs is None:
        ignore_dirs = []

    if ignore_paths is None:
        ignore_paths = []

    root_path = os.path.abspath(root_path)
    ignore_paths = {os.path.abspath(p) for p in ignore_paths}

    root_name = os.path.basename(root_path.rstrip(os.sep))
    print(root_name)

    def _walk(current_path, prefix="", depth=1):
        # 深度超出限制，不再继续
        if depth >= MAX_DEPTH:
            return

        # 命中忽略的绝对路径，直接跳过
        if current_path in ignore_paths:
            return

        try:
            entries = sorted(os.listdir(current_path))
        except PermissionError:
            return

        # 只收集目录
        dirs = []
        for e in entries:
            full_path = os.path.join(current_path, e)

            if not os.path.isdir(full_path):
                continue
            if e in ignore_dirs:
                continue
            if full_path in ignore_paths:
                continue

            dirs.append(e)

        total = len(dirs)

        for index, d in enumerate(dirs):
            full_path = os.path.join(current_path, d)
            is_last = index == total - 1

            print(prefix + "|-- " + d)

            next_prefix = "    " if is_last else "|   "
            _walk(
                full_path,
                prefix + next_prefix,
                depth + 1
            )

    _walk(root_path)

ignore = [
    ".github",
    ".git",
    ".vscode",
    "__pycache__",
    "idea",
    ".devcontainer"
    # "docs",
    # "examples",
]

print_project_structure_dirs_only(
    root_path="/app/langchain",
    ignore_dirs=ignore,
    ignore_paths = [ # 忽略项目下的指定路径
        "/app/langchain/libs/langchain", # 老版本，直接忽略
        "/app/langchain/libs/core/.venv",
        "/app/langchain/libs/langchain_v1/llms",
        "/app/langchain/libs/langchain_v1/.venv",
        "/app/langchain/libs/langchain_v1/bettafishwithlangchain",
        "/app/langchain/libs/langchain_v1/bettafishwithlangchain-del",
    ]
)
