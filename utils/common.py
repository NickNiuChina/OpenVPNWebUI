
def make_dirs(name, mode=0o755, exist_ok=False):
    """ 默认权限设置为 0o755 """
    return os.makedirs(name, mode=mode, exist_ok=exist_ok)