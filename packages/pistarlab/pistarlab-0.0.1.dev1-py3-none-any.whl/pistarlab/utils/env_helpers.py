import contextlib
import importlib
import logging
import os
import re
import string
from io import StringIO
from pathlib import Path

import numpy as np
import PIL.Image
from PIL import Image, ImageDraw, ImageFont
from pistarlab.utils.serialize import space_to_pyson

from ..meta import *


def get_class(module_name, class_name):
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def get_class_from_entry_point(entry_point):
    module, clss = entry_point.split(":")
    cls = get_class(module, clss)
    try:
        return cls
    except Exception as e:
        logging.error("Failed to get class for {}".format(entry_point))
        return None


def get_env_def(
        default_render_mode,
        env_kwargs,
        default_wrappers=[]):
    return {
        "default_render_mode": default_render_mode,
        "env_kwargs": env_kwargs,
        'default_wrappers': default_wrappers,
    }


def get_default_render_mode(metadata):
    render_modes = metadata.get('render.modes', [])
    default_render_mode = None
    if "rgb_array" in render_modes:
        default_render_mode = "rgb_array"
    elif "ansi" in render_modes:
        default_render_mode = "ansi"
    elif "human" in render_modes:
        default_render_mode = "human"

    return default_render_mode


def get_env_instance(entry_point, kwargs):
    return get_class_from_entry_point(entry_point)(**kwargs)


def get_wrapped_env_instance(entry_point, kwargs, wrappers):
    env = get_env_instance(entry_point, kwargs)
    for wrapper in wrappers:
        wrapper_entry_point = wrapper['entry_point']
        logging.info(f"Wrapping {entry_point} with {wrapper_entry_point}")
        wrapper_class = get_class_from_entry_point(wrapper_entry_point)
        env = wrapper_class(env=env)
    return env


def get_env_space_info(env_ref):
    meta = {}
    meta['observation_spaces'] = {'default': space_to_pyson(env_ref.observation_space)}
    meta['action_spaces'] = {'default': space_to_pyson(env_ref.action_space)}
    meta['num_players'] = 1
    meta['max_num_players'] = 1
    meta['players'] = ['default']
    meta['possible_players'] = ['default']
    return meta


def get_multiagent_env_space_info(env_ref):
    meta = {}
    meta['observation_spaces'] = {id: space_to_pyson(space) for id, space in env_ref.observation_spaces.items()}
    meta['action_spaces'] = {id: space_to_pyson(space) for id, space in env_ref.action_spaces.items()}
    meta['num_players'] = env_ref.num_players
    meta['max_num_players'] = env_ref.max_num_players
    meta['players'] = env_ref.players
    meta['possible_players'] = env_ref.possible_players
    return meta


def gen_render_image(env_ref, render_mode=None):
    if render_mode in ['rgb_array']:
        env_ref.reset()
        value = env_ref.render(mode=render_mode)
        if type(value) == np.ndarray:
            im = PIL.Image.fromarray(value)
        else:
            im = value
    else:
        im = PIL.Image.fromarray(np.zeros((10, 10)))
    return im


def get_pygame_surface_as_image(surf=None):
    import pygame
    if surf is None:
        surf = pygame.display.get_surface()
    surf_size = (surf.get_width(), surf.get_height())
    img_st = pygame.image.tostring(surf, "RGB")
    return PIL.Image.frombytes("RGB", surf_size, img_st)


PRINTABLE = set(string.printable)
COLOR_TXT_REGX = r'\x1b[[(?);]{0,2}(;?\d)*.'


def get_text_as_image(text):
    output = "".join(filter(lambda x: x in PRINTABLE, re.sub(COLOR_TXT_REGX, '', text)))
    max_line = max([len(x) for x in output.split("\n")])
    line_count = len(output.split("\n"))
    img = Image.new('RGB', (6 * max_line + 10, 14 * line_count + 10))
    d = ImageDraw.Draw(img)
    d.text((2, 2), output, fill=(255, 0, 0))
    return img


def get_stdout_as_image(render_fn):
    f = StringIO()
    with contextlib.redirect_stdout(f):
        render_fn()
    return get_text_as_image(f.getvalue())


