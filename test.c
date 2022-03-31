#include <stdio.h>
#define BYTE_WIDTH 8

int main() {

    short a = 33;

    for(int i = 0; i < sizeof(a)*BYTE_WIDTH; ++i) {
        char c;
        if (a & 1) c = '1';
        else c = '0';
        putchar(c);
        a >>= 1;
    }
    

}