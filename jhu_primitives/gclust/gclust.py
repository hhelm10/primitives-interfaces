#!/usr/bin/env python

# gclust.py
# Copyright (c) 2017. All rights reserved.

from rpy2 import robjects
from typing import Sequence, TypeVar, Union, Dict
import os
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()
from primitive_interfaces.transformer import TransformerPrimitiveBase
#from jhu_primitives.core.JHUGraph import JHUGraph
import numpy as np
from d3m.metadata import container, hyperparams, metadata as metadata_module, params, utils
from d3m.primitive_interfaces import base
from d3m.primitive_interfaces.base import CallResult


Inputs = container.ndarray
Outputs = container.ndarray

class Params(params.Params):
    pass

class Hyperparams(hyperparams.Hyperparams):
    dim = hyperparams.Hyperparameter[int](default = 2)

class GaussianClustering(TransformerPrimitiveBase[Inputs, Outputs, Hyperparams]):
    # This should contain only metadata which cannot be automatically determined from the code.
    metadata = metadata_module.PrimitiveMetadata({
        # Simply an UUID generated once and fixed forever. Generated using "uuid.uuid4()".
        'id': '5194ef94-3683-319a-9d8d-5c3fdd09de24',
        'version': "0.1.0",
        'name': "jhu.gclust",
        # The same path the primitive is registered with entry points in setup.py.
        'python_path': 'd3m.primitives.jhu_primitives.GaussianClustering',
        # Keywords do not have a controlled vocabulary. Authors can put here whatever they find suitable.
        'keywords': ['gaussian clustering'],
        'source': {
            'name': "JHU",
            'uris': [
                # Unstructured URIs. Link to file and link to repo in this case.
                'https://github.com/neurodata/primitives-interfaces/jhu_primitives/gclust/gclust.py',
#                'https://github.com/youngser/primitives-interfaces/blob/jp-devM1/jhu_primitives/ase/ase.py',
                'https://github.com/neurodata/primitives-interfaces.git',
            ],
        },
        # A list of dependencies in order. These can be Python packages, system packages, or Docker images.
        # Of course Python packages can also have their own dependencies, but sometimes it is necessary to
        # install a Python package first to be even able to run setup.py of another package. Or you have
        # a dependency which is not on PyPi.
        'installation': [
            {
            'type': 'UBUNTU',
            'package': 'r-base',
            'version': '3.4.2'
            },
            {
            'type': 'UBUNTU',
            'package': 'libxml2-dev',
            'version': '2.9.4'
            },
            {
            'type': 'UBUNTU',
            'package': 'libpcre3-dev',
            'version': '2.9.4'
            },
#            {
#            'type': 'UBUNTU',
#            'package': 'r-base-dev',
#            'version': '3.4.2'
#            },
#            {
#            'type': 'UBUNTU',
#            'package': 'r-recommended',
#            'version': '3.4.2'
#            },
            {
            'type': 'PIP',
            'package_uri': 'git+https://github.com/neurodata/primitives-interfaces.git@{git_commit}#egg=jhu_primitives'.format(
                git_commit=utils.current_git_commit(os.path.dirname(__file__)),
            ),
        }],
        # URIs at which one can obtain code for the primitive, if available.
        # 'location_uris': [
        #     'https://gitlab.com/datadrivendiscovery/tests-data/raw/{git_commit}/primitives/test_primitives/monomial.py'.format(
        #         git_commit=utils.current_git_commit(os.path.dirname(__file__)),
        #     ),
        # ],
        # Choose these from a controlled vocabulary in the schema. If anything is missing which would
        # best describe the primitive, make a merge request.
        'algorithm_types': [
            "GAUSSIAN_PROCESS"
        ],
        'primitive_family': "CLUSTERING"
    })

    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, docker_containers: Dict[str, str] = None) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed, docker_containers=docker_containers)

    def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> CallResult[Outputs]:
        """
        TODO: YP description

        **Positional Arguments:**

        inputs:
            - A matrix

        **Optional Arguments:**

        dim:
            - The number of clusters in which to assign the data
        """

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                "gclust.interface.R")

        dim = self.hyperparams['dim']
        cmd = """
        source("%s")
        fn <- function(X, dim) {
            gclust.interface(X, dim)
        }
        """ % path

        print(cmd)

        result = int(robjects.r(cmd)(inputs, dim)[0])

        outputs = container.ndarray(result)

        return base.CallResult(outputs)




'''
import os
import numpy as np
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()

from typing import Sequence, TypeVar
from primitive_interfaces.transformer import TransformerPrimitiveBase

Input = np.ndarray
Output = np.ndarray
Params = TypeVar('Params')

class GaussianClustering(TransformerPrimitiveBase[Input, Output, Params]):
    def cluster(self, *, inputs: Input) -> int:
        """
        TODO: YP description

        **Positional Arguments:**

        inputs:
            - A matrix

        **Optional Arguments:**

        dim:
            - The number of clusters in which to assign the data
        """

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                "gclust.interface.R")
        cmd = """
        source("%s")
        fn <- function(X, dim) {
            gclust.interface(X, dim)
        }
        """ % path
        return int(robjects.r(cmd)(inputs, dim)[0])

    def produce(self, *, inputs: Sequence[Input]) -> Sequence[Output]:
        self.cluster(inputs=inputs)
'''
