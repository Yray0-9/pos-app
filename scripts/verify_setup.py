"""Verify local Python environment, dependencies, and Django configuration."""

import importlib
import subprocess
import sys
from pathlib import Path


REQUIRED_PACKAGES = [
    "django",
    "dotenv",
    "sqlparse",
    "asgiref",
    "tzdata",
]


def check_python_version() -> bool:
    print(f"[*] Python version: {sys.version.split()[0]} ({sys.executable})")
    if sys.version_info < (3, 10):
        print("[-] Python 3.10+ is required.")
        return False
    print("[+] Python version is compatible.")
    return True


def check_packages() -> bool:
    print("[*] Checking required dependencies...")
    all_installed = True
    for pkg in REQUIRED_PACKAGES:
        try:
            importlib.import_module(pkg)
            print(f"  [+] {pkg}: installed")
        except ImportError:
            print(f"  [-] {pkg}: NOT installed (run: pip install -r requirements.txt)")
            all_installed = False
    return all_installed


def check_env_file(project_root: Path) -> bool:
    env_file = project_root / ".env"
    print(f"[*] Checking .env file at {env_file}...")
    if not env_file.exists():
        print("  [-] .env file missing. Run: python scripts/init_env.py")
        return False
    print("  [+] .env file exists.")
    return True


def run_django_check(project_root: Path) -> bool:
    manage_py = project_root / "manage.py"
    print("[*] Running Django system checks (manage.py check)...")
    try:
        result = subprocess.run(
            [sys.executable, str(manage_py), "check"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print("  [+] Django system checks passed with 0 issues.")
            return True
        else:
            print(f"  [-] Django system checks failed:\n{result.stderr}")
            return False
    except Exception as exc:
        print(f"  [-] Failed to execute manage.py: {exc}")
        return False


def main():
    project_root = Path(__file__).resolve().parent.parent
    print("=" * 60)
    print("Common Table POS - Environment and Setup Verification")
    print("=" * 60)

    ok_version = check_python_version()
    ok_pkgs = check_packages()
    ok_env = check_env_file(project_root)
    ok_django = False

    if ok_pkgs and ok_env:
        ok_django = run_django_check(project_root)

    print("=" * 60)
    if ok_version and ok_pkgs and ok_env and ok_django:
        print("[SUCCESS] All environment and setup checks passed!")
        sys.exit(0)
    else:
        print("[FAILED] Some checks failed. Please review the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
