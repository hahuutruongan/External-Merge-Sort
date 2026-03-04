#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <queue>
#include <cstdio>
#include <iomanip>

using namespace std;

struct MinHeapNode {
    double element;
    size_t fileIndex;
    
    bool operator>(const MinHeapNode& other) const {
        return element > other.element;
    }
};

void printArray(const vector<double>& arr) {
    for (double val : arr) {
        cout << fixed << setprecision(2) << val << "  ";
    }
    cout << endl;
}

void externalMergeSort(const string& inputFile, const string& outputFile, long long ramBytes) {
    ifstream inFile(inputFile, ios::binary | ios::ate);
    if (!inFile) {
        cout << "[Loi] Khong the mo tap tin nguon!\n";
        return;
    }

    streamsize fileSize = inFile.tellg();
    inFile.seekg(0, ios::beg);
    
    if (fileSize % static_cast<streamsize>(sizeof(double)) != 0) {
        cout << "[Loi] Kich thuoc tap tin khong hop le.\n";
        return;
    }

    size_t totalElements = static_cast<size_t>(fileSize) / sizeof(double);
    if (totalElements == 0) return;

    // TÍNH TOÁN CHUNK SIZE DỰA TRÊN BYTE (Chia cho 8 bytes của số double)
    size_t CHUNK_SIZE = static_cast<size_t>(ramBytes / sizeof(double));
    
    // Đề phòng trường hợp RAM cấp quá nhỏ, tối thiểu phải chứa được 1 số
    if (CHUNK_SIZE == 0) CHUNK_SIZE = 1; 

    if (totalElements < CHUNK_SIZE) {
        CHUNK_SIZE = totalElements;
    }

    // Biến illustrate tự động bật nếu số lượng phần tử đủ nhỏ (<= 1000)
    bool illustrate = (totalElements <= 1000);

    // Tính ngược lại MB chỉ để hiển thị log cho đẹp
    double displayMB = static_cast<double>(ramBytes) / (1024.0 * 1024.0);

    cout << ">> Du lieu: " << totalElements << " phan tu.\n";
    cout << ">> RAM cap phat: " << fixed << setprecision(4) << displayMB << " MB (" << CHUNK_SIZE << " phan tu/chunk).\n";

    // --- PHASE 1: SPLIT & LOCAL SORT ---
    size_t numChunks = 0;
    vector<string> tempFiles;
    vector<double> buffer(CHUNK_SIZE);

    if (illustrate) cout << "\n[PHASE 1] Phan chia va sap xep cuc bo:" << endl;

    while (inFile.tellg() < fileSize && inFile.tellg() != -1) {
        size_t elementsToRead = min(CHUNK_SIZE, totalElements - numChunks * CHUNK_SIZE);
        if (elementsToRead == 0) break;
        
        inFile.read(reinterpret_cast<char*>(buffer.data()), static_cast<streamsize>(elementsToRead * sizeof(double)));
        sort(buffer.begin(), buffer.begin() + elementsToRead);

        if (illustrate) {
            cout << "  - Chunk " << numChunks + 1 << " (da sap xep): ";
            printArray(vector<double>(buffer.begin(), buffer.begin() + elementsToRead));
        }

        string tempFileName = "temp_run_" + to_string(numChunks) + ".bin";
        tempFiles.push_back(tempFileName);
        
        ofstream tempFile(tempFileName, ios::binary);
        tempFile.write(reinterpret_cast<const char*>(buffer.data()), static_cast<streamsize>(elementsToRead * sizeof(double)));
        tempFile.close();

        numChunks++;
    }
    inFile.close();

    // --- PHASE 2: K-WAY MERGE ---
    if (illustrate) cout << "\n[PHASE 2] Tron cac tap tin tam (K-Way Merge):" << endl;

    ofstream outFile(outputFile, ios::binary);
    vector<ifstream*> tempFilePointers;
    priority_queue<MinHeapNode, vector<MinHeapNode>, greater<MinHeapNode>> minHeap;

    for (size_t i = 0; i < numChunks; i++) {
        ifstream* f = new ifstream(tempFiles[i], ios::binary);
        tempFilePointers.push_back(f);
        
        double firstElement;
        if (f->read(reinterpret_cast<char*>(&firstElement), sizeof(double))) {
            minHeap.push({firstElement, i});
        }
    }

    int step = 1;
    while (!minHeap.empty()) {
        MinHeapNode root = minHeap.top();
        minHeap.pop();

        outFile.write(reinterpret_cast<const char*>(&root.element), sizeof(double));
        
        if (illustrate) {
            cout << "  - Buoc " << step++ << ": Lay " << fixed << setprecision(2) << root.element 
                 << " tu " << tempFiles[root.fileIndex] << " ghi vao file dich." << endl;
        }

        double nextElement;
        if (tempFilePointers[root.fileIndex]->read(reinterpret_cast<char*>(&nextElement), sizeof(double))) {
            minHeap.push({nextElement, root.fileIndex});
        }
    }

    outFile.close();
    for (size_t i = 0; i < numChunks; i++) {
        tempFilePointers[i]->close();
        delete tempFilePointers[i];
        remove(tempFiles[i].c_str()); 
    }

    cout << "\n--- HOAN TAT XU LY ---\n";
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        cout << "[Loi] Sai cu phap. Can 3 tham so: input output ram_bytes\n";
        return 1;
    }

    string inputFile = argv[1];
    string outputFile = argv[2];
    
    // Chuyển chuỗi tham số thành số nguyên long long (Bytes)
    try {
        long long ramBytes = stoll(argv[3]); 
        externalMergeSort(inputFile, outputFile, ramBytes);
    } catch (...) {
        cout << "[Loi] Tham so RAM khong hop le.\n";
        return 1;
    }

    return 0;
}