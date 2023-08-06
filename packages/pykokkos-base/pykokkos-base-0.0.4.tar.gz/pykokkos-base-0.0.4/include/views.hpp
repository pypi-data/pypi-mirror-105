/*
//@HEADER
// ************************************************************************
//
//                        Kokkos v. 3.0
//       Copyright (2020) National Technology & Engineering
//               Solutions of Sandia, LLC (NTESS).
//
// Under the terms of Contract DE-NA0003525 with NTESS,
// the U.S. Government retains certain rights in this software.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
// 1. Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//
// 2. Redistributions in binary form must reproduce the above copyright
// notice, this list of conditions and the following disclaimer in the
// documentation and/or other materials provided with the distribution.
//
// 3. Neither the name of the Corporation nor the names of the
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY NTESS "AS IS" AND ANY
// EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
// PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL NTESS OR THE
// CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
// EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
// PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
// PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
// LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
// NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// Questions? Contact Christian R. Trott (crtrott@sandia.gov)
//
// ************************************************************************
//@HEADER
*/

#pragma once

#include "Kokkos_Core.hpp"
#include "Kokkos_DynRankView.hpp"
#include "Kokkos_DynamicView.hpp"
#include "Kokkos_View.hpp"

#include "common.hpp"

//--------------------------------------------------------------------------------------//

template <typename Tp, size_t... Idx,
          typename RetT = std::array<size_t, sizeof...(Idx)>>
RetT get_extents(Tp &m, std::index_sequence<Idx...>) {
  return RetT{m.extent(Idx)...};
}

template <typename Up, size_t Idx, typename Tp>
constexpr auto get_stride(Tp &m);

template <typename Up, typename Tp, size_t... Idx,
          typename RetT = std::array<size_t, sizeof...(Idx)>>
RetT get_strides(Tp &m, std::index_sequence<Idx...>) {
  return RetT{(sizeof(Up) * m.stride(Idx))...};
}

#define GET_STRIDE(IDX_NUM)                                             \
  template <size_t Idx, typename Tp, enable_if_t<(Idx == IDX_NUM)> = 0> \
  constexpr auto get_stride(Tp &m) {                                    \
    return m.stride_##IDX_NUM();                                        \
  }

GET_STRIDE(0)
GET_STRIDE(1)
GET_STRIDE(2)
GET_STRIDE(3)
GET_STRIDE(4)
GET_STRIDE(5)
GET_STRIDE(6)
GET_STRIDE(7)

template <typename Up, typename Tp, size_t... Idx,
          typename RetT = std::array<size_t, sizeof...(Idx)>>
RetT get_stride(Tp &m, std::index_sequence<Idx...>) {
  return RetT{(sizeof(Up) * get_stride<Idx>(m))...};
}

//--------------------------------------------------------------------------------------//

namespace impl {
template <typename Tp, typename... Args>
struct get_item {
  static constexpr auto sequence = std::make_index_sequence<sizeof...(Args)>{};
  using tuple_type               = std::tuple<Args...>;

  template <size_t... Idx>
  static decltype(auto) get(Tp &_obj, tuple_type &&_args,
                            std::index_sequence<Idx...>) {
    return _obj.access(std::get<Idx>(std::forward<tuple_type>(_args))...);
  }

  static auto get() {
    return [](Tp &_obj, tuple_type _args) {
      return get(_obj, std::move(_args), sequence);
    };
  }
  template <typename Vp>
  static auto set() {
    return [](Tp &_obj, tuple_type _args, Vp _val) {
      get(_obj, std::move(_args), sequence) = _val;
    };
  }
};

template <typename Tp>
struct get_item<Tp, size_t> {
  static auto get() {
    return [](Tp &_obj, size_t _arg) { return _obj.access(_arg); };
  }
  template <typename Vp>
  static auto set() {
    return [](Tp &_obj, size_t _arg, Vp _val) { _obj.access(_arg) = _val; };
  }
};

template <typename Tp, size_t Idx>
struct get_type;

template <typename Tp>
struct get_type<Tp, 1> {
  using type = impl::get_item<Tp, size_t>;
};

template <typename Tp>
struct get_type<Tp, 2> {
  using type = impl::get_item<Tp, size_t, size_t>;
};

template <typename Tp>
struct get_type<Tp, 3> {
  using type = impl::get_item<Tp, size_t, size_t, size_t>;
};

template <typename Tp>
struct get_type<Tp, 4> {
  using type = impl::get_item<Tp, size_t, size_t, size_t, size_t>;
};

template <typename Tp>
struct get_type<Tp, 5> {
  using type = impl::get_item<Tp, size_t, size_t, size_t, size_t, size_t>;
};

template <typename Tp>
struct get_type<Tp, 6> {
  using type =
      impl::get_item<Tp, size_t, size_t, size_t, size_t, size_t, size_t>;
};

template <typename Tp>
struct get_type<Tp, 7> {
  using type = impl::get_item<Tp, size_t, size_t, size_t, size_t, size_t,
                              size_t, size_t>;
};

template <typename Tp>
struct get_type<Tp, 8> {
  using type = impl::get_item<Tp, size_t, size_t, size_t, size_t, size_t,
                              size_t, size_t, size_t>;
};

}  // namespace impl

template <typename Tp, size_t Idx>
struct get_item {
  using impl_type                = typename impl::get_type<Tp, Idx>::type;
  using array_type               = std::array<Tp, Idx>;
  static constexpr auto sequence = std::make_index_sequence<Idx>{};

  static auto get() { return impl_type::get(); }

  template <typename Vp>
  static auto set() {
    return impl_type::template set<Vp>();
  }
};

