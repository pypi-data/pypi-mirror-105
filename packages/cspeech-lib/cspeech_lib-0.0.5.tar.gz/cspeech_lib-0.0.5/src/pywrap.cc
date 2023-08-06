#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include <string>

#include "align.h"

namespace cspeech {
namespace {
namespace py = pybind11;

std::vector<Edge> py_align(std::vector<Node>& nodes,
                                  const py::array_t<float>& logits,
                                  int blank_class = 0,
                                  bool allow_class_repeats = true) {
  if (logits.ndim() != 2) {
    throw py::value_error("logits must have 2 dimensions.");
  }
//  if (logits.itemsize() != 4) {
//    throw py::value_error("logits must have 2 dimensions.");
//  }

//  std::vector<float> flogits;
//  for (float l : logits) {
//    flogits.push_back(l)
//  }


  const std::vector<const Edge*> edges = align(nodes,
               logits.data(),
               /*num_classes=*/logits.shape(1),
               /*num_time_steps=*/logits.shape(0),
               blank_class,
               allow_class_repeats);

  // Copy the edges for python (such that it owns them).
  std::vector<Edge> edges_cp;
  for (const auto* edge : edges) {
    edges_cp.push_back(*edge);
  }
  return edges_cp;
}

std::vector<Edge> py_align_safe(std::vector<Node>& nodes,
                           const std::vector<int>& logits,
                           int num_classes,
                           int num_time_steps,
                           int blank_class = 0,
                           bool allow_class_repeats = true) {
  std::vector<float> flogits;
  for (int e : logits) {
    flogits.push_back(static_cast<float>(e) / 10000.0f);
  }
  const std::vector<const Edge*> edges = align(nodes,
                                               flogits.data(),
                                               num_classes,
                                               num_time_steps,
                                               blank_class,
                                               allow_class_repeats);

  // Copy the edges for python (such that it owns them).
  std::vector<Edge> edges_cp;
  for (const auto* edge : edges) {
    edges_cp.push_back(*edge);
  }
  return edges_cp;
}

PYBIND11_MODULE(cspeech_lib, m) {
  m.def("align",
        &py_align,
        R"(Aligns the nodes onto the logits. The logits must be a float32 numpy array of shape [time_steps, num_classes].)",
        py::arg("nodes"),
        py::arg("logits"),
        py::arg("blank_class") = 0,
        py::arg("allow_class_repeats") = true);

  m.def("py_align_safe",
        &py_align_safe,
        R"(Aligns the nodes onto the logits. The logits must be a float32 numpy array of shape [time_steps, num_classes].)",
        py::arg("nodes"),
        py::arg("logits"),
        py::arg("num_classes"),
        py::arg("num_time_steps"),
        py::arg("blank_class") = 0,
        py::arg("allow_class_repeats") = true);

  py::class_<Node>(m, "Node")
      .def(py::init<>())
      .def_readwrite("edges", &Node::edges);

  py::class_<Edge>(m, "Edge")
      .def(py::init<>())
      .def_readwrite("class_id", &Edge::class_id)
      .def_readwrite("target", &Edge::target)
      .def_readwrite("logit_penalty", &Edge::logit_penalty)
      .def_readwrite("length_logit_penalty", &Edge::length_logit_penalty);
}

}  // namespace
}  // namespace cspeech