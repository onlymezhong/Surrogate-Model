# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Functional tests for reduction ops."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
from tensorflow.python.framework import tensor_shape


class SumReductionTest(tf.test.TestCase):
    def _compare(self, x, reduction_axes, keep_dims, use_gpu=False):
        np_ans = x
        if reduction_axes is None:
            np_ans = np.sum(np_ans, keepdims=keep_dims)
        else:
            reduction_axes = np.array(reduction_axes).astype(np.int32)
            for ra in reduction_axes.ravel()[::-1]:
                np_ans = np.sum(np_ans, axis=ra, keepdims=keep_dims)
        with self.test_session(use_gpu=use_gpu):
            tf_ans = tf.reduce_sum(x, reduction_axes, keep_dims)
            out = tf_ans.eval()
        self.assertAllClose(np_ans, out)
        self.assertShapeEqual(np_ans, tf_ans)

    def _compareAll(self, x, reduction_axes):
        if reduction_axes is not None and np.shape(reduction_axes) == (1,):
            # Test scalar reduction_axes argument
            self._compareAll(x, reduction_axes[0])
        self._compare(x, reduction_axes, False, use_gpu=True)
        self._compare(x, reduction_axes, False, use_gpu=False)
        self._compare(x, reduction_axes, True, use_gpu=True)
        self._compare(x, reduction_axes, True, use_gpu=False)

    def testFloatReduce1D(self):
        # Create a 1D array of floats
        np_arr = np.arange(1, 6).reshape([5]).astype(np.float32)
        self._compareAll(np_arr, [0])

    def testFloatReduce2D(self):
        # Create a 2D array of floats and reduce across all possible
        # dimensions
        np_arr = np.arange(0, 10).reshape([2, 5]).astype(np.float32)
        self._compareAll(np_arr, None)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])
        self._compareAll(np_arr, [1])
        self._compareAll(np_arr, [0, 1])

    def testFloatReduce3D(self):
        # Create a 3D array of floats and reduce across all possible
        # dimensions
        np_arr = np.arange(0, 30).reshape([2, 3, 5]).astype(np.float32)
        self._compareAll(np_arr, None)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])
        self._compareAll(np_arr, [1])
        self._compareAll(np_arr, [2])
        self._compareAll(np_arr, [0, 1])
        self._compareAll(np_arr, [1, 2])
        self._compareAll(np_arr, [0, 2])
        self._compareAll(np_arr, [0, 1, 2])

    def testFloatReduce4D(self):
        # Create a 4D array of floats and reduce across some
        # dimensions
        np_arr = np.arange(0, 210).reshape([2, 3, 5, 7]).astype(np.float32)
        self._compareAll(np_arr, None)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])
        self._compareAll(np_arr, [1])
        self._compareAll(np_arr, [2])
        self._compareAll(np_arr, [0, 1])
        self._compareAll(np_arr, [1, 2])
        # Need specialization for reduce(4D, [0, 2])
        # self._compareAll(np_arr, [0, 2])
        self._compareAll(np_arr, [0, 1, 2])
        self._compareAll(np_arr, [1, 2, 3])
        self._compareAll(np_arr, [0, 1, 2, 3])

    def testFloatReduce5D(self):
        # Create a 5D array of floats and reduce across some dimensions
        np_arr = np.arange(0, 840).reshape([2, 3, 5, 7, 4]).astype(np.float32)
        self._compareAll(np_arr, None)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])
        self._compareAll(np_arr, [1])
        self._compareAll(np_arr, [2])
        self._compareAll(np_arr, [0, 1])
        self._compareAll(np_arr, [1, 2])
        # Need specialization for reduce(4D, [0, 2])
        # self._compareAll(np_arr, [0, 2])
        self._compareAll(np_arr, [0, 1, 2])
        self._compareAll(np_arr, [1, 2, 3])
        self._compareAll(np_arr, [0, 1, 2, 3])
        self._compareAll(np_arr, [1, 2, 3, 4])
        self._compareAll(np_arr, [0, 1, 2, 3, 4])

    # Simple tests for various types.
    def testDoubleReduce1D(self):
        np_arr = np.arange(1, 6).reshape([5]).astype(np.float64)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])

    def testInt32Reduce1D(self):
        np_arr = np.arange(1, 6).reshape([5]).astype(np.int32)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])

    def testComplex64Reduce1D(self):
        np_arr = np.arange(1, 6).reshape([5]).astype(np.complex64)
        self._compare(np_arr, [], False)
        self._compare(np_arr, [0], False)

    def testInvalidIndex(self):
        np_arr = np.arange(0, 10).reshape([2, 5]).astype(np.float32)
        input_tensor = tf.convert_to_tensor(np_arr)
        with self.assertRaisesWithPredicateMatch(
                ValueError, lambda e: "Invalid reduction dimension" in str(e)):
            tf.reduce_sum(input_tensor, [-1])
        with self.assertRaisesWithPredicateMatch(
                ValueError, lambda e: "Invalid reduction dimension" in str(e)):
            tf.reduce_sum(input_tensor, [2])
        with self.assertRaisesWithPredicateMatch(
                ValueError, lambda e: "Invalid reduction dimension" in str(e)):
            tf.reduce_sum(input_tensor, [0, 2])

    # Int64??

    def _compareGradient(self, shape, sum_shape, reduction_axes):
        if reduction_axes is not None and np.shape(reduction_axes) == (1,):
            # Test scalar reduction_axes argument
            self._compareGradient(shape, sum_shape, reduction_axes[0])
        x = np.arange(1.0, 49.0).reshape(shape).astype(np.float64)
        with self.test_session():
            t = tf.convert_to_tensor(x)
            su = tf.reduce_sum(t, reduction_axes)
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        shape,
                                                        su,
                                                        sum_shape,
                                                        x_init_value=x,
                                                        delta=1)
        self.assertAllClose(jacob_t, jacob_n, rtol=1e-8, atol=1e-8)

    def testGradient(self):
        self._compareGradient([2, 3, 4, 2], [2, 2], [1, 2])

    def testGradient2(self):
        self._compareGradient([2, 3, 4, 2], [2, 4, 2], [1])

    def testGradient3(self):
        self._compareGradient([2, 3, 4, 2], [2, 3, 2], [2])

    def testGradient4(self):
        self._compareGradient([2, 3, 4, 2], [], None)

    def testHighRank(self):
        # Do a bunch of random high dimensional reductions
        np.random.seed(42)
        for _ in range(20):
            rank = np.random.randint(4, 10 + 1)
            axes, = np.nonzero(np.random.randint(2, size=rank))
            shape = tuple(np.random.randint(1, 3 + 1, size=rank))
            data = np.random.randint(1024, size=shape)
            self._compareAll(data, axes)
        # Check some particular axis patterns
        for rank in 4, 7, 10:
            shape = tuple(np.random.randint(1, 3 + 1, size=rank))
            data = np.random.randint(1024, size=shape)
            for axes in ([], np.arange(rank), np.arange(0, rank, 2),
                         np.arange(1, rank, 2)):
                self._compareAll(data, axes)

    def testExpand(self):
        # Reduce an empty tensor to a nonempty tensor
        x = np.zeros((5, 0))
        self._compareAll(x, [1])


