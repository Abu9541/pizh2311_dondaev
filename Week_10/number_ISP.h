#pragma once
#include <cinttypes>
#include <iostream>
#include <array>
#include <string>

class INumberConverter {
public:
    virtual ~INumberConverter() = default;
    virtual void from_uint(uint32_t i) = 0;
    virtual void from_string(const char* buff) = 0;
};

class IArithmeticOperations {
public:
    virtual ~IArithmeticOperations() = default;
    virtual IArithmeticOperations* add(const IArithmeticOperations* other) = 0;
    virtual IArithmeticOperations* subtract(const IArithmeticOperations* other) = 0;
    virtual IArithmeticOperations* multiply(const IArithmeticOperations* other) = 0;
    virtual IArithmeticOperations* divide(const IArithmeticOperations* other) = 0;
};

class IComparisonOperations {
public:
    virtual ~IComparisonOperations() = default;
    virtual bool equals(const IComparisonOperations* other) const = 0;
    virtual bool not_equals(const IComparisonOperations* other) const = 0;
    virtual bool greater_or_equal(const IComparisonOperations* other) const = 0;
};

class IOutputOperation {
public:
    virtual ~IOutputOperation() = default;
    virtual void print(std::ostream& stream) const = 0;
};

class UInt2022 : public INumberConverter, 
                 public IArithmeticOperations,
                 public IComparisonOperations,
                 public IOutputOperation {
public:
    static const size_t kBits = 2022;
    static const size_t kBytes = (kBits + 7) / 8;
    static const size_t kChunks = (kBits + 31) / 32;
    std::array<uint32_t, kChunks> chunks;

    UInt2022() {
        chunks.fill(0);
    }

    // INumberConverter implementation
    void from_uint(uint32_t i) override;
    void from_string(const char* buff) override;

    // IArithmeticOperations implementation
    IArithmeticOperations* add(const IArithmeticOperations* other) override;
    IArithmeticOperations* subtract(const IArithmeticOperations* other) override;
    IArithmeticOperations* multiply(const IArithmeticOperations* other) override;
    IArithmeticOperations* divide(const IArithmeticOperations* other) override;

    // IComparisonOperations implementation
    bool equals(const IComparisonOperations* other) const override;
    bool not_equals(const IComparisonOperations* other) const override;
    bool greater_or_equal(const IComparisonOperations* other) const override;

    // IOutputOperation implementation
    void print(std::ostream& stream) const override;

    // Helper methods
    static UInt2022 create_from_uint(uint32_t i);
    static UInt2022 create_from_string(const char* buff);
};

// Global operators for backward compatibility
UInt2022 operator+(const UInt2022& lhs, const UInt2022& rhs);
UInt2022 operator-(const UInt2022& lhs, const UInt2022& rhs);
UInt2022 operator*(const UInt2022& lhs, const UInt2022& rhs);
UInt2022 operator/(const UInt2022& lhs, const UInt2022& rhs);
bool operator==(const UInt2022& lhs, const UInt2022& rhs);
bool operator!=(const UInt2022& lhs, const UInt2022& rhs);
bool operator>=(const UInt2022& lhs, const UInt2022& rhs);
std::ostream& operator<<(std::ostream& stream, const UInt2022& value);