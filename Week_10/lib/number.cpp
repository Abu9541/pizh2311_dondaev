#include "number.h"
#include <algorithm>
#include <stdexcept>
#include <cstring>

uint2022_t from_uint(uint32_t i) {
    uint2022_t result;
    result.chunks[0] = i;
    return result;
}

uint2022_t from_string(const char* buff) {
    uint2022_t result;
    std::string str(buff);
    
    if (str.empty()) {
        return result;
    }

    for (char c : str) {
        if (!isdigit(c)) {
            throw std::invalid_argument("Invalid character in input string");
        }
    }

    for (size_t i = 0; i < str.size(); ++i) {
        uint32_t carry = 0;
        for (size_t j = 0; j < result.chunks.size(); ++j) {
            uint64_t product = static_cast<uint64_t>(result.chunks[j]) * 10 + carry;
            result.chunks[j] = static_cast<uint32_t>(product & 0xFFFFFFFF);
            carry = static_cast<uint32_t>(product >> 32);
        }
        if (carry != 0) {
            throw std::overflow_error("Number is too large for uint2022_t");
        }

        uint32_t digit = str[i] - '0';
        carry = digit;
        for (size_t j = 0; j < result.chunks.size() && carry != 0; ++j) {
            uint64_t sum = static_cast<uint64_t>(result.chunks[j]) + carry;
            result.chunks[j] = static_cast<uint32_t>(sum & 0xFFFFFFFF);
            carry = static_cast<uint32_t>(sum >> 32);
        }
        if (carry != 0) {
            throw std::overflow_error("Number is too large for uint2022_t");
        }
    }

    return result;
}

uint2022_t operator+(const uint2022_t& lhs, const uint2022_t& rhs) {
    uint2022_t result;
    uint32_t carry = 0;

    for (size_t i = 0; i < lhs.chunks.size(); ++i) {
        uint64_t sum = static_cast<uint64_t>(lhs.chunks[i]) + rhs.chunks[i] + carry;
        result.chunks[i] = static_cast<uint32_t>(sum & 0xFFFFFFFF);
        carry = static_cast<uint32_t>(sum >> 32);
    }

    if (carry != 0 || (lhs.chunks.back() > 0 && rhs.chunks.back() > 0 && result.chunks.back() < std::min(lhs.chunks.back(), rhs.chunks.back()))) {
        throw std::overflow_error("Addition overflow in uint2022_t");
    }

    return result;
}

uint2022_t operator-(const uint2022_t& lhs, const uint2022_t& rhs) {
    uint2022_t result;
    uint32_t borrow = 0;

    for (size_t i = 0; i < lhs.chunks.size(); ++i) {
        uint64_t diff = static_cast<uint64_t>(lhs.chunks[i]) - rhs.chunks[i] - borrow;
        result.chunks[i] = static_cast<uint32_t>(diff & 0xFFFFFFFF);
        borrow = (diff >> 32) ? 1 : 0;
    }

    if (borrow != 0) {
        throw std::underflow_error("Subtraction underflow in uint2022_t");
    }

    return result;
}

uint2022_t operator*(const uint2022_t& lhs, const uint2022_t& rhs) {
    uint2022_t result;
    std::array<uint64_t, uint2022_t::kChunks * 2> temp = {0};

    for (size_t i = 0; i < lhs.chunks.size(); ++i) {
        uint64_t carry = 0;
        for (size_t j = 0; j < rhs.chunks.size(); ++j) {
            uint64_t product = static_cast<uint64_t>(lhs.chunks[i]) * rhs.chunks[j] + temp[i + j] + carry;
            temp[i + j] = product & 0xFFFFFFFF;
            carry = product >> 32;
        }
        if (carry != 0) {
            throw std::overflow_error("Multiplication overflow in uint2022_t");
        }
    }

    for (size_t i = lhs.chunks.size(); i < temp.size(); ++i) {
        if (temp[i] != 0) {
            throw std::overflow_error("Multiplication overflow in uint2022_t");
        }
    }

    for (size_t i = 0; i < result.chunks.size(); ++i) {
        result.chunks[i] = static_cast<uint32_t>(temp[i]);
    }

    return result;
}

bool operator==(const uint2022_t& lhs, const uint2022_t& rhs) {
    return lhs.chunks == rhs.chunks;
}

bool operator!=(const uint2022_t& lhs, const uint2022_t& rhs) {
    return !(lhs == rhs);
}