class MeanReductionTest(tf.test.TestCase):
    def _compare(self, x, reduction_axes, keep_dims):
        np_sum = x
        count = 1
        for ra in reduction_axes[::-1]:
            np_sum = np.sum(np_sum, axis=ra, keepdims=keep_dims)
            count *= x.shape[ra]
        np_ans = np_sum / count
        with self.test_session():
            reduction_axes = np.array(reduction_axes).astype(np.int32)
            tf_ans = tf.reduce_mean(x, reduction_axes, keep_dims)
            out = tf_ans.eval()
        self.assertAllClose(np_ans, out)
        self.assertShapeEqual(np_ans, tf_ans)

    def _compareAll(self, x, reduction_axes):
        self._compare(x, reduction_axes, False)
        self._compare(x, reduction_axes, True)

    def testFloatReduce3D(self):
        # Create a 3D array of floats and reduce across all possible
        # dimensions
        np_arr = np.arange(0, 30).reshape([2, 3, 5]).astype(np.float32)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])
        self._compareAll(np_arr, [1])
        self._compareAll(np_arr, [2])
        self._compareAll(np_arr, [0, 1])
        self._compareAll(np_arr, [1, 2])
        self._compareAll(np_arr, [0, 2])
        self._compareAll(np_arr, [0, 1, 2])

    def testDoubleReduce3D(self):
        # Create a 3D array of doubles and reduce across all possible
        # dimensions
        np_arr = np.arange(0, 30).reshape([2, 3, 5]).astype(np.float64)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])
        self._compareAll(np_arr, [1])
        self._compareAll(np_arr, [2])
        self._compareAll(np_arr, [0, 1])
        self._compareAll(np_arr, [1, 2])
        self._compareAll(np_arr, [0, 2])
        self._compareAll(np_arr, [0, 1, 2])

    def testGradient(self):
        s = [2, 3, 4, 2]
        x = np.arange(1.0, 49.0).reshape(s).astype(np.float32)
        with self.test_session():
            t = tf.convert_to_tensor(x)
            su = tf.reduce_mean(t, [1, 2])
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        s,
                                                        su,
                                                        [2, 2],
                                                        x_init_value=x,
                                                        delta=1)
            self.assertAllClose(jacob_t, jacob_n, rtol=1e-3, atol=1e-3)

            su = tf.reduce_mean(t, [0, 1, 2, 3])
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        s,
                                                        su,
                                                        [1],
                                                        x_init_value=x,
                                                        delta=1)
            self.assertAllClose(jacob_t, jacob_n, rtol=1e-3, atol=1e-3)

            su = tf.reduce_mean(t, [])
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        s,
                                                        su,
                                                        [2, 3, 4, 2],
                                                        x_init_value=x,
                                                        delta=1)
            self.assertAllClose(jacob_t, jacob_n, rtol=1e-3, atol=1e-3)


