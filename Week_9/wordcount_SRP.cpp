#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cctype>
#include <algorithm>

//Класс для хранения данных
class FileStats {
private:
    std::size_t lines = 0;
    std::size_t words = 0;
    std::size_t bytes = 0;
    std::size_t chars = 0;
    std::string filename;

public:
    FileStats(const std::string& name) : filename(name) {}

    void setLines(std::size_t l) { lines = l; }
    void setWords(std::size_t w) { words = w; }
    void setBytes(std::size_t b) { bytes = b; }
    void setChars(std::size_t c) { chars = c; }

    std::size_t getLines() const { return lines; }
    std::size_t getWords() const { return words; }
    std::size_t getBytes() const { return bytes; }
    std::size_t getChars() const { return chars; }
    std::string getFilename() const { return filename; }
};

//Класс для подсчета статистики
class FileStatsCounter {
public:
    static FileStats count(const std::string& filename) {
        FileStats stats(filename);
        
        std::ifstream file(filename, std::ios::binary | std::ios::ate);
        if (!file.is_open()) {
            std::cerr << "Error: Could not open file " << filename << "\n";
            return stats;
        }
        
        stats.setBytes(file.tellg());
        file.seekg(0, std::ios::beg);
        
        bool inWord = false;
        char ch;
        
        while (file.get(ch)) {
            stats.setChars(stats.getChars() + 1);
            
            if (ch == '\n') {
                stats.setLines(stats.getLines() + 1);
            }
            
            if (std::isspace(static_cast<unsigned char>(ch))) {
                if (inWord) {
                    stats.setWords(stats.getWords() + 1);
                    inWord = false;
                }
            } else {
                inWord = true;
            }
        }
        
        if (inWord) {
            stats.setWords(stats.getWords() + 1);
        }
        
        return stats;
    }
};

//Класс для вывода результатов
class StatsPrinter {
public:
    static void print(const FileStats& stats, bool showLines, bool showWords, 
                     bool showBytes, bool showChars) {
        if (showLines) {
            std::cout << stats.getLines() << " ";
        }
        if (showWords) {
            std::cout << stats.getWords() << " ";
        }
        if (showBytes) {
            std::cout << stats.getBytes() << " ";
        }
        if (showChars) {
            std::cout << stats.getChars() << " ";
        }
        std::cout << stats.getFilename() << "\n";
    }
};

//Класс для обработки аргументов
class ArgumentParser {
private:
    bool showLines = false;
    bool showWords = false;
    bool showBytes = false;
    bool showChars = false;
    bool defaultMode = true;
    std::vector<std::string> filenames;

public:
    void parse(int argc, char* argv[]) {
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            
            if (arg[0] == '-') {
                defaultMode = false;
                
                if (arg == "-l" || arg == "--lines") {
                    showLines = true;
                } else if (arg == "-w" || arg == "--words") {
                    showWords = true;
                } else if (arg == "-c" || arg == "--bytes") {
                    showBytes = true;
                } else if (arg == "-m" || arg == "--chars") {
                    showChars = true;
                } else if (arg.size() > 1 && arg[0] == '-' && arg[1] != '-') {
                    parseCombinedOptions(arg);
                } else {
                    throw std::runtime_error("Error: Unknown option " + arg);
                }
            } else {
                filenames.push_back(arg);
            }
        }
        
        if (defaultMode) {
            showLines = true;
            showWords = true;
            showBytes = true;
        }
    }

    bool shouldShowLines() const { return showLines; }
    bool shouldShowWords() const { return showWords; }
    bool shouldShowBytes() const { return showBytes; }
    bool shouldShowChars() const { return showChars; }
    const std::vector<std::string>& getFilenames() const { return filenames; }

private:
    void parseCombinedOptions(const std::string& arg) {
        for (size_t j = 1; j < arg.size(); ++j) {
            switch (arg[j]) {
                case 'l': showLines = true; break;
                case 'w': showWords = true; break;
                case 'c': showBytes = true; break;
                case 'm': showChars = true; break;
                default:
                    throw std::runtime_error("Error: Unknown option -" + std::string(1, arg[j]));
            }
        }
    }
};

//Класс для координации работы приложения
class WordCountApplication {
public:
    static void printUsage() {
        std::cout << "Usage: WordCount.exe [OPTION] filename [filename,.....]\n"
                  << "Options:\n"
                  << "  -l, --lines    print the line counts\n"
                  << "  -c, --bytes    print the byte counts\n"
                  << "  -w, --words    print the word counts\n"
                  << "  -m, --chars    print the character counts\n"
                  << "If no options are specified, -l, -w, -c are assumed\n";
    }

    static int run(int argc, char* argv[]) {
        if (argc < 2) {
            printUsage();
            return 1;
        }
        
        try {
            ArgumentParser parser;
            parser.parse(argc, argv);
            
            const auto& filenames = parser.getFilenames();
            if (filenames.empty()) {
                std::cerr << "Error: No input files specified\n";
                printUsage();
                return 1;
            }
            
            for (const auto& filename : filenames) {
                FileStats stats = FileStatsCounter::count(filename);
                StatsPrinter::print(stats, 
                                    parser.shouldShowLines(), 
                                    parser.shouldShowWords(), 
                                    parser.shouldShowBytes(), 
                                    parser.shouldShowChars());
            }
        } catch (const std::exception& e) {
            std::cerr << e.what() << "\n";
            printUsage();
            return 1;
        }
        
        return 0;
    }
};

//Точка входа программы
int main(int argc, char* argv[]) {
    return WordCountApplication::run(argc, argv);
}