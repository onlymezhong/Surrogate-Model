#!/usr/bin/env bash
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

set -e

# Install dependencies from ubuntu deb repository.
apt-get update
apt-get install -y \
    bc \
    build-essential \
    curl \
    git \
    pkg-config \
    python-dev \
    python-numpy \
    python-pip \
    python3-dev \
    python3-numpy \
    python3-pip \
    software-properties-common \
    swig \
    unzip \
    wget \
    zip \
    zlib1g-dev
apt-get clean
rm -rf /var/lib/apt/lists/*