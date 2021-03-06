from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import tensorflow.contrib.slim as slim

import numpy as np

from ray.rllib.models.model import Model


def normc_initializer(std=1.0):
    def _initializer(shape, dtype=None, partition_info=None):
        out = np.random.randn(*shape).astype(np.float32)
        out *= std / np.sqrt(np.square(out).sum(axis=0, keepdims=True))
        return tf.constant(out)
    return _initializer


class FullyConnectedNetwork(Model):
    """Generic fully connected network."""

    def _init(self, inputs, num_outputs, options):
        hiddens = options.get("fcnet_hiddens", [256, 256])
        activation = options.get("fcnet_activation", tf.nn.tanh)
        print("Constructing fcnet {} {}".format(hiddens, activation))

        with tf.name_scope("fc_net"):
            i = 1
            last_layer = inputs
            for size in hiddens:
                last_layer = slim.fully_connected(
                    last_layer, size,
                    weights_initializer=normc_initializer(1.0),
                    activation_fn=activation,
                    scope="fc{}".format(i))
                i += 1
            output = slim.fully_connected(
                last_layer, num_outputs,
                weights_initializer=normc_initializer(0.01),
                activation_fn=None, scope="fc_out")
            return output, last_layer
