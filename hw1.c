#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <ctype.h> // For tolower function

// Function to check if a number is prime
bool isPrime(int num) {
    if (num <= 1) {
        return false; // Numbers less than or equal to 1 are not prime
    }
    for (int i = 2; i * i <= num; i++) {
        if (num % i == 0) {
            return false; // Not prime if divisible by any number other than 1 and itself
        }
    }
    return true;
}

// Function to calculate the factorial of a number
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

// Function to return the appropriate string based on the conditions
const char* primeOrFactorial(int n) {
    if (n <= 1) {
        return "Invalid Input"; // Condition for n <= 1
    } else if (isPrime(n)) {
        return "Prime Number"; // If n is prime
    } else {
        static char result[50]; // Static array to hold the factorial as a string
        sprintf(result, "%lld", factorial(n)); // Calculate factorial and store it in result
        return result; // Return the factorial as a string
    }
}

// Function to sum elements that are equal to their indices
int UABIndexSum(int arr[], int size) {
    int sum = 0;

    // Iterate through the array and add elements equal to their index
    for (int i = 0; i < size; i++) {
        if (arr[i] == i) {
            sum += arr[i];
        }
    }
    return sum;
}

// Function to replace even numbers in an array with 0 and return the modified array
void replaceEvenWithZero(int arr[], int size) {
    // Iterate through the array and replace even numbers with 0
    for (int i = 0; i < size; i++) {
        if (arr[i] % 2 == 0) {
            arr[i] = 0;
        }
    }
}

// Function to print the array
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

// Function to check if a number is an even square
bool evenSquare(int n) {
    if (n < 0) {
        return false; // No negative number can be a square
    }

    int root = (int)sqrt(n); // Calculate the integer square root of n
    if (root * root == n && root % 2 == 0) {
        return true; // n is a square of an even integer
    }
    
    return false; // Otherwise, it is not an even square
}

// Function to count vowels in a string (case insensitive)
int countVowels(const char* s) {
    int count = 0;
    int i = 0;
    
    while (s[i] != '\0') {
        char ch = tolower(s[i]); // Convert to lowercase to make case insensitive
        if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') {
            count++;
        }
        i++;
    }
    
    return count;
}

int main() {
    int n;
    
    // Input a number from the user
    printf("Enter a positive integer: ");
    scanf("%d", &n);

    // Call the primeOrFactorial function and display the result
    printf("%s\n", primeOrFactorial(n));

    // Input array size and elements for UABIndexSum and replaceEvenWithZero
    printf("Enter the size of the array: ");
    int size;
    scanf("%d", &size);
    
    int arr[size];
    printf("Enter %d elements:\n", size);
    for (int i = 0; i < size; i++) {
        scanf("%d", &arr[i]);
    }

    // Call the UABIndexSum function and display the result
    int sum = UABIndexSum(arr, size);
    printf("Sum of elements equal to their indices: %d\n", sum);

    // Call the replaceEvenWithZero function to modify the array
    replaceEvenWithZero(arr, size);

    // Print the modified array
    printf("Array after replacing even numbers with 0: ");
    printArray(arr, size);

    // Call the evenSquare function and display the result
    if (evenSquare(n)) {
        printf("%d is an even square.\n", n);
    } else {
        printf("%d is not an even square.\n", n);
    }

    // Input string to count vowels
    char str[100];
    printf("Enter a string: ");
    scanf(" %[^\n]s", str); // Input string including spaces

    // Call the countVowels function and display the result
    int vowelCount = countVowels(str);
    printf("Number of vowels in the string: %d\n", vowelCount);

    return 0;
}