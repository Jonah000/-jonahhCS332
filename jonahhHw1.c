#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

bool isPrime(int num) {
    if (num <= 1) {
        return false;
    }
    for (int i = 2; i * i <= num; i++) {
        if (num % i == 0) {
            return false;
        }
    }
    return true;
}

long long factorial(int num) {
    if (num == 0 || num == 1) {
        return 1;
    }
    long long result = 1;
    for (int i = 2; i <= num; i++) {
        result *= i;
    }
    return result;
}

const char* primeOrFactorial(int n) {
    if (n <= 1) {
        return "Invalid Input";
    } else if (isPrime(n)) {
        return "Prime Number";
    } else {
        static char result[50];
        sprintf(result, "%lld", factorial(n));
        return result;
    }
}

int UABIndexSum(int arr[], int size) {
    int sum = 0;

    for (int i = 0; i < size; i++) {
        if (arr[i] == i) {
            sum += arr[i];
        }
    }
    return sum;
}

void replaceEvenWithZero(int arr[], int size) {

    for (int i = 0; i < size; i++) {
        if (arr[i] % 2 == 0) {
            arr[i] = 0;
        }
    }
}

void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

bool evenSquare(int n) {
    if (n < 0) {
        return false;
    }

    int root = (int)sqrt(n);
    if (root * root == n && root % 2 == 0) {
        return true;
    }
    
    return false;
}

int countVowels(const char* s) {
    int count = 0;
    int i = 0;
    
    while (s[i] != '\0') {
        char ch = tolower(s[i]);
        if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') {
            count++;
        }
        i++;
    }
    
    return count;
}

int main() {
    int n;
    
    printf("Enter a positive integer: ");
    scanf("%d", &n);

    printf("%s\n", primeOrFactorial(n));

    printf("Enter the size of the array: ");
    int size;
    scanf("%d", &size);
    
    int arr[size];
    printf("Enter %d elements:\n", size);
    for (int i = 0; i < size; i++) {
        scanf("%d", &arr[i]);
    }

    int sum = UABIndexSum(arr, size);
    printf("Sum of elements equal to their indices: %d\n", sum);

    replaceEvenWithZero(arr, size);

    printf("Array after replacing even numbers with 0: ");
    printArray(arr, size);

    if (evenSquare(n)) {
        printf("%d is an even square.\n", n);
    } else {
        printf("%d is not an even square.\n", n);
    }

    char str[100];
    printf("Enter a string: ");
    scanf(" %s", str);

    int vowelCount = countVowels(str);
    printf("Number of vowels in the string: %d\n", vowelCount);

    return 0;
}