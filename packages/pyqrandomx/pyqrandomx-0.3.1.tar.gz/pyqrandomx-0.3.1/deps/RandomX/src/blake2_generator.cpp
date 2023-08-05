/*
Copyright (c) 2018-2019, tevador <tevador@gmail.com>

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
	* Redistributions of source code must retain the above copyright
	  notice, this list of conditions and the following disclaimer.
	* Redistributions in binary form must reproduce the above copyright
	  notice, this list of conditions and the following disclaimer in the
	  documentation and/or other materials provided with the distribution.
	* Neither the name of the copyright holder nor the
	  names of its contributors may be used to endorse or promote products
	  derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#include <stddef.h>
#include "blake2/blake2.h"
#include "blake2/endian.h"
#include "blake2_generator.hpp"

namespace randomx {

	constexpr int maxSeedSize = 60;

	Blake2Generator::Blake2Generator(const void* seed, size_t seedSize, int nonce) : dataIndex(sizeof(data)) {
		memset(data, 0, sizeof(data));
		memcpy(data, seed, seedSize > maxSeedSize ? maxSeedSize : seedSize);
		store32(&data[maxSeedSize], nonce);
	}

	uint8_t Blake2Generator::getByte() {
		checkData(1);
		return data[dataIndex++];
	}

	uint32_t Blake2Generator::getUInt32() {
		checkData(4);
		auto ret = load32(&data[dataIndex]);
		dataIndex += 4;
		return ret;
	}

	void Blake2Generator::checkData(const size_t bytesNeeded) {
		if (dataIndex + bytesNeeded > sizeof(data)) {
			blake2b(data, sizeof(data), data, sizeof(data), nullptr, 0);
			dataIndex = 0;
		}
	}
}