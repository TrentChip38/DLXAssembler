//Heres one way that should be easily transferable to assembly
int factorial(int n) {
    if (n < 0) {
        return -1;
    }
    if (n == 0) {
        return 1;
    }
    int i = 1;
    int result = 1;
    int prevresult = 0;
    while(i <= n) {
        prevresult = result;
        //result = oldresult * i;
        for(int j = 1; j < i; j++) {
            result += prevresult;
        }
        i++;
    }
    return result;
}
