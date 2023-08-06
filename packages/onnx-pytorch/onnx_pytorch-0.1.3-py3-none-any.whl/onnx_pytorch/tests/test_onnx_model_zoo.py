from tempfile import TemporaryDirectory

import os
import importlib.util

import numpy as np
import onnx
import onnxruntime
from onnx.numpy_helper import to_array
from onnxruntime.tools.symbolic_shape_infer import SymbolicShapeInference
import pytest
import torch

from onnx_model_maker import *
from onnx_model_maker.ops import *
from onnx_pytorch import code_gen

torch.set_printoptions(8)


class TestModel:

  def _run(self, inputs_np, onnx_model):
    model = onnx.ModelProto()
    model.CopyFrom(onnx_model)
    sess_options = onnxruntime.SessionOptions()
    session = onnxruntime.InferenceSession(model.SerializeToString(),
                                           sess_options)
    ort_outputs = session.run(None, {k: v for k, v in inputs_np})
    model.graph.ClearField("value_info")
    model = SymbolicShapeInference.infer_shapes(model, 2**31 - 1, True, True, 1)
    with TemporaryDirectory() as tmpdir:
      tmpdir = "/Users/wenhao/Projects/onnx-pytorch/onnx_pytorch/tests/tmp"
      code_gen.gen(model,
                   output_dir=tmpdir,
                   tensor_inplace=True,
                   simplify_names=True)
      spec = importlib.util.spec_from_file_location(
          "model", os.path.join(tmpdir, "model.py"))
      mod = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(mod)
      pt_outputs = mod.test_run_model(
          [torch.from_numpy(v) for _, v in inputs_np])
      assert np.allclose(ort_outputs, [o.detach().numpy() for o in pt_outputs],
                         atol=1e-5,
                         rtol=1e-5,
                         equal_nan=True)

  # def test_ugmarketing(self):
  #   ugmarkering_model_path = "/Users/wenhao/Projects/ai_speed/saved_model/model.onnx"
  #   if not os.path.exists(ugmarkering_model_path):
  #     return False
  #   model = onnx.load(ugmarkering_model_path)
  #   self._run(
  #       [("import/whole_input:0", np.random.randn(1, 2905).astype(np.float32))],
  #       model)
  #
  # def test_gongxian(self):
  #   model_path = "/Users/wenhao/Projects/ai_speed/cenaniang_new.onnx"
  #   if not os.path.exists(model_path):
  #     return False
  #   model = onnx.load(model_path)
  #   self._run([("input", np.random.randn(1, 4576).astype(np.float32))], model)

  # def test_dcn(self):
  #   model_path = "/Users/wenhao/Projects/DeepCTR/model.onnx"
  #   if not os.path.exists(model_path):
  #     return False
  #   model = onnx.load(model_path)
  #   b = 10
  #   self._run([
  #       ("x_5:0", np.random.randint(0, 188, (b, 1)).astype(np.int32)),
  #       ("x_4:0", np.random.randint(0, 20, (b, 1)).astype(np.int32)),
  #       ("x_3:0", np.random.randint(0, 7, (b, 1)).astype(np.int32)),
  #       ("x_2:0", np.random.randint(0, 2, (b, 1)).astype(np.int32)),
  #       ("x_1:0", np.random.randint(0, 193, (b, 1)).astype(np.int32)),
  #       ("x:0", np.random.randint(0, 187, (b, 1)).astype(np.int32)),
  #   ], model)

  def test_dcn_criteo(self):
    model_path = "/Users/wenhao/Projects/DeepCTR/dcn_criteo.onnx"
    if not os.path.exists(model_path):
      return False
    model = onnx.load(model_path)
    initializers = {i.name: i for i in model.graph.initializer}
    inputs = [i.name for i in model.graph.input if i.name not in initializers]
    nodes = {
        n.input[1]: n
        for n in model.graph.node
        if n.op_type == "Gather" and n.input[1] in inputs
    }
    mapping = {i: nodes[i].input[0].split("/")[1].split("_")[-1] for i in inputs if i in nodes}
    mapping.update({i: f"I{int(i.split('_')[1].split(':')[0]) - 25}" for i in inputs if i not in nodes})
    b = 10
    inputs_np = [
        (i,
         np.random.randint(0,
                           to_array(initializers[nodes[i].input[0]]).shape[0],
                           (b, 1)).astype(np.int32)
         if i in nodes else np.random.randn(b, 1).astype(np.float32))
        for i in inputs
    ]
    self._run(inputs_np, model)


if __name__ == '__main__':
  pytest.main(['-s', 'test_onnx_model_zoo.py'])
