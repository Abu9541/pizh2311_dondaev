#include <lib/number.h>
#include <iostream>
#include <limits>

int main() {
    // Basic operations testing
    std::cout << "=== Basic tests ===" << std::endl;
    UInt2022 a = UInt2022::create_from_uint(123456789);
    UInt2022 b = UInt2022::create_from_string("987654321");
    std::cout << "a = " << a << std::endl;
    std::cout << "b = " << b << std::endl;
    std::cout << "a + b = " << (a + b) << std::endl;
    std::cout << "b - a = " << (b - a) << std::endl;
    std::cout << "a * b = " << (a * b) << std::endl;
    std::cout << "b / a = " << (b / a) << std::endl;

    // Addition overflow test
    std::cout << "\n=== Addition overflow test ===" << std::endl;
    try {
        UInt2022 max_val;
        for (auto& chunk : max_val.chunks) {
            chunk = std::numeric_limits<uint32_t>::max();
        }
        
        UInt2022 one = UInt2022::create_from_uint(1);
        UInt2022 overflow = max_val + one;
        
        std::cout << "ERROR: Overflow not detected!" << std::endl;
    } catch (const std::overflow_error& e) {
        std::cout << "Overflow caught: " << e.what() << std::endl;
    }

    // Multiplication overflow test
    std::cout << "\n=== Multiplication overflow test ===" << std::endl;
    try {
        UInt2022 half_max;
        half_max.chunks.back() = 0x80000000;
        
        UInt2022 overflow = half_max * half_max;
        
        std::cout << "ERROR: Multiplication overflow not detected!" << std::endl;
    } catch (const std::overflow_error& e) {
        std::cout << "Multiplication overflow caught: " << e.what() << std::endl;
    }

    // Subtraction underflow test
    std::cout << "\n=== Subtraction underflow test ===" << std::endl;
    try {
        UInt2022 small = UInt2022::create_from_uint(5);
        UInt2022 big = UInt2022::create_from_uint(10);
        UInt2022 result = small - big;
        
        std::cout << "ERROR: Underflow not detected!" << std::endl;
    } catch (const std::underflow_error& e) {
        std::cout << "Underflow caught: " << e.what() << std::endl;
    }

    // Construction from string overflow test
    std::cout << "\n=== String construction overflow test ===" << std::endl;
    try {
        std::string too_large_num = "1";
        too_large_num.append(2022, '0');
        
        UInt2022 overflow = UInt2022::create_from_string(too_large_num.c_str());
        
        std::cout << "ERROR: Construction overflow not detected!" << std::endl;
    } catch (const std::overflow_error& e) {
        std::cout << "Construction overflow caught: " << e.what() << std::endl;
    }

    // Division by zero test
    std::cout << "\n=== Division by zero test ===" << std::endl;
    try {
        UInt2022 zero = UInt2022::create_from_uint(0);
        UInt2022 some_num = UInt2022::create_from_uint(10);
        UInt2022 result = some_num / zero;
        
        std::cout << "ERROR: Division by zero not detected!" << std::endl;
    } catch (const std::invalid_argument& e) {
        std::cout << "Division by zero caught: " << e.what() << std::endl;
    }

    return 0;
}