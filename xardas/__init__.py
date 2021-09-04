import importlib.util
import os
from types import ModuleType
from typing import Optional, Dict, Tuple, List

import yaml
from discord import Activity, ActivityType, Client
from discord.ext.commands import Bot, Cog
from discord_slash import SlashCommand

from xardas.config import XardasConfig, XardasModuleConfig


def _load_config(path: str) -> XardasConfig:
    try:
        with open(path, 'r') as fp:
            return XardasConfig.parse_obj(yaml.safe_load(fp))
    except Exception as e:
        print(f'Invalid configuration file: {e}')
        exit(-1)


class Xardas(Bot):
    def __init__(self, config_path: str):
        super().__init__('§')
        self._cfg_path = config_path
        self._cfg = _load_config(self._cfg_path)

        self._task = None
        self._slash = SlashCommand(self, debug_guild=self._cfg.debug_guild, sync_commands=True)
        self._loaded_modules: Dict[str, Tuple[ModuleType, Cog]] = {}

    def get_loaded_modules(self) -> List[Tuple[str, XardasModuleConfig]]:
        return [(name, self._cfg.modules[name]) for name in set(self._loaded_modules.keys())]

    def _load(self, name: str, mod_cfg: XardasModuleConfig):
        if mod_cfg.path is None:
            path = os.path.join(self._cfg.module_path, name + '.py')
        else:
            path = mod_cfg.path

        spec = importlib.util.spec_from_file_location(f'module.{name}', path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        cog = mod.load(self)
        self.add_cog(cog)
        self._loaded_modules[name] = mod, cog

    def _unload(self, name: str):
        mod, cog = self._loaded_modules.pop(name)
        self.remove_cog(cog.qualified_name)
        mod.unload(cog)

    def _load_all_modules(self, ignore_errors=False):
        for name, cfg in self._cfg.modules.items():
            if cfg.enabled is False:
                continue

            if ignore_errors:
                try:
                    self._load(name, cfg)
                except Exception as e:
                    print(e)
            else:
                self._load(name, cfg)

    async def reload(self, module: Optional[str]):
        self._cfg = _load_config(self._cfg_path)

        if module is not None:
            if module in self._loaded_modules:
                self._unload(module)

            self._load(module, self._cfg.modules[module])
        else:
            for name in set(self._loaded_modules.keys()):
                self._unload(name)

            self._load_all_modules()

        await self._slash.sync_all_commands()

    async def on_ready(self, *_):
        await self.change_presence(activity=Activity(type=ActivityType.watching, name='you.'))

    def run(self):
        # register the builtin commands
        from xardas.builtin import load as builtin
        self.add_cog(builtin(self))

        # register all enabled modules
        self._load_all_modules(ignore_errors=True)

        return super().run(self._cfg.token)