//--------------------------------------------------------------------------------------//

template <typename... Args>
std::string construct_name(const std::string &delim, Args &&... args) {
  std::stringstream ss;
  FOLD_EXPRESSION(ss << delim << std::forward<Args>(args));
  return ss.str().substr(delim.length());
}

//--------------------------------------------------------------------------------------//

template <typename ViewT, typename Up, size_t... Idx>
auto get_init(const std::string &lbl, const Up &arr,
              std::index_sequence<Idx...>) {
  return new ViewT(lbl, static_cast<const size_t>(std::get<Idx>(arr))...);
}

template <typename ViewT, size_t Idx>
auto get_init() {
  return [](std::string lbl, std::array<size_t, Idx> arr) {
    return get_init<ViewT>(lbl, arr, std::make_index_sequence<Idx>{});
  };
}

template <typename ViewT, typename Up, typename Tp, size_t... Idx>
auto get_unmanaged_init(const Up &arr, const Tp data,
                        std::index_sequence<Idx...>) {
  return new ViewT(data, static_cast<const size_t>(std::get<Idx>(arr))...);
}

template <typename ViewT, size_t Idx, typename Tp>
auto get_unmanaged_init() {
  return [](py::buffer buf, std::array<size_t, Idx> arr) {
    return get_unmanaged_init<ViewT>(arr, static_cast<Tp *>(buf.request().ptr),
                                     std::make_index_sequence<Idx>{});
  };
}

// define managed init
template <typename ViewT, size_t Idx, typename Tp, typename Mp, typename Vp,
          enable_if_t<!std::is_same<
              Mp, Kokkos::MemoryTraits<Kokkos::Unmanaged>>::value> = 0>
auto get_init(Vp &_view) {
  _view.def(py::init(get_init<ViewT, Idx>()));
}

// define unmanaged init
template <typename ViewT, size_t Idx, typename Tp, typename Mp, typename Vp,
          enable_if_t<std::is_same<
              Mp, Kokkos::MemoryTraits<Kokkos::Unmanaged>>::value> = 0>
auto get_init(Vp &_view) {
  _view.def(py::init(get_unmanaged_init<ViewT, Idx, Tp>()));
}

template <typename ViewT, size_t Idx, typename Up, typename Tp, typename Mp,
          typename Vp,
          enable_if_t<!std::is_same<Up, Kokkos::AnonymousSpace>::value> = 0>
auto get_init(Vp &_view) {
  get_init<ViewT, Idx, Tp, Mp>(_view);
}

template <typename ViewT, size_t Idx, typename Up, typename Tp, typename Mp,
          typename Vp,
          enable_if_t<std::is_same<Up, Kokkos::AnonymousSpace>::value> = 0>
auto get_init(Vp &) {}

//--------------------------------------------------------------------------------------//

namespace Common {
// creates overloads for data access from python
template <typename Tp, typename View_t, size_t... Idx>
void generate_view_access(py::class_<View_t> &_view,
                          std::index_sequence<Idx...>) {
  FOLD_EXPRESSION(_view.def("__getitem__", get_item<View_t, Idx + 1>::get(),
                            "Get the element"));
  FOLD_EXPRESSION(_view.def("__setitem__",
                            get_item<View_t, Idx + 1>::template set<Tp>(),
                            "Set the element"));
}

// generic function to generate a view once the view type has been specified
template <typename View_t, typename Sp, typename Tp, typename Mp, size_t DimIdx,
          size_t... Idx>
void generate_view(py::module &_mod, const std::string &_name,
                   const std::string &_msg, size_t _ndim = DimIdx + 1) {
  bool debug = false;
#if !defined(NDEBUG)
  debug = true;
#endif

  if (debug)
    std::cout << "Registering " << _msg << " as python class '" << _name
              << "'..." << std::endl;

  // class decl
  py::class_<View_t> _view(_mod, _name.c_str(), py::buffer_protocol());

  // default initializer
  _view.def(py::init([]() { return new View_t{}; }));

  // initializer with extents
  get_init<View_t, DimIdx + 1, Sp, Tp, Mp>(_view);

  // conversion to/from numpy
  _view.def_buffer([_ndim](View_t &m) -> py::buffer_info {
    auto _extents = get_extents(m, std::make_index_sequence<DimIdx + 1>{});
    auto _strides = get_stride<Tp>(m, std::make_index_sequence<DimIdx + 1>{});
    return py::buffer_info(m.data(),    // Pointer to buffer
                           sizeof(Tp),  // Size of one scalar
                           py::format_descriptor<Tp>::format(),  // Descriptor
                           _ndim,     // Number of dimensions
                           _extents,  // Buffer dimensions
                           _strides   // Strides (in bytes) for each index
    );
  });

  // shape property
  _view.def_property_readonly(
      "shape",
      [](View_t &m) {
        return get_extents(m, std::make_index_sequence<DimIdx + 1>{});
      },
      "Get the shape of the array (extents)");

  // memory space
  _view.def_property_readonly(
      "memory_space", [](View_t &) { return ViewSpaceIndex<Sp>::value; },
      "Memory space of the view");

  // support []
  generate_view_access<Tp>(_view, std::index_sequence<Idx...>{});
}

template <typename View_t, typename Sp, typename Tp, typename Mp, size_t DimIdx,
          size_t... Idx>
void generate_view(py::module &_mod, const std::string &_name,
                   const std::string &_msg, size_t _ndim,
                   std::index_sequence<Idx...>) {
  generate_view<View_t, Sp, Tp, Mp, DimIdx, Idx...>(_mod, _name, _msg, _ndim);
}
}  // namespace Common
//
