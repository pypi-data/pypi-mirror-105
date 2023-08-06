from functools import partial

import torch
import torch.nn as nn

from ..util.python_utils import make_print_if_verbose
from ..util.module_utils import get_child_module_by_names


def make_call_order_hooks(
    model, verbose=True
):
    vprint = make_print_if_verbose(verbose)

    for attr in ["_layer_logits", "_layer_logits_handles"]:
        if not hasattr(model, attr):
            setattr(model, attr, {})

    if not hasattr(model, "_last_input_ids"):
        model._last_input_ids = None
        model._last_input_ids_handle = None

    if not hasattr(model, "_ln_f_getter"):
        model._ln_f_getter = final_layernorm_locator(model)

    if not hasattr(model, "_ln_base"):
        # TODO: use
        model._ln_base = (
            nn.LayerNorm(model.config.hidden_size)
            .to(model.device)
            .requires_grad_(False)
        )

    if layer_names is None:
        h = get_child_module_by_names(model, prefixes)
        layer_names = list(range(len(h)))

    def _get_layer(name):
        return get_child_module_by_names(model, prefixes + [str(name)])

    def _make_record_logits_hook(name):
        model._layer_logits[name] = None

        def _record_logits_hook(module, input, output) -> None:
            del model._layer_logits[name]
            ln_f = model._ln_f_getter()
            model._layer_logits[name] = model.lm_head(ln_f(output[0]))

        return _record_logits_hook

    def _record_input_ids_hook(module, input, output):
        model._last_input_ids = input[0]

    def _hook_already_there(name):
        handle = model._layer_logits_handles.get(name)
        if not handle:
            return False
        layer = _get_layer(name)
        return handle.id in layer._forward_hooks

    for name in layer_names:
        if _hook_already_there(name):
            vprint(f"skipping layer {name}, hook already exists")
            continue
        layer = _get_layer(name)
        handle = layer.register_forward_hook(_make_record_logits_hook(name))
        model._layer_logits_handles[name] = handle

    if model._last_input_ids_handle is None:
        handle = model.transformer.get_input_embeddings().register_forward_hook(_record_input_ids_hook)
        model._last_input_ids_handle = handle