class ProdReductionTest(tf.test.TestCase):
    def _compare(self, x, reduction_axes, keep_dims):
        np_ans = x
        if reduction_axes is None:
            np_ans = np.prod(np_ans, keepdims=keep_dims)
        else:
            for ra in reduction_axes[::-1]:
                np_ans = np.prod(np_ans, axis=ra, keepdims=keep_dims)
        with self.test_session():
            if reduction_axes is not None:
                reduction_axes = np.array(reduction_axes).astype(np.int32)
            tf_ans = tf.reduce_prod(x, reduction_axes, keep_dims)
            out = tf_ans.eval()
        self.assertAllClose(np_ans, out)
        self.assertShapeEqual(np_ans, tf_ans)

    def _compareAll(self, x, reduction_axes):
        self._compare(x, reduction_axes, False)
        self._compare(x, reduction_axes, True)

    def testFloatReduce3D(self):
        # Create a 3D array of floats and reduce across all possible
        # dimensions
        np_arr = np.arange(0, 30).reshape([2, 3, 5]).astype(np.float32)
        self._compareAll(np_arr, None)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])
        self._compareAll(np_arr, [1])
        self._compareAll(np_arr, [2])
        self._compareAll(np_arr, [0, 1])
        self._compareAll(np_arr, [1, 2])
        self._compareAll(np_arr, [0, 2])
        self._compareAll(np_arr, [0, 1, 2])

    def testGradient(self):
        s = [2, 3, 4, 2]
        # NOTE(kearnes): divide by 20 so product is a reasonable size
        x = np.arange(1.0, 49.0).reshape(s).astype(np.float32) / 20.
        with self.test_session():
            t = tf.convert_to_tensor(x)

            su = tf.reduce_prod(t, [])
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        s,
                                                        su,
                                                        [2, 3, 4, 2],
                                                        x_init_value=x,
                                                        delta=1)
            self.assertAllClose(jacob_t, jacob_n, rtol=1e-3, atol=1e-3)

            su = tf.reduce_prod(t, [1, 2])
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        s,
                                                        su,
                                                        [2, 2],
                                                        x_init_value=x,
                                                        delta=1)
            self.assertAllClose(jacob_t, jacob_n, rtol=1e-3, atol=1e-3)

            su = tf.reduce_prod(t, [0, 1, 2, 3])
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        s,
                                                        su,
                                                        [1],
                                                        x_init_value=x,
                                                        delta=1)
            self.assertAllClose(jacob_t, jacob_n, rtol=1e-3, atol=1e-3)

        # NOTE(kearnes): the current gradient calculation gives NaNs for 0 inputs
        x = np.arange(0.0, 48.0).reshape(s).astype(np.float32) / 20.
        with self.test_session():
            t = tf.convert_to_tensor(x)
            su = tf.reduce_prod(t, [])
            jacob_t, _ = tf.test.compute_gradient(t,
                                                  s,
                                                  su,
                                                  [2, 3, 4, 2],
                                                  x_init_value=x,
                                                  delta=1)
            with self.assertRaisesOpError("Tensor had NaN values"):
                tf.check_numerics(jacob_t, message="_ProdGrad NaN test").op.run()