def render_env_frame_as_image(
        render_fn,
        mode,
        output_width=None,
        output_height=None,
        ob=None):
    """
    TODO: needs cleaned
    """
    if render_fn is None:
        return None
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    img = None
    if mode == "pygame":
        try:
            img = render_fn(mode="rgb_array")
        except Exception as e:
            try:
                render_fn(mode="human")
                img = get_pygame_surface_as_image()
            except Exception as e:
                img = render_fn()
                img = get_pygame_surface_as_image()
    elif mode == "stdout":
        img = get_stdout_as_image(render_fn)
    elif mode == "ansi":
        rendered_text = render_fn(mode=mode)
        img = get_text_as_image(rendered_text)
    elif mode == "rgb_array":
        img = render_fn(mode=mode)
    else:
        logging.debug("Unknown Render mode {}, using obs".format(mode))
        try:
            img = get_text_as_image(str(ob))
            if img is not None:
                logging.debug("Render Successful")
        except Exception as e:
            pass

    if type(img) == np.ndarray:
        img = PIL.Image.fromarray(img)

    if img is not None and output_width is not None:
        if output_height is None:
            size = img.size
            aspect = size[0] / size[1]
            output_height = int(output_width / aspect)
            if output_height % 2 == 1:
                output_height += 1
        img = img.resize((output_width, output_height))

    return img


def get_env_spec_data(
        spec_id,
        entry_point=None,
        env_kwargs={},
        env_type=RL_SINGLEPLAYER_ENV,
        displayed_name=None,
        version="0.0.1-dev",
        environment_id=None,
        environment_displayed_name=None,
        description=None,
        default_wrappers=[],
        default_render_mode=None,
        metadata={},
        tags=[],
        categories=[]):
    spec_data = {}
    spec_data['spec_id'] = spec_id
    spec_data['displayed_name'] = displayed_name or spec_id
    spec_data['description'] = description
    spec_data['entry_point'] = entry_point
    spec_data['version'] = version
    spec_data['disabled'] = False
    spec_data['env_type'] = env_type
    spec_data['tags'] = tags
    spec_data['categories'] = categories
    spec_data['environment_id'] = environment_id or spec_id
    spec_data['environment_displayed_name'] = environment_displayed_name or environment_id
    spec_data['metadata'] = metadata
    spec_data['config'] = get_env_def(
        default_render_mode=default_render_mode,
        env_kwargs=env_kwargs or {},
        default_wrappers=default_wrappers)
    return spec_data


def probe_env_metadata(spec_data, image_path=None):
    """
    TODO: needs cleaned
    """
    spec_id = spec_data['spec_id']
    entry_point = spec_data['entry_point']
    env_kwargs = spec_data['config']['env_kwargs']
    default_wrappers = spec_data['config']['default_wrappers']
    render_mode = spec_data['config']['default_render_mode']
    env_type = spec_data['env_type']
    metadata = spec_data.get('metadata', {})
    environment_id = spec_data['environment_id']

    env_class = get_class_from_entry_point(entry_point)

    metadata['image_filename'] = None
    #check for class metadata
    if hasattr(env_class, 'metadata'):
        metadata.update(env_class.metadata)
    else:
        env_inst = env_class(**env_kwargs)
        if hasattr(env_inst, 'metadata'):
            metadata.update(env_inst.metadata)

    if "render.modes" not in metadata:
        metadata['render.modes'] = []
    if "render.fps" not in metadata:
        metadata['render.fps'] = 30

    # get default_render_mode
    if render_mode is None or render_mode == "null":
        render_mode = get_default_render_mode(metadata)
    metadata['render_mode'] = render_mode

    metadata['render_stats'] = "stats" in metadata['render.modes']

    # Probe env config
    env_ref = get_wrapped_env_instance(
        entry_point=entry_point,
        kwargs=env_kwargs,
        wrappers=default_wrappers)
    ob = env_ref.reset()

    if env_type == RL_SINGLEPLAYER_ENV:
        metadata.update(get_env_space_info(env_ref))
    elif env_type == RL_MULTIPLAYER_ENV:
        metadata.update(get_multiagent_env_space_info(env_ref))
    else:
        logging.error("Unknown env_type:{} for spec_id: {}".format(env_type, spec_id))

    # Generate Preview Image
    if image_path is not None:
        logging.debug("Generating Preview Image")
        try:
            img = render_env_frame_as_image(env_ref.render, render_mode, ob=ob)
        except Exception as e:
            img = None
            logging.error(e)
        if img is not None:
            image_filename = f"{environment_id}.jpg"
            image_filepath = os.path.join(image_path, image_filename)
            logging.debug("Creating image {}".format(image_filepath))
            img.save(image_filepath)
            metadata['image_filename'] = image_filename
        else:
            logging.debug("img is None")

        try:
            import pygame
            pygame.quit()
        except:
            pass
    try:
        env_ref.close()
    except:
        pass
    return metadata
