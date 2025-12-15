import os


def print_project_structure_ascii(
    root_path: str,
    ignore_dirs=None,
    ignore_paths=None
):
    """
    打印项目目录结构（ASCII 树）
    
    ignore_dirs:
        - 按目录名忽略（任意层级）
        - 示例：["venv", ".git"]

    ignore_paths:
        - 按绝对路径忽略整个目录
        - 示例：["/project/src/generated"]
    """

    if ignore_dirs is None:
        ignore_dirs = []

    if ignore_paths is None:
        ignore_paths = []

    root_path = os.path.abspath(root_path)
    ignore_paths = {os.path.abspath(p) for p in ignore_paths}

    root_name = os.path.basename(root_path.rstrip(os.sep))
    print(root_name)

    def _walk(current_path, prefix=""):
        # 如果当前目录在忽略路径中，直接跳过
        if current_path in ignore_paths:
            return

        try:
            entries = sorted(os.listdir(current_path))
        except PermissionError:
            return

        # 过滤掉按名字忽略的目录
        entries = [
            e for e in entries
            if e not in ignore_dirs
        ]

        total = len(entries)

        for index, entry in enumerate(entries):
            full_path = os.path.join(current_path, entry)
            is_last = index == total - 1

            # 如果是忽略的绝对路径，直接跳过
            if full_path in ignore_paths:
                continue

            print(prefix + "|-- " + entry)

            if os.path.isdir(full_path):
                next_prefix = "    " if is_last else "|   "
                _walk(full_path, prefix + next_prefix)

    _walk(root_path)

project_path = "/app/langchain"
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


print_project_structure_ascii(
    root_path=project_path, 
    ignore_dirs=ignore,
    ignore_paths = [ # 忽略项目下的指定路径
        "/app/langchain/libs/langchain_v1/.venv",
        "/app/langchain/libs/langchain_v1/bettafishwithlangchain",
        "/app/langchain/libs/langchain_v1/bettafishwithlangchain-del",
    ]
)