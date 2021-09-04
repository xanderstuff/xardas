from typing import Optional, Any, Dict

from pydantic import BaseModel, Field


class XardasModuleConfig(BaseModel):
    description: Optional[str] = None
    path: Optional[str] = None
    enabled: bool = True
    config: Dict[str, Any] = {}


class XardasConfig(BaseModel):
    token: str = Field(description='The bot\'s token (required).')
    debug_guild: Optional[int] = Field(description='Set to to a guild ID to use when developing the bot.')
    module_path: str = '/etc/xardas/modules'
    modules: Dict[str, XardasModuleConfig] = Field(default_factory=dict, description='A list of modules to expose.')
