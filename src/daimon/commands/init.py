from daimon.utils.logging_utils import setup_logger
from pathlib import Path
import shutil
import daimon
logger = setup_logger()

def copy_dir(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, dirs_exist_ok=True)

def ensure_global_schema():
    # check for global schema, if not found, then copy from package
    global_schema_path = Path.home() / ".daimon" / "schema"
    if not global_schema_path.exists():
        logger.info(f'global schema not found at {global_schema_path}, copying from package...')
        source = Path(daimon.__file__).resolve().parents[0] / "schema"
        destination = global_schema_path.parents[0]
        copy_dir(source, destination)
    else:
        logger.info(f'global schema found at {global_schema_path}')


def init_command():
    logger.info("Initializing daimon project...")
    ensure_global_schema()
    adding_global_schema_to_project = input("Do you want to add global schema to your project? (y/n): ")
    if adding_global_schema_to_project.lower() == "y":
        breakpoint()
    else:
        raise Exception("Global schema is required for daimon to work")
    # copy global schema to project .schema
    # generate daimon.yaml
    # generate .env template, if its already there, then add to it
if __name__ == "__main__":
    init_command()