class MinReductionTest(tf.test.TestCase):
    def _compare(self, x, reduction_axes, keep_dims, use_gpu=False):
        np_ans = x
        if reduction_axes is None:
            np_ans = np.amin(np_ans, keepdims=keep_dims)
        else:
            for ra in reduction_axes[::-1]:
                np_ans = np.amin(np_ans, axis=ra, keepdims=keep_dims)
        with self.test_session(use_gpu=use_gpu):
            if reduction_axes is not None:
                reduction_axes = np.array(reduction_axes).astype(np.int32)
            tf_ans = tf.reduce_min(x, reduction_axes, keep_dims)
            out = tf_ans.eval()
        self.assertAllClose(np_ans, out)
        self.assertShapeEqual(np_ans, tf_ans)

    def _compareAll(self, x, reduction_axes):
        self._compare(x, reduction_axes, False, use_gpu=True)
        self._compare(x, reduction_axes, False, use_gpu=False)
        self._compare(x, reduction_axes, True, use_gpu=True)
        self._compare(x, reduction_axes, True, use_gpu=False)

    def testFloatReduce3D(self):
        # Create a 3D array of floats and reduce across all possible
        # dimensions
        np_arr = np.arange(0, 30).reshape([2, 3, 5]).astype(np.float32)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])
        self._compareAll(np_arr, [1])
        self._compareAll(np_arr, [2])
        self._compareAll(np_arr, [0, 1])
        self._compareAll(np_arr, [1, 2])
        self._compareAll(np_arr, [0, 2])
        self._compareAll(np_arr, [0, 1, 2])

    def testDoubleReduce3D(self):
        # Create a 3D array of doubles and reduce across all possible
        # dimensions
        np_arr = np.arange(0, 30).reshape([2, 3, 5]).astype(np.float64)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])
        self._compareAll(np_arr, [1])
        self._compareAll(np_arr, [2])
        self._compareAll(np_arr, [0, 1])
        self._compareAll(np_arr, [1, 2])
        self._compareAll(np_arr, [0, 2])
        self._compareAll(np_arr, [0, 1, 2])

    def testGradient(self):
        s = [2, 3, 4, 2]
        x = np.arange(1.0, 49.0).reshape(s).astype(np.float64)
        with self.test_session():
            t = tf.convert_to_tensor(x)
            su = tf.reduce_min(t, [1, 2])
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        s,
                                                        su,
                                                        [2, 2],
                                                        x_init_value=x,
                                                        delta=1)
        self.assertAllClose(jacob_t, jacob_n, rtol=1e-8, atol=1e-8)

    def testGradient2(self):
        s = [2, 3, 4, 2]
        x = np.arange(1.0, 49.0).reshape(s).astype(np.float64)
        with self.test_session():
            t = tf.convert_to_tensor(x)
            su = tf.reduce_min(t, [1])
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        s,
                                                        su,
                                                        [2, 4, 2],
                                                        x_init_value=x,
                                                        delta=1)
        self.assertAllClose(jacob_t, jacob_n, rtol=1e-8, atol=1e-8)

    def testGradient3(self):
        s = [2, 3, 4, 2]
        x = np.arange(1.0, 49.0).reshape(s).astype(np.float64)
        with self.test_session():
            t = tf.convert_to_tensor(x)
            su = tf.reduce_min(t, [2])
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        s,
                                                        su,
                                                        [2, 3, 2],
                                                        x_init_value=x,
                                                        delta=1)
        self.assertAllClose(jacob_t, jacob_n, rtol=1e-8, atol=1e-8)

    def testGradient4(self):
        s = [2, 3, 4, 2]
        x = np.arange(1.0, 49.0).reshape(s).astype(np.float64)
        with self.test_session():
            t = tf.convert_to_tensor(x)
            su = tf.reduce_min(t)
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        s,
                                                        su,
                                                        [1],
                                                        x_init_value=x,
                                                        delta=1)
        self.assertAllClose(jacob_t, jacob_n, rtol=1e-8, atol=1e-8)


