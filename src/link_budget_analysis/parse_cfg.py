from pathlib import Path
from dataclasses import dataclass

from yaml import safe_load


def load_link_config_file(filename: str) -> dict:
    '''
    Loads link analysis configuration file,
    Parameters
    ----------
    filename: str
        name of file, relative to balloon configurations folder
    Returns
    -------
    Configuration
        contents of configuration file, ready to be parsed.
    '''
    cfg_dir_rel = Path(__file__).parent.parent.parent
    cfg_file_path = cfg_dir_rel / \
        Path(f"cfg/default_configuration/{filename}")

    with open(cfg_file_path, "r") as f:
        raw_cfg: dict = safe_load(f)
        
    req_keys = {"header", "default_config"}
    cfg_keyset = set(raw_cfg.keys())
    if not req_keys.issubset(cfg_keyset):
        raise ValueError(
            f"Config file is missing keys: {req_keys.difference(cfg_keyset)}")
    
    # return analysis config based on type
    
    analysis_type = raw_cfg["header"]["analysis_type"]

    if analysis_type == "default":
        return raw_cfg

    elif analysis_type == "characterization" :
        raise NotImplementedError("Characterziation not yet implemented")
    else:
        raise ValueError(f"analysis_type = {analysis_type} is an invalid combination.")