std::ostream& operator<<(std::ostream& stream, const uint2022_t& value) {
    if (value == uint2022_t()) {
        stream << "0";
        return stream;
    }

    uint2022_t tmp = value;
    std::string result;
    
    while (tmp != uint2022_t()) {
        uint32_t remainder = 0;
        for (int i = tmp.chunks.size() - 1; i >= 0; --i) {
            uint64_t dividend = (static_cast<uint64_t>(remainder) << 32) + tmp.chunks[i];
            tmp.chunks[i] = static_cast<uint32_t>(dividend / 10);
            remainder = static_cast<uint32_t>(dividend % 10);
        }
        result.push_back('0' + remainder);
    }

    std::reverse(result.begin(), result.end());
    stream << result;
    return stream;
}

bool operator>=(const uint2022_t& lhs, const uint2022_t& rhs) {
    for (int i = lhs.chunks.size() - 1; i >= 0; --i) {
        if (lhs.chunks[i] > rhs.chunks[i]) {
            return true;
        } else if (lhs.chunks[i] < rhs.chunks[i]) {
            return false;
        }
    }
    return true;
}

uint2022_t operator/(const uint2022_t& lhs, const uint2022_t& rhs) {
    if (rhs == uint2022_t()) {
        throw std::invalid_argument("Division by zero");
    }

    if (lhs == uint2022_t()) {
        return uint2022_t();
    }

    if (rhs == from_uint(1)) {
        return lhs;
    }

    uint2022_t quotient;
    uint2022_t remainder;
    uint2022_t divisor = rhs;

    for (int i = lhs.chunks.size() * 32 - 1; i >= 0; --i) {
        remainder = remainder + remainder;
        if ((lhs.chunks[i / 32] >> (i % 32)) & 1) {
            remainder.chunks[0] |= 1;
        }

        if (remainder >= divisor) { 
            remainder = remainder - divisor;
            quotient.chunks[i / 32] |= (1 << (i % 32));
        }
    }

    return quotient;
}


#include "number.h"
#include <iostream>
#include <limits>

int main() {
    // Basic operations testing
    std::cout << "=== Basic tests ===" << std::endl;
    uint2022_t a = from_uint(123456789);
    uint2022_t b = from_string("987654321");
    std::cout << "a = " << a << std::endl;
    std::cout << "b = " << b << std::endl;
    std::cout << "a + b = " << (a + b) << std::endl;
    std::cout << "b - a = " << (b - a) << std::endl;
    std::cout << "a * b = " << (a * b) << std::endl;
    std::cout << "b / a = " << (b / a) << std::endl;

    // Addition overflow test
    std::cout << "\n=== Addition overflow test ===" << std::endl;
    try {
        uint2022_t max_val;
        for (auto& chunk : max_val.chunks) {
            chunk = std::numeric_limits<uint32_t>::max(); // Все биты установлены в 1
        }
        
        uint2022_t one = from_uint(1);
        uint2022_t overflow = max_val + one;
        
        std::cout << "ERROR: Overflow not detected!" << std::endl;
    } catch (const std::overflow_error& e) {
        std::cout << "Overflow caught: " << e.what() << std::endl;
    }

    // Multiplication overflow test
    std::cout << "\n=== Multiplication overflow test ===" << std::endl;
    try {
        uint2022_t half_max;
        half_max.chunks.back() = 0x80000000; // 2^2019 (для 64 chunks)
        
        uint2022_t overflow = half_max * half_max;
        
        std::cout << "ERROR: Multiplication overflow not detected!" << std::endl;
    } catch (const std::overflow_error& e) {
        std::cout << "Multiplication overflow caught: " << e.what() << std::endl;
    }

    // Subtraction underflow test
    std::cout << "\n=== Subtraction underflow test ===" << std::endl;
    try {
        uint2022_t small = from_uint(5);
        uint2022_t big = from_uint(10);
        uint2022_t result = small - big;
        
        std::cout << "ERROR: Underflow not detected!" << std::endl;
    } catch (const std::underflow_error& e) {
        std::cout << "Underflow caught: " << e.what() << std::endl;
    }

    // Construction from string overflow test
    std::cout << "\n=== String construction overflow test ===" << std::endl;
    try {
        std::string too_large_num = "1";
        too_large_num.append(2022, '0');  // "1" + 2022 zeros = 2^2022
        
        uint2022_t overflow = from_string(too_large_num.c_str());
        
        std::cout << "ERROR: Construction overflow not detected!" << std::endl;
    } catch (const std::overflow_error& e) {
        std::cout << "Construction overflow caught: " << e.what() << std::endl;
    }

    // Division by zero test
    std::cout << "\n=== Division by zero test ===" << std::endl;
    try {
        uint2022_t zero = from_uint(0);
        uint2022_t some_num = from_uint(10);
        uint2022_t result = some_num / zero;
        
        std::cout << "ERROR: Division by zero not detected!" << std::endl;
    } catch (const std::invalid_argument& e) {
        std::cout << "Division by zero caught: " << e.what() << std::endl;
    }

    return 0;
}