class MaxReductionTest(tf.test.TestCase):
    def _compare(self, x, reduction_axes, keep_dims, use_gpu=False):
        np_ans = x
        if reduction_axes is None:
            np_ans = np.amax(np_ans, keepdims=keep_dims)
        else:
            for ra in reduction_axes[::-1]:
                np_ans = np.amax(np_ans, axis=ra, keepdims=keep_dims)
        with self.test_session(use_gpu=use_gpu):
            if reduction_axes is not None:
                reduction_axes = np.array(reduction_axes).astype(np.int32)
            tf_ans = tf.reduce_max(x, reduction_axes, keep_dims)
            out = tf_ans.eval()
        self.assertAllClose(np_ans, out)
        self.assertShapeEqual(np_ans, tf_ans)

    def _compareAll(self, x, reduction_axes):
        self._compare(x, reduction_axes, False, use_gpu=True)
        self._compare(x, reduction_axes, False, use_gpu=False)
        self._compare(x, reduction_axes, True, use_gpu=True)
        self._compare(x, reduction_axes, True, use_gpu=False)

    def testFloatReduce3D(self):
        # Create a 3D array of floats and reduce across all possible
        # dimensions
        np_arr = np.arange(0, 30).reshape([2, 3, 5]).astype(np.float32)
        self._compareAll(np_arr, None)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])
        self._compareAll(np_arr, [1])
        self._compareAll(np_arr, [2])
        self._compareAll(np_arr, [0, 1])
        self._compareAll(np_arr, [1, 2])
        self._compareAll(np_arr, [0, 2])
        self._compareAll(np_arr, [0, 1, 2])

    def testDoubleReduce3D(self):
        # Create a 3D array of doubles and reduce across all possible
        # dimensions
        np_arr = np.arange(0, 30).reshape([2, 3, 5]).astype(np.float64)
        self._compareAll(np_arr, None)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])
        self._compareAll(np_arr, [1])
        self._compareAll(np_arr, [2])
        self._compareAll(np_arr, [0, 1])
        self._compareAll(np_arr, [1, 2])
        self._compareAll(np_arr, [0, 2])
        self._compareAll(np_arr, [0, 1, 2])

    def testGradient(self):
        s = [2, 3, 4, 2]
        x = np.arange(1.0, 49.0).reshape(s).astype(np.float64)
        with self.test_session():
            t = tf.convert_to_tensor(x)
            su = tf.reduce_max(t, [1, 2])
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        s,
                                                        su,
                                                        [2, 2],
                                                        x_init_value=x,
                                                        delta=1)
        self.assertAllClose(jacob_t, jacob_n, rtol=1e-8, atol=1e-8)

    def testGradient2(self):
        s = [2, 3, 4, 2]
        x = np.arange(1.0, 49.0).reshape(s).astype(np.float64)
        with self.test_session():
            t = tf.convert_to_tensor(x)
            su = tf.reduce_max(t, [1])
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        s,
                                                        su,
                                                        [2, 4, 2],
                                                        x_init_value=x,
                                                        delta=1)
        self.assertAllClose(jacob_t, jacob_n, rtol=1e-8, atol=1e-8)

    def testGradient3(self):
        s = [2, 3, 4, 2]
        x = np.arange(1.0, 49.0).reshape(s).astype(np.float64)
        with self.test_session():
            t = tf.convert_to_tensor(x)
            su = tf.reduce_max(t, [2])
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        s,
                                                        su,
                                                        [2, 3, 2],
                                                        x_init_value=x,
                                                        delta=1)
        self.assertAllClose(jacob_t, jacob_n, rtol=1e-8, atol=1e-8)

    def testGradient4(self):
        s = [2, 3, 4, 2]
        x = np.arange(1.0, 49.0).reshape(s).astype(np.float64)
        with self.test_session():
            t = tf.convert_to_tensor(x)
            su = tf.reduce_max(t)
            jacob_t, jacob_n = tf.test.compute_gradient(t,
                                                        s,
                                                        su,
                                                        [1],
                                                        x_init_value=x,
                                                        delta=1)
        self.assertAllClose(jacob_t, jacob_n, rtol=1e-8, atol=1e-8)


