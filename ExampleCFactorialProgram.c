#include <stdio.h>
//Just my example to look at and think about factorial calculation
int main() {
    int n, i;
    // Use unsigned long long to handle larger factorials (up to 20!)
    unsigned long long factorial = 1;

    printf("Enter a non-negative integer: ");
    scanf("%d", &n);

    // Check for negative input
    if (n < 0) {
        printf("Error! Factorial of a negative number doesn't exist.\\n");
    } else {
        // 0! is 1, so the loop doesn't run for n=0, which is correct.
        for (i = 1; i <= n; ++i) {
            factorial *= i; // factorial = factorial * i;
        }
        printf("Factorial of %d = %llu\\n", n, factorial);
    }

    return 0;
}
