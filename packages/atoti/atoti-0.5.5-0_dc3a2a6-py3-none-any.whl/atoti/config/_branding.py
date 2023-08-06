from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from .._path_utils import PathLike, to_absolute_path
from ._utils import Configuration


@dataclass(frozen=True)
class Branding(Configuration):

    accent_color: Optional[str]
    favicon: Optional[str]
    frame_color: Optional[str]
    logo: Optional[str]
    title: Optional[str]

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_branding(**data)


def create_branding(
    *,
    accent_color: Optional[str] = None,
    favicon: Optional[PathLike] = None,
    frame_color: Optional[str] = None,
    logo: Optional[PathLike] = None,
    title: Optional[str] = None,
) -> Branding:
    """Create an application branding configuration.

    Args:
        accent_color: The CSS color to give to hovered elements of the frame (header and sidenav).
        favicon: The file path to the ``.ico`` image to use as the favicon.
        frame_color: The CSS color to give to the background of the frame (header and sidenav).
        logo: The file path to the ``.svg`` image that will be displayed in a 24px by 24px area in the upper-left corner.
        title: The title to give to the page.

    Example:
        >>> python_config = tt.config.create_config(
        ...     branding=tt.config.create_branding(
        ...         accent_color="#ff00ff",
        ...         favicon="favicon.ico",
        ...         frame_color="rgb(42, 42, 42)",
        ...         logo="../logo.svg",
        ...         title="Analytic App",
        ...     )
        ... )
        >>> yaml_config = '''
        ... branding:
        ...   accent_color: "#ff00ff"
        ...   favicon: favicon.ico
        ...   frame_color: rgb(42, 42, 42)
        ...   logo: ../logo.svg
        ...   title: Analytic App
        ... '''

        .. doctest::
            :hide:

            >>> diff_yaml_config_with_python_config(yaml_config, python_config)

    """
    return Branding(
        favicon=to_absolute_path(favicon) if favicon is not None else None,
        accent_color=accent_color,
        frame_color=frame_color,
        logo=to_absolute_path(logo) if logo is not None else None,
        title=title,
    )