class AllReductionTest(tf.test.TestCase):
    def _compare(self, x, reduction_axes, keep_dims, use_gpu=False):
        np_ans = x
        if reduction_axes is None:
            np_ans = np.all(np_ans, keepdims=keep_dims)
        else:
            for ra in reduction_axes[::-1]:
                np_ans = np.all(np_ans, axis=ra, keepdims=keep_dims)
        with self.test_session(use_gpu=use_gpu):
            if reduction_axes is not None:
                reduction_axes = np.array(reduction_axes).astype(np.int32)
            tf_ans = tf.reduce_all(x, reduction_axes, keep_dims)
            out = tf_ans.eval()
        self.assertAllEqual(np_ans, out)
        self.assertShapeEqual(np_ans, tf_ans)

    def _compareAll(self, x, reduction_axes):
        self._compare(x, reduction_axes, False, use_gpu=True)
        self._compare(x, reduction_axes, False, use_gpu=False)
        self._compare(x, reduction_axes, True, use_gpu=True)
        self._compare(x, reduction_axes, True, use_gpu=False)

    def testAll3D(self):
        # Create a 3D array of bools and reduce across all possible
        # dimensions
        np_arr = (np.random.uniform(0, 1, 30) > 0.1).reshape([2, 3, 5])
        self._compareAll(np_arr, None)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])
        self._compareAll(np_arr, [1])
        self._compareAll(np_arr, [2])
        self._compareAll(np_arr, [0, 1])
        self._compareAll(np_arr, [1, 2])
        self._compareAll(np_arr, [0, 2])
        self._compareAll(np_arr, [0, 1, 2])


class AnyReductionTest(tf.test.TestCase):
    def _compare(self, x, reduction_axes, keep_dims, use_gpu=False):
        np_ans = x
        if reduction_axes is None:
            np_ans = np.any(np_ans, keepdims=keep_dims)
        else:
            for ra in reduction_axes[::-1]:
                np_ans = np.any(np_ans, axis=ra, keepdims=keep_dims)
        with self.test_session(use_gpu=use_gpu):
            if reduction_axes is not None:
                reduction_axes = np.array(reduction_axes).astype(np.int32)
            tf_ans = tf.reduce_any(x, reduction_axes, keep_dims)
            out = tf_ans.eval()
        self.assertAllEqual(np_ans, out)
        self.assertShapeEqual(np_ans, tf_ans)

    def _compareAll(self, x, reduction_axes):
        self._compare(x, reduction_axes, False, use_gpu=True)
        self._compare(x, reduction_axes, False, use_gpu=False)
        self._compare(x, reduction_axes, True, use_gpu=True)
        self._compare(x, reduction_axes, True, use_gpu=False)

    def testAll3D(self):
        # Create a 3D array of bools and reduce across all possible
        # dimensions
        np_arr = (np.random.uniform(0, 1, 30) > 0.9).reshape([2, 3, 5])
        self._compareAll(np_arr, None)
        self._compareAll(np_arr, [])
        self._compareAll(np_arr, [0])
        self._compareAll(np_arr, [1])
        self._compareAll(np_arr, [2])
        self._compareAll(np_arr, [0, 1])
        self._compareAll(np_arr, [1, 2])
        self._compareAll(np_arr, [0, 2])
        self._compareAll(np_arr, [0, 1, 2])

    def testPartialShapes(self):
        # Input shape is unknown.
        c_unknown = tf.placeholder(tf.float32)
        s_unknown = tf.reduce_sum(c_unknown, [1, 2])
        self.assertEqual(tensor_shape.unknown_shape(), s_unknown.get_shape())

        # Input shape only has known rank.
        c_known_rank = tf.placeholder(tf.float32)
        c_known_rank.set_shape(tensor_shape.unknown_shape(ndims=3))
        s_known_rank = tf.reduce_sum(c_known_rank, [1, 2], keep_dims=True)
        self.assertEqual(3, s_known_rank.get_shape().ndims)

        # Reduction indices are unknown.
        unknown_indices = tf.placeholder(tf.int32)
        c_unknown_indices = tf.constant([[10.0], [20.0]])
        s_unknown_indices = tf.reduce_sum(c_unknown_indices, unknown_indices,
                                          keep_dims=False)
        self.assertEqual(tensor_shape.unknown_shape(),
                         s_unknown_indices.get_shape())
        s_unknown_indices_keep = tf.reduce_sum(c_unknown_indices, unknown_indices,
                                               keep_dims=True)
        self.assertEqual(2, s_unknown_indices_keep.get_shape().ndims)


if __name__ == "__main__":
    tf.test.main()
