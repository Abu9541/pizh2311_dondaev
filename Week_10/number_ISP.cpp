#include "number.h"
#include <algorithm>
#include <stdexcept>
#include <cstring>

void UInt2022::from_uint(uint32_t i) {
    chunks.fill(0);
    chunks[0] = i;
}

void UInt2022::from_string(const char* buff) {
    chunks.fill(0);
    std::string str(buff);
    
    if (str.empty()) {
        return;
    }

    for (char c : str) {
        if (!isdigit(c)) {
            throw std::invalid_argument("Invalid character in input string");
        }
    }

    for (size_t i = 0; i < str.size(); ++i) {
        uint32_t carry = 0;
        for (size_t j = 0; j < chunks.size(); ++j) {
            uint64_t product = static_cast<uint64_t>(chunks[j]) * 10 + carry;
            chunks[j] = static_cast<uint32_t>(product & 0xFFFFFFFF);
            carry = static_cast<uint32_t>(product >> 32);
        }
        if (carry != 0) {
            throw std::overflow_error("Number is too large for uint2022_t");
        }

        uint32_t digit = str[i] - '0';
        carry = digit;
        for (size_t j = 0; j < chunks.size() && carry != 0; ++j) {
            uint64_t sum = static_cast<uint64_t>(chunks[j]) + carry;
            chunks[j] = static_cast<uint32_t>(sum & 0xFFFFFFFF);
            carry = static_cast<uint32_t>(sum >> 32);
        }
        if (carry != 0) {
            throw std::overflow_error("Number is too large for uint2022_t");
        }
    }
}

IArithmeticOperations* UInt2022::add(const IArithmeticOperations* other) {
    const UInt2022* rhs = dynamic_cast<const UInt2022*>(other);
    if (!rhs) {
        throw std::invalid_argument("Invalid type for addition");
    }
    return new UInt2022(*this + *rhs);
}

IArithmeticOperations* UInt2022::subtract(const IArithmeticOperations* other) {
    const UInt2022* rhs = dynamic_cast<const UInt2022*>(other);
    if (!rhs) {
        throw std::invalid_argument("Invalid type for subtraction");
    }
    return new UInt2022(*this - *rhs);
}

IArithmeticOperations* UInt2022::multiply(const IArithmeticOperations* other) {
    const UInt2022* rhs = dynamic_cast<const UInt2022*>(other);
    if (!rhs) {
        throw std::invalid_argument("Invalid type for multiplication");
    }
    return new UInt2022(*this * *rhs);
}

IArithmeticOperations* UInt2022::divide(const IArithmeticOperations* other) {
    const UInt2022* rhs = dynamic_cast<const UInt2022*>(other);
    if (!rhs) {
        throw std::invalid_argument("Invalid type for division");
    }
    return new UInt2022(*this / *rhs);
}

bool UInt2022::equals(const IComparisonOperations* other) const {
    const UInt2022* rhs = dynamic_cast<const UInt2022*>(other);
    if (!rhs) {
        return false;
    }
    return chunks == rhs->chunks;
}

bool UInt2022::not_equals(const IComparisonOperations* other) const {
    return !equals(other);
}

bool UInt2022::greater_or_equal(const IComparisonOperations* other) const {
    const UInt2022* rhs = dynamic_cast<const UInt2022*>(other);
    if (!rhs) {
        throw std::invalid_argument("Invalid type for comparison");
    }
    
    for (int i = chunks.size() - 1; i >= 0; --i) {
        if (chunks[i] > rhs->chunks[i]) {
            return true;
        } else if (chunks[i] < rhs->chunks[i]) {
            return false;
        }
    }
    return true;
}

void UInt2022::print(std::ostream& stream) const {
    if (*this == UInt2022()) {
        stream << "0";
        return;
    }

    UInt2022 tmp = *this;
    std::string result;
    
    while (tmp != UInt2022()) {
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
}

UInt2022 UInt2022::create_from_uint(uint32_t i) {
    UInt2022 result;
    result.from_uint(i);
    return result;
}

UInt2022 UInt2022::create_from_string(const char* buff) {
    UInt2022 result;
    result.from_string(buff);
    return result;
}

// Global operators implementations (same logic as before)
UInt2022 operator+(const UInt2022& lhs, const UInt2022& rhs) {
    UInt2022 result;
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

UInt2022 operator-(const UInt2022& lhs, const UInt2022& rhs) {
    UInt2022 result;
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

UInt2022 operator*(const UInt2022& lhs, const UInt2022& rhs) {
    UInt2022 result;
    std::array<uint64_t, UInt2022::kChunks * 2> temp = {0};

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

bool operator==(const UInt2022& lhs, const UInt2022& rhs) {
    return lhs.chunks == rhs.chunks;
}

bool operator!=(const UInt2022& lhs, const UInt2022& rhs) {
    return !(lhs == rhs);
}

std::ostream& operator<<(std::ostream& stream, const UInt2022& value) {
    value.print(stream);
    return stream;
}

bool operator>=(const UInt2022& lhs, const UInt2022& rhs) {
    return lhs.greater_or_equal(&rhs);
}

UInt2022 operator/(const UInt2022& lhs, const UInt2022& rhs) {
    if (rhs == UInt2022()) {
        throw std::invalid_argument("Division by zero");
    }

    if (lhs == UInt2022()) {
        return UInt2022();
    }

    if (rhs == UInt2022::create_from_uint(1)) {
        return lhs;
    }

    UInt2022 quotient;
    UInt2022 remainder;
    UInt2022 divisor = rhs;